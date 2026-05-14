package com.simsneo.engine;

import com.simsneo.model.Sim;
import com.simsneo.model.Wall;
import com.simsneo.model.Furniture;
import com.simsneo.model.WorldGrid;
import com.simsneo.view.WorldRenderer;
import com.simsneo.view.HUD;
import javafx.animation.AnimationTimer;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;

public class GameLoop extends AnimationTimer {

    public static GameLoop instance;
    private GraphicsContext gc;
    private HUD hud;
    private long lastUpdate = 0;
    private WorldGrid world;
    private WorldRenderer renderer;
    private GameClock clock;
    private CareerSystem careers;
    private EventDispatcher events;

    private int lastProcessedHour = -1;

    public GameLoop(GraphicsContext gc, HUD hud) {
        instance = this;
        this.gc = gc;
        this.hud = hud;
        this.world = new WorldGrid(20, 20);
        this.renderer = new WorldRenderer(world);
        this.clock = new GameClock();
        this.careers = new CareerSystem();
        this.events = new EventDispatcher();
        
        // Step 101: Define Sims
        Sim sim = new Sim("SimNeo_01", 5, 5);
        this.world.addSim(sim);
        this.careers.assignJob(sim, CareerSystem.JobLevel.JUNIOR_CODER);

        // Step 151: Construction
        this.world.addWall(new Wall(5, 5, true));
        this.world.addWall(new Wall(5, 5, false));

        // Step 201: Objects
        this.world.addObject(new Furniture("Fridge", 5, 5, 1, 1, 0, 1, 600.0, "#ffffff"));
    }

    @Override
    public void handle(long now) {
        if (lastUpdate == 0) {
            lastUpdate = now;
            return;
        }
        
        double deltaSeconds = (now - lastUpdate) / 1_000_000_000.0;
        
        // Step 251-300: Time Orchestration
        clock.update(deltaSeconds);
        
        // Hourly Triggers
        int currentHour = clock.getHour();
        if (currentHour != lastProcessedHour) {
            for (Sim s : world.getSims()) {
                careers.checkCarpool(s, currentHour);
            }
            events.checkRandomEvents(world, currentHour);
            lastProcessedHour = currentHour;
        }

        // Step 103: Update Agent Nervous System
        for (Sim sim : world.getSims()) {
            sim.updateMotives(deltaSeconds * clock.getSpeed());
        }

        // Step 351: Recursive Hardening
        SystemIntegrity.validateSimInteractions(world);

        renderer.render(gc);

        
        // UI Dashboard (Step 301-350)
        hud.update(clock, world.getSims().get(0));

        lastUpdate = now;
    }

    public void setSpeed(double s) {
        clock.setSpeed(s);
    }
}
