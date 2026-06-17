package com.simsneo.engine;

import com.fasterxml.jackson.databind.JsonNode;
import java.util.ArrayList;
import java.util.List;

/**
 * Facade over SimPythonBridge — preserves the API that GameLoop uses.
 * Delegates to the singleton persistent bridge instead of spawning new processes.
 */
public class SpriteBridge {

    private final SimPythonBridge bridge = SimPythonBridge.getInstance();

    public List<AgentData> getActiveAgents() {
        List<AgentData> agents = new ArrayList<>();
        JsonNode resp = bridge.sendSync("get_agents", 1000);
        if (resp == null || !resp.path("ok").asBoolean(false)) return agents;
        JsonNode arr = resp.path("data").path("agents");
        if (arr.isArray()) {
            for (JsonNode a : arr) {
                agents.add(new AgentData(
                    a.path("name").asText("?"),
                    a.path("anchor").asText("?"),
                    a.path("traits"),
                    a.path("uuid").asText(""),
                    a.path("trust").asDouble(0.5)
                ));
            }
        }
        return agents;
    }

    public GridStatus getGridStatus() {
        JsonNode resp = bridge.sendSync("get_grid", 500);
        if (resp == null || !resp.path("ok").asBoolean(false)) return new GridStatus(1, 0);
        JsonNode d = resp.path("data");
        return new GridStatus(d.path("nodes").asInt(1), d.path("agents").asInt(0));
    }

    public void tick() {
        bridge.sendSync("tick", 300);
    }

    // ── value types used by GameLoop ──────────────────────────────────────────

    public static class GridStatus {
        public int nodes;
        public int agents;
        public GridStatus(int n, int a) { this.nodes = n; this.agents = a; }
    }

    public static class AgentData {
        public String   name;
        public String   anchor;
        public JsonNode traits;
        public String   uuid;
        public double   trust;

        public AgentData(String n, String a, JsonNode t, String u, double s) {
            this.name   = n;
            this.anchor = a;
            this.traits = t;
            this.uuid   = u;
            this.trust  = s;
        }
    }
}
