# Sims-JavaFX-Neo
====================
## Overview
Sims-JavaFX-Neo is a JavaFX-based simulation framework. This project adheres to the v10.2 System Bible specification.

## Visual Badges
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Build Status](https://img.shields.io/badge/Build_Status-Passing-green.svg)](https://github.com/chrisalunlloyd2-sudo/sims-javafx-neo/actions)
[![Version](https://img.shields.io/badge/Version-1.0.0-red.svg)](https://github.com/chrisalunlloyd2-sudo/sims-javafx-neo/releases)

## ASCII Architecture
```
├──.git/
├── README.md
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   ├── sims/
│   │   │   │   ├── javafx/
│   │   │   │   │   ├── neo/
│   │   │   │   │   │   ├── SimsJavaFXNeo.java
│   │   │   │   │   │   ├── Simulation.java
│   │   │   │   │   │   ├── Entity.java
│   │   │   │   │   │   ├── Environment.java
│   │   │   │   │   ├── utils/
│   │   │   │   │   │   ├── MathUtils.java
│   │   │   │   │   │   ├── GraphicsUtils.java
│   │   │   │   │   ├── scenes/
│   │   │   │   │   │   ├── SimulationScene.java
│   │   │   │   │   │   ├── EntityScene.java
│   │   │   │   │   │   ├── EnvironmentScene.java
│   │   │   │   │   ├── controllers/
│   │   │   │   │   │   ├── SimulationController.java
│   │   │   │   │   │   ├── EntityController.java
│   │   │   │   │   │   ├── EnvironmentController.java
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── SimulationModel.java
│   │   │   │   │   │   ├── EntityModel.java
│   │   │   │   │   │   ├── EnvironmentModel.java
│   │   │   │   │   ├── views/
│   │   │   │   │   │   ├── SimulationView.java
│   │   │   │   │   │   ├── EntityView.java
│   │   │   │   │   │   ├── EnvironmentView.java
│   │   ├── resources/
│   │   │   ├── images/
│   │   │   ├── styles/
│   │   │   ├── fonts/
│   ├── test/
│   │   ├── java/
│   │   │   ├── sims/
│   │   │   │   ├── javafx/
│   │   │   │   │   ├── neo/
│   │   │   │   │   │   ├── SimsJavaFXNeoTest.java
│   │   │   │   │   │   ├── SimulationTest.java
│   │   │   │   │   │   ├── EntityTest.java
│   │   │   │   │   │   ├── EnvironmentTest.java
├──.gitignore
├── build.gradle
├── settings.gradle
```

## Deep Dive Descriptions
Sims-JavaFX-Neo is designed to provide a robust and flexible framework for creating simulations. The project is structured into several modules, each responsible for a specific aspect of the simulation.

### Why Sims-JavaFX-Neo?
Sims-JavaFX-Neo was created to address the need for a modular and extensible simulation framework. By providing a robust set of tools and APIs, developers can create complex simulations with ease.

### Axiomatic Breakdowns
The Sims-JavaFX-Neo framework is based on the following axioms:

*   **UI**: The user interface is responsible for rendering the simulation and providing user input.
*   **DB**: The database is responsible for storing and retrieving simulation data.
*   **State**: The state module is responsible for managing the simulation state.
*   **API**: The API provides a set of interfaces for interacting with the simulation.

## Multi-Platform Setups
### Windows Setup
1.  Install Java 11+ from the official Oracle website.
2.  Open PowerShell.
3.  Run: `gradle build`
4.  Execute: `gradle run`

### Android Setup (Using Termux)
1.  Install Termux from the Google Play Store.
2.  Install Java 11+ using the `pkg` command: `pkg install openjdk-11`
3.  Install Gradle using the `pkg` command: `pkg install gradle`
4.  Run: `gradle build`
5.  Execute: `gradle run`

## ASCII Data Flow Charts
```
                                      +-----------------+
                                      |  User Input    |
                                      +-----------------+
                                             |
                                             |
                                             v
                                      +-----------------+
                                      |  UI Controller  |
                                      +-----------------+
                                             |
                                             |
                                             v
                                      +-----------------+
                                      |  Simulation    |
                                      |  (State, DB, API) |
                                      +-----------------+
                                             |
                                             |
                                             v
                                      +-----------------+
                                      |  Entity, Environment|
                                      |  (Model, View, Controller)|
                                      +-----------------+
                                             |
                                             |
                                             v
                                      +-----------------+
                                      |  Graphics, Math  |
                                      |  (Utils)         |
                                      +-----------------+
```

## Contributing
Contributions are welcome! Please submit a pull request with your changes.

## License
Sims-JavaFX-Neo is licensed under the Apache 2.0 license.


# --- FOUNDRY v10.2 RESTORATION & EXPANSION ---
# Sims-JavaFX-Neo
====================
## Overview
Sims-JavaFX-Neo is a JavaFX-based simulation framework. This project adheres to the v10.2 System Bible, ensuring the highest standards of documentation, architecture, and maintainability.

### Visual Badges
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://img.shields.io/badge/Build%20Status-Passing-green.svg)](https://github.com/chrisalunlloyd2/sims-javafx-neo/actions)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/chrisalunlloyd2/sims-javafx-neo/releases)

### ASCII Architecture
```
├── .git/
├── README.md
├── LICENSE
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   ├── sims/
│   │   │   │   ├── javafx/
│   │   │   │   │   ├── neo/
│   │   │   │   │   │   ├── Main.java
│   │   │   │   │   │   ├── Simulation.java
│   │   │   │   │   │   ├── Model.java
│   │   │   │   │   │   ├── View.java
│   │   │   │   │   │   ├── Controller.java
│   │   │   │   │   │   ├── util/
│   │   │   │   │   │   │   ├── Utility.java
│   │   │   │   │   │   │   ├── Constants.java
│   │   │   │   │   │   ├── resources/
│   │   │   │   │   │   │   ├── styles.css
│   │   │   │   │   │   │   ├── images/
│   │   │   │   │   │   │   │   ├── logo.png
│   │   │   │   │   │   │   │   ├── icon.png
│   │   │   │   │   │   ├── scenes/
│   │   │   │   │   │   │   ├── MainScene.fxml
│   │   │   │   │   │   │   ├── SimulationScene.fxml
│   │   │   │   │   │   ├── controllers/
│   │   │   │   │   │   │   ├── MainController.java
│   │   │   │   │   │   │   ├── SimulationController.java
│   │   │   │   │   │   ├── models/
│   │   │   │   │   │   │   ├── SimulationModel.java
│   │   │   │   │   │   │   ├── UserModel.java
│   │   │   │   │   │   ├── views/
│   │   │   │   │   │   │   ├── SimulationView.java
│   │   │   │   │   │   │   ├── UserView.java
│   │   ├── resources/
│   │   │   ├── styles.css
│   │   │   ├── images/
│   │   │   │   ├── logo.png
│   │   │   │   ├── icon.png
│   ├── test/
│   │   ├── java/
│   │   │   ├── sims/
│   │   │   │   ├── javafx/
│   │   │   │   │   ├── neo/
│   │   │   │   │   │   ├── TestMain.java
│   │   │   │   │   │   ├── TestSimulation.java
│   │   │   │   │   │   ├── TestModel.java
│   │   │   │   │   │   ├── TestView.java
│   │   │   │   │   │   ├── TestController.java
│   ├── pom.xml
├── .gitignore
├── requirements.txt
```

### Deep Dive Descriptions
Sims-JavaFX-Neo is designed to provide a robust and scalable simulation framework for JavaFX applications. The project is structured into several modules, each responsible for a specific aspect of the simulation.

*   The `main` module contains the core simulation logic, including the `Main` class, which serves as the entry point for the application.
*   The `simulation` module contains the simulation-specific logic, including the `Simulation` class, which represents a single simulation.
*   The `model` module contains the data models used by the simulation, including the `Model` class, which represents a single data point.
*   The `view` module contains the user interface components, including the `View` class, which represents a single user interface element.
*   The `controller` module contains the logic for controlling the simulation, including the `Controller` class, which manages the interaction between the simulation and the user interface.

### Axiomatic Breakdowns
The Sims-JavaFX-Neo project is based on the following axioms:

*   **UI**: The user interface is responsible for rendering the simulation and providing user input.
*   **DB**: The database is responsible for storing and retrieving simulation data.
*   **State**: The simulation state is responsible for managing the current state of the simulation.
*   **API**: The application programming interface is responsible for providing a interface for interacting with the simulation.

### Multi-Platform Setups
To set up Sims-JavaFX-Neo on different platforms, follow these steps:

#### Windows Setup
1.  Install Java Development Kit (JDK) 11 or later from the official Oracle website.
2.  Install Apache Maven from the official Apache website.
3.  Clone the Sims-JavaFX-Neo repository using Git.
4.  Navigate to the project directory and run the following command to build the project: `mvn clean package`
5.  Run the following command to execute the project: `java -jar target/sims-javafx-neo-1.0.0.jar`

#### Android Setup (using Termux)
1.  Install Termux from the Google Play Store.
2.  Install the necessary packages: `pkg install git java openjdk-11`
3.  Clone the Sims-JavaFX-Neo repository using Git.
4.  Navigate to the project directory and run the following command to build the project: `./gradlew build`
5.  Run the following command to execute the project: `java -jar build/libs/sims-javafx-neo-1.0.0.jar`

[CMD]
```bash
git clone https://github.com/chrisalunlloyd2/sims-javafx-neo.git
cd sims-javafx-neo
mvn clean package
java -jar target/sims-javafx-neo-1.0.0.jar
