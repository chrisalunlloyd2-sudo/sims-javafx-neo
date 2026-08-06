# sims-javafx-neo

> sim_backend.py — Persistent Python simulation backend for sims-javafx-neo.

*Auto-generated 2026-08-05 18:39 from source — branch `main`, 21 Python modules, 40 other files.*

## Architecture

```
  .director_payload.md
  .gitignore
  ASCII_PROJECT_MAP.txt
  Blueprint.md
  CHANGELOG.md
  JAVAFX_NEO_1700_STEP_PLAN.md
  PROJECT_LOG.md
  README.md
  ROADMAP.md
  TASKS.md
  pom.xml
  sprite_package.zip
  docs/
    OPERATIONAL_RUNBOOK.md
    SYSTEMS_ARCHITECTURE.md
  sprite_core/
    autonomous_controller.py
    behavioral_engine.py
    discovery.py
    final_orchestrator.py
    grid_manager.py
    grid_protocol.py
    hardware_id.py
    init_db.py
    init_hooks.py
    interceptor.py
    interpreter.py
    learning_engine.py
    context_fence/
      memory_discovery_sprite.json
      memory_maintenance_sprite.json
      memory_security_sprite.json
      db/
        sprite.db
    scripts/
      heartbeat.py
      purge.py
      sweep.py
  src/
    main/
      java/
        module-info.java
```

## Dependencies

External packages imported by this project:

`getpass`, `psutil`

## How to run

Executable entry points (have a `__main__` block):

- `python sprite_core/autonomous_controller.py`
- `python sprite_core/behavioral_engine.py`
- `python sprite_core/discovery.py`
- `python sprite_core/final_orchestrator.py`
- `python sprite_core/grid_manager.py`
- `python sprite_core/grid_protocol.py`
- `python sprite_core/hardware_id.py`
- `python sprite_core/init_db.py`
- `python sprite_core/init_hooks.py`
- `python sprite_core/interceptor.py`
- `python sprite_core/interpreter.py`
- `python sprite_core/learning_engine.py`

## Modules

### `sprite_core/autonomous_controller.py`

- **class `AutonomousController`**
  - methods: `check_environment_and_act`, `execute_autonomous_action`, `self_modify`

### `sprite_core/behavioral_engine.py`

- **class `BehavioralEngine`**
  - methods: `get_execution_priority`
- **class `IACProtocol`** — Step 805: Inter-Agent Communication
  - methods: `send_handover`

### `sprite_core/discovery.py`

- **class `DiscoveryModule`**
  - methods: `sweep`

### `sprite_core/final_orchestrator.py`

- **class `FinalOrchestrator`** — Step 1403: Deploy the 'Final Orchestrator'
  - methods: `run_stress_test`, `boot`

### `sprite_core/grid_manager.py`

- **class `GridManager`** — Step 1102: Remote Agent Deployment & Step 1103: Global State Ledger
  - methods: `grid_callback`, `run_heartbeat_loop`, `start`, `deploy_to_remote`

### `sprite_core/grid_protocol.py`

- **class `GridProtocol`** — Step 1101: Define the 'Grid Protocol'
  - methods: `start_server`, `handle_client`, `send_message`

### `sprite_core/hardware_id.py`

- `get_hardware_uuid()` — Step 1001: Implement 'Real-World Anchoring'

### `sprite_core/init_db.py`

- `init_db()`

### `sprite_core/init_hooks.py`

- `inject_startup_hook()` — Step 755: Inject Deep Init Hooks (Windows Startup Folder)

### `sprite_core/interceptor.py`

- `resolve_aliases(ids)` — Step 702: Resolve aliases in the input sequence
- `execute_by_id(p_id, headless)`
- `process_input(user_input, headless)`
- `fallback_nlp(text)`

### `sprite_core/interpreter.py`

- **class `PerformativeInterpreter`**
  - methods: `translate`, `allocate_new`

