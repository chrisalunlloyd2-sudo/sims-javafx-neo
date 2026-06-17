package com.simsneo.engine;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.*;
import java.util.concurrent.*;

/**
 * Persistent JSON-over-stdio bridge to sprite_core/sim_backend.py.
 *
 * One subprocess lives for the JVM session. Requests are serialised
 * (single writer + ordered pending queue) — sim_backend.py is single-threaded.
 *
 * Usage (singleton):
 *   JsonNode resp = SimPythonBridge.getInstance().sendSync("get_agents", 1000);
 */
public class SimPythonBridge {

    private static final String PYTHON  = "C:\\Python314\\python.exe";
    private static final String BACKEND = "C:\\Viper\\projects\\sims-javafx-neo\\sprite_core\\sim_backend.py";

    // Eager singleton — initialised once when class is loaded
    private static final SimPythonBridge INSTANCE = new SimPythonBridge();

    private Process        proc;
    private BufferedWriter writer;
    private BufferedReader reader;
    private boolean        ready = false;

    private final ObjectMapper mapper = new ObjectMapper();

    // In-order pending futures — responses arrive in the same order as requests
    private final BlockingDeque<CompletableFuture<JsonNode>> pending =
            new LinkedBlockingDeque<>();

    private final ExecutorService pool = Executors.newSingleThreadExecutor(r -> {
        Thread t = new Thread(r, "sim-reader");
        t.setDaemon(true);
        return t;
    });

    private SimPythonBridge() {
        startProcess();
    }

    public static SimPythonBridge getInstance() {
        return INSTANCE;
    }

    // ── startup ───────────────────────────────────────────────────────────────

    private void startProcess() {
        try {
            ProcessBuilder pb = new ProcessBuilder(PYTHON, "-u", BACKEND);
            pb.redirectErrorStream(false);
            proc   = pb.start();
            writer = new BufferedWriter(new OutputStreamWriter(proc.getOutputStream(), "UTF-8"));
            reader = new BufferedReader(new InputStreamReader(proc.getInputStream(),  "UTF-8"));

            // Consume the one-line ready banner before entering the read loop
            String banner = reader.readLine();
            if (banner != null && banner.contains("sim_backend ready")) {
                ready = true;
                System.err.println("[SimBridge] sim_backend.py online");
            } else {
                System.err.println("[SimBridge] Unexpected banner: " + banner);
            }

            pool.submit(this::readLoop);
        } catch (Exception e) {
            System.err.println("[SimBridge] Failed to start sim_backend.py: " + e.getMessage());
        }
    }

    // ── reader thread ─────────────────────────────────────────────────────────

    private void readLoop() {
        try {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.isBlank()) continue;
                CompletableFuture<JsonNode> future = pending.pollFirst();
                if (future == null) continue;
                try {
                    future.complete(mapper.readTree(line));
                } catch (Exception e) {
                    future.completeExceptionally(e);
                }
            }
        } catch (IOException e) {
            System.err.println("[SimBridge] Reader ended: " + e.getMessage());
        } finally {
            // Drain pending futures so callers don't hang
            CompletableFuture<JsonNode> f;
            while ((f = pending.pollFirst()) != null) {
                f.completeExceptionally(new IOException("sim_backend disconnected"));
            }
        }
    }

    // ── public API ────────────────────────────────────────────────────────────

    /**
     * Send a named command with no extra fields. Blocks up to timeoutMs.
     * Returns null on error / timeout.
     */
    public JsonNode sendSync(String cmd, long timeoutMs) {
        ObjectNode msg = mapper.createObjectNode();
        msg.put("cmd", cmd);
        return sendSync(msg, timeoutMs);
    }

    /**
     * Send an arbitrary JSON message. Blocks up to timeoutMs.
     * Returns null on error / timeout.
     */
    public JsonNode sendSync(ObjectNode msg, long timeoutMs) {
        if (!ready) return null;
        CompletableFuture<JsonNode> future = new CompletableFuture<>();
        try {
            pending.offerLast(future);
            writer.write(mapper.writeValueAsString(msg));
            writer.newLine();
            writer.flush();
            return future.get(timeoutMs, TimeUnit.MILLISECONDS);
        } catch (TimeoutException e) {
            pending.remove(future);
            future.cancel(false);
            System.err.println("[SimBridge] Timeout on: " + msg.path("cmd").asText("?"));
            return null;
        } catch (Exception e) {
            System.err.println("[SimBridge] sendSync error: " + e.getMessage());
            return null;
        }
    }

    public boolean isReady() { return ready; }

    public void shutdown() {
        try { writer.close();          } catch (Exception ignored) {}
        try { if (proc != null) proc.destroyForcibly(); } catch (Exception ignored) {}
        pool.shutdownNow();
    }
}
