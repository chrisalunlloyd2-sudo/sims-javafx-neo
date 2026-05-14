package com.simsneo;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.layout.BorderPane;
import com.simsneo.view.HUD;
import javafx.scene.input.KeyEvent;

public class MainApp extends Application {

    public static final int WINDOW_WIDTH = 1024;
    public static final int WINDOW_HEIGHT = 768;

    @Override
    public void start(Stage primaryStage) {
        BorderPane root = new BorderPane();

        Canvas canvas = new Canvas(WINDOW_WIDTH, WINDOW_HEIGHT - 150);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        HUD hud = new HUD();

        root.setCenter(canvas);
        root.setBottom(hud);

        Scene scene = new Scene(root, WINDOW_WIDTH, WINDOW_HEIGHT);

        // Step 304: Keyboard Master Hotkeys
        scene.addEventHandler(KeyEvent.KEY_PRESSED, (key) -> {
            switch(key.getCode()) {
                case DIGIT1: GameLoop.instance.setSpeed(1.0); break;
                case DIGIT2: GameLoop.instance.setSpeed(2.0); break;
                case DIGIT3: GameLoop.instance.setSpeed(3.0); break;
                case P: GameLoop.instance.setSpeed(0.0); break; // Pause
            }
        });

        primaryStage.setTitle("Sims JavaFX Neo - 1700-Step Expansion");
        primaryStage.setScene(scene);
        primaryStage.show();

        GameLoop gameLoop = new GameLoop(gc, hud);
        gameLoop.start();
    }


    public static void main(String[] args) {
        launch(args);
    }
}
