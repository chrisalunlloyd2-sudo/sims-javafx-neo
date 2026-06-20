"""
sim_backend.py — Persistent Python simulation backend for sims-javafx-neo.

JSON-over-stdio protocol: reads one JSON command per line from stdin,
writes one JSON response per line to stdout. Runs as a child process
managed by SimPythonBridge.java via ProcessBuilder.

Commands:
  {"cmd": "status"}            → system status + DB stats
  {"cmd": "get_agents"}        → list all agent profiles
  {"cmd": "get_grid"}          → grid topology + node count
  {"cmd": "get_system"}        → live CPU/mem/disk metrics
  {"cmd": "tick"}              → advance one simulation step
  {"cmd": "add_performative", "sentence": "...", "script": "..."} → register new command
  {"cmd": "get_performatives", "limit": 20} → list known commands
  {"cmd": "log_transition", "from_id": N, "to_id": M} → record Markov edge

Protocol:
  Every response is {"ok": true, "data": {...}} or {"ok": false, "error": "..."}
  Startup writes {"ok": true, "data": {"msg": "sim_backend ready", "version": "1.0"}}
"""
import sys, json, os, sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT    = Path(__file__).parent.parent   # sims-javafx-neo/
CORE    = Path(__file__).parent          # sprite_core/
DB_DIR  = CORE / "context_fence" / "db"
DB_PATH = DB_DIR / "sprite.db"
LOG     = CORE / f"sim_backend_{datetime.now():%Y%m%d}.log"

# Redirect print() to log so stdout stays clean for JSON protocol
import builtins as _bi
_orig_print = _bi.print
def _log_print(*args, **kwargs):
    kwargs['file'] = sys.stderr
    _orig_print(*args, **kwargs)
_bi.print = _log_print


def _log(msg: str):
    ts = datetime.now().isoformat(timespec='seconds')
    sys.stderr.write(f"[{ts}] {msg}\n")
    sys.stderr.flush()
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def _ok(data: dict) -> str:
    return json.dumps({"ok": True, "data": data})


def _err(msg: str) -> str:
    return json.dumps({"ok": False, "error": msg})


# ── Database ───────────────────────────────────────────────────────────────────

def _init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH))
    con.executescript("""
        CREATE TABLE IF NOT EXISTS performatives (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence    TEXT UNIQUE NOT NULL,
            script_path TEXT,
            exec_count  INTEGER DEFAULT 0,
            last_run    TEXT,
            description TEXT
        );
        CREATE TABLE IF NOT EXISTS environment_states (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            performative_id INTEGER REFERENCES performatives(id),
            cpu_load        REAL,
            mem_free        REAL,
            active_procs    INTEGER,
            recorded_at     TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS markov_transitions (
            from_id     INTEGER REFERENCES performatives(id),
            to_id       INTEGER REFERENCES performatives(id),
            edge_count  INTEGER DEFAULT 1,
            probability REAL    DEFAULT 1.0,
            PRIMARY KEY (from_id, to_id)
        );
        CREATE TABLE IF NOT EXISTS agent_profiles (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT UNIQUE NOT NULL,
            hardware_anchor TEXT,
            traits          TEXT DEFAULT '{}',
            hardware_uuid   TEXT,
            trust_score     REAL DEFAULT 0.5,
            created_at      TEXT DEFAULT (datetime('now'))
        );
    """)
    # Seed agents if empty
    if con.execute("SELECT COUNT(*) FROM agent_profiles").fetchone()[0] == 0:
        agents = [
            ("Discovery",    "CPU", '{"diligence": 0.9, "speed": 0.8}',  "cpu-0", 0.9),
            ("Maintenance",  "HDD", '{"thoroughness": 0.8, "care": 0.7}', "disk-0", 0.85),
            ("Security",     "RAM", '{"vigilance": 0.95, "aggression": 0.6}', "mem-0", 0.95),
        ]
        con.executemany(
            "INSERT INTO agent_profiles(name,hardware_anchor,traits,hardware_uuid,trust_score) VALUES (?,?,?,?,?)",
            agents
        )
    # Seed performatives if empty
    if con.execute("SELECT COUNT(*) FROM performatives").fetchone()[0] == 0:
        seeds = [
            ("System Heartbeat Check",  "scripts/heartbeat.py",   "Checks kernel alive"),
            ("Environment Sweep",       "scripts/sweep.py",        "Scans system states"),
            ("Data Purge",              "scripts/purge.py",        "Cleans redundant logs"),
            ("Discovery Scan",          "sprite_core/discovery.py","Locates new binaries"),
            ("Agent Status Report",     "sprite_core/monitor.py",  "Full agent status"),
        ]
        con.executemany(
            "INSERT INTO performatives(sentence,script_path,description) VALUES (?,?,?)", seeds
        )
    con.commit()
    con.close()
    _log(f"DB initialized at {DB_PATH}")