### `sprite_core/learning_engine.py`

- **class `LearningEngine`**
  - methods: `is_relevant`, `record_transition`, `update_probabilities`, `get_prediction`, `check_for_aliases`

### `sprite_core/monitor.py`

- `get_system_metrics()`
- `log_metrics()`

### `sprite_core/orchestrator.py`

- **class `KernelOrchestrator`**
  - methods: `run_command`, `kill_process`, `list_active`

### `sprite_core/profile_manager.py`

- **class `OpenClawProfileManager`**
  - methods: `generate_full_profile`

### `sprite_core/sim_backend.py`

sim_backend.py — Persistent Python simulation backend for sims-javafx-neo.

- `cmd_status(_msg)`
- `cmd_get_agents(_msg)`
- `cmd_get_grid(_msg)`
- `cmd_get_system(_msg)`
- `cmd_tick(_msg)`
- `cmd_get_performatives(msg)`
- `cmd_add_performative(msg)`
- `cmd_log_transition(msg)`
- `main()`

### `sprite_core/simulation_orchestrator.py`

- **class `LivingSimulationOrchestrator`** — Step 1003 & 1105: Finalize the 'Living Simulation' Orchestrator with Grid Support
  - methods: `start_simulation`, `update_trust_scores`, `stop_simulation`

### `sprite_core/sprite_watchdog.py`

- `is_process_running(name)`
- `maintain_persistence()`

## Public API index

| Module | Function | Signature |
|--------|----------|-----------|
| `hardware_id` | `get_hardware_uuid` | `get_hardware_uuid()` |
| `init_db` | `init_db` | `init_db()` |
| `init_hooks` | `inject_startup_hook` | `inject_startup_hook()` |
| `interceptor` | `execute_by_id` | `execute_by_id(p_id, headless)` |
| `interceptor` | `fallback_nlp` | `fallback_nlp(text)` |
| `interceptor` | `process_input` | `process_input(user_input, headless)` |
| `interceptor` | `resolve_aliases` | `resolve_aliases(ids)` |
| `monitor` | `get_system_metrics` | `get_system_metrics()` |
| `monitor` | `log_metrics` | `log_metrics()` |
| `sim_backend` | `cmd_add_performative` | `cmd_add_performative(msg)` |
| `sim_backend` | `cmd_get_agents` | `cmd_get_agents(_msg)` |
| `sim_backend` | `cmd_get_grid` | `cmd_get_grid(_msg)` |
| `sim_backend` | `cmd_get_performatives` | `cmd_get_performatives(msg)` |
| `sim_backend` | `cmd_get_system` | `cmd_get_system(_msg)` |
| `sim_backend` | `cmd_log_transition` | `cmd_log_transition(msg)` |
| `sim_backend` | `cmd_status` | `cmd_status(_msg)` |
| `sim_backend` | `cmd_tick` | `cmd_tick(_msg)` |
| `sim_backend` | `main` | `main()` |
| `sprite_watchdog` | `is_process_running` | `is_process_running(name)` |
| `sprite_watchdog` | `maintain_persistence` | `maintain_persistence()` |

## Status

- Branch: `main`
- Last commit: 2026-08-05 18:30:07 -0600
- File types: .java ×22, .md ×10, .json ×3, .txt ×1, .xml ×1, .zip ×1, .log ×1, .db ×1

### Recent commits
```
c5ea2b9 docs: auto-update [skip-docs]
b76658c docs: auto-update [skip-docs]
fcc23e0 docs: auto-update [skip-docs]
c2ab9a9 docs: auto-update [skip-docs]
53519c8 docs: auto-update [skip-docs]
4e7e747 docs: auto-update [skip-docs]
ae4b4e9 docs: auto-update [skip-docs]
aad0afd docs: auto-update [skip-docs]
```

---
*README generated by `readme_generator.py` (Viper). Deterministic — derived from source, not LLM prose.*