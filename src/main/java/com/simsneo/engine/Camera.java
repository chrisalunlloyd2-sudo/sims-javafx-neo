package com.simsneo.engine;

/**
 * Step 57: The Camera Class
 * Manages viewport offsets for panning and focal points.
 */
public class Camera {
    private double x;
    private double y;

    public Camera(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public void pan(double dx, double dy) {
        this.x += dx;
        this.y += dy;
    }

    public double getX() { return x; }
    public void setX(double x) { this.x = x; }
    public double getY() { return y; }
    public void setY(double y) { this.y = y; }
}