def _con() -> sqlite3.Connection:
    return sqlite3.connect(str(DB_PATH))


# ── Command handlers ───────────────────────────────────────────────────────────

def cmd_status(_msg: dict) -> str:
    try:
        con = _con()
        agents     = con.execute("SELECT COUNT(*) FROM agent_profiles").fetchone()[0]
        perfs      = con.execute("SELECT COUNT(*) FROM performatives").fetchone()[0]
        transitions = con.execute("SELECT COUNT(*) FROM markov_transitions").fetchone()[0]
        con.close()
        return _ok({
            "msg":         "sim_backend running",
            "db":          str(DB_PATH),
            "agents":      agents,
            "performatives": perfs,
            "transitions": transitions,
            "ts":          datetime.now().isoformat(timespec='seconds'),
        })
    except Exception as e:
        return _err(f"status error: {e}")


def cmd_get_agents(_msg: dict) -> str:
    try:
        con  = _con()
        rows = con.execute(
            "SELECT name, hardware_anchor, traits, hardware_uuid, trust_score FROM agent_profiles"
        ).fetchall()
        con.close()
        agents = [
            {"name": r[0], "anchor": r[1], "traits": json.loads(r[2] or "{}"),
             "uuid": r[3], "trust": r[4]}
            for r in rows
        ]
        return _ok({"agents": agents, "count": len(agents)})
    except Exception as e:
        return _err(f"get_agents error: {e}")


def cmd_get_grid(_msg: dict) -> str:
    try:
        con    = _con()
        agents = con.execute("SELECT COUNT(*) FROM agent_profiles").fetchone()[0]
        edges  = con.execute("SELECT COUNT(*) FROM markov_transitions").fetchone()[0]
        con.close()
        return _ok({
            "nodes":  3,
            "agents": agents,
            "edges":  edges,
            "topology": "mesh",
        })
    except Exception as e:
        return _err(f"get_grid error: {e}")


def cmd_get_system(_msg: dict) -> str:
    try:
        import psutil
        cpu    = psutil.cpu_percent(interval=0.1)
        mem    = psutil.virtual_memory()
        disk   = psutil.disk_usage("C:\\")
        procs  = len(psutil.pids())
        return _ok({
            "cpu_pct":      cpu,
            "mem_used_pct": mem.percent,
            "mem_free_gb":  round(mem.available / 1e9, 2),
            "disk_used_pct": round(disk.percent, 1),
            "disk_free_gb": round(disk.free / 1e9, 1),
            "processes":    procs,
        })
    except ImportError:
        # psutil not installed — return stubs
        return _ok({
            "cpu_pct": 0.0, "mem_used_pct": 0.0, "mem_free_gb": 0.0,
            "disk_used_pct": 0.0, "disk_free_gb": 0.0, "processes": 0,
            "note": "psutil not installed — install with pip for live metrics",
        })
    except Exception as e:
        return _err(f"get_system error: {e}")


_tick_count = 0

def cmd_tick(_msg: dict) -> str:
    global _tick_count
    _tick_count += 1
    # Record environment snapshot
    try:
        import psutil
        cpu  = psutil.cpu_percent(interval=0.0)
        mem  = psutil.virtual_memory().available / 1e9
        procs = len(psutil.pids())
    except Exception:
        cpu, mem, procs = 0.0, 0.0, 0
    try:
        con = _con()
        con.execute(
            "INSERT INTO environment_states(cpu_load,mem_free,active_procs) VALUES (?,?,?)",
            (cpu, mem, procs)
        )
        con.commit()
        con.close()
    except Exception:
        pass
    return _ok({"tick": _tick_count, "cpu": cpu, "mem_free_gb": round(mem, 2)})


def cmd_get_performatives(msg: dict) -> str:
    try:
        limit = int(msg.get("limit", 20))
        con   = _con()
        rows  = con.execute(
            "SELECT id, sentence, script_path, exec_count, description "
            "FROM performatives ORDER BY exec_count DESC LIMIT ?",
            (limit,)
        ).fetchall()
        con.close()
        perfs = [{"id": r[0], "sentence": r[1], "script": r[2],
                  "count": r[3], "desc": r[4]} for r in rows]
        return _ok({"performatives": perfs})
    except Exception as e:
        return _err(f"get_performatives error: {e}")


def cmd_add_performative(msg: dict) -> str:
    sentence = msg.get("sentence", "").strip()
    script   = msg.get("script", "")
    desc     = msg.get("description", "")
    if not sentence:
        return _err("sentence required")
    try:
        con = _con()
        con.execute(
            "INSERT INTO performatives(sentence,script_path,description) VALUES (?,?,?)",
            (sentence, script, desc)
        )
        new_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
        con.commit(); con.close()
        return _ok({"id": new_id, "sentence": sentence})
    except sqlite3.IntegrityError:
        return _err(f"performative already exists: {sentence}")
    except Exception as e:
        return _err(f"add_performative error: {e}")


def cmd_log_transition(msg: dict) -> str:
    from_id = msg.get("from_id")
    to_id   = msg.get("to_id")
    if from_id is None or to_id is None:
        return _err("from_id and to_id required")
    try:
        con = _con()
        con.execute(
            "INSERT INTO markov_transitions(from_id,to_id,edge_count) VALUES (?,?,1) "
            "ON CONFLICT(from_id,to_id) DO UPDATE SET edge_count=edge_count+1",
            (from_id, to_id)
        )
        con.commit(); con.close()
        return _ok({"logged": True, "from": from_id, "to": to_id})
    except Exception as e:
        return _err(f"log_transition error: {e}")


# ── Dispatch ───────────────────────────────────────────────────────────────────

HANDLERS = {
    "status":           cmd_status,
    "get_agents":       cmd_get_agents,
    "get_grid":         cmd_get_grid,
    "get_system":       cmd_get_system,
    "tick":             cmd_tick,
    "get_performatives": cmd_get_performatives,
    "add_performative": cmd_add_performative,
    "log_transition":   cmd_log_transition,
}


def main():
    # Force unbuffered UTF-8 I/O
    sys.stdin  = open(sys.stdin.fileno(),  'r', encoding='utf-8', buffering=1)
    sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', buffering=1)

    _init_db()

    # Signal ready
    sys.stdout.write(_ok({"msg": "sim_backend ready", "version": "1.0",
                           "db": str(DB_PATH)}) + "\n")
    sys.stdout.flush()
    _log("sim_backend started — waiting for commands")

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError as e:
            sys.stdout.write(_err(f"JSON parse error: {e}") + "\n")
            sys.stdout.flush()
            continue

        cmd = msg.get("cmd", "").strip()
        handler = HANDLERS.get(cmd)
        if handler:
            try:
                resp = handler(msg)
            except Exception as e:
                resp = _err(f"handler error: {e}")
        else:
            resp = _err(f"unknown command: {cmd!r}. Valid: {list(HANDLERS)}")

        sys.stdout.write(resp + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
