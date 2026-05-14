package com.simsneo.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Step 55: The WorldGrid
 * A 2D array representing the geometric plane of the city.
 */
public class WorldGrid {
    private final int width;
    private final int height;
    private final Tile[][] grid;

    public WorldGrid(int width, int height) {
        this.width = width;
        this.height = height;
        this.grid = new Tile[width][height];
        initializeGrid();
    }

    private void initializeGrid() {
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                grid[x][y] = new Tile(x, y, Tile.TileType.GRASS);
            }
        }
    }

    public Tile getTile(int x, int y) {
        if (x >= 0 && x < width && y >= 0 && y < height) {
            return grid[x][y];
        }
        return null;
    }

    /**
     * Step 56: Z-Order Indexing
     * Returns tiles sorted back-to-front for correct isometric rendering.
     */
    public List<Tile> getSortedTiles() {
        List<Tile> sorted = new ArrayList<>();
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                sorted.add(grid[x][y]);
            }
        }
        // Depth-sorting: (x + y) determines the order
        sorted.sort((a, b) -> (a.getX() + a.getY()) - (b.getX() + b.getY()));
        return sorted;
    }

    private final List<Wall> walls = new ArrayList<>();
    private final List<GameObject> objects = new ArrayList<>();

    public void addObject(GameObject obj) {
        objects.add(obj);
    }

    public List<GameObject> getObjects() {
        return objects;
    }

    public void addWall(Wall wall) {
        walls.add(wall);
    }

    public List<Wall> getWalls() {
        return walls;
    }
