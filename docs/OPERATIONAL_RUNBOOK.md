# OPERATIONAL RUNBOOK: Setup & Build
**Platform:** Java 17+ / Maven 3.9+
**OS:** Windows 10/11 (Optimized for Deep Registry & DePIN)

---

## 1. Environment Synchronization
1. **Ollama:** Ensure `ollama serve` is active and `h2o-danube3:4b` is pulled.
2. **JAVA_HOME:** Point to JDK 17 installation.
3. **Maven:** Ensure `mvn` is in the system PATH.

## 2. Build Commands
```powershell
# Clean and compile the JavaFX Neo engine
mvn clean compile

# Run the simulation
mvn javafx:run
```

## 3. Maintenance Protocols
- **Update DNA:** To modify agent behaviors, update the `Sim.java` motives decay rates.
- **Z-Order Buffer:** If layering artifacts appear, check `WorldRenderer.java` sorting logic.
- **PII Scrubbing:** Always run the Entropy Scan before committing to public repositories.

---
*Status: READY FOR GENESIS*
