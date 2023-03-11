package agh.ics.oop;

import java.util.Vector;

public class SimulationEngine implements IEngine, Runnable {
    private final IWorldMap map;
    private final Animal[] animals;
    private final int moveDelay;
    private MoveDirection[] mvDirs;
    private Vector<IPositionChangeObserver> observers = new Vector<IPositionChangeObserver>();

    public SimulationEngine(MoveDirection[] mvDirs, IWorldMap map, Vector2d[] initialPositions, int moveDelay) {
        this.map = map;
        this.mvDirs = mvDirs;

        Vector<Animal> v = new Vector<Animal>();
        for (Vector2d pos : initialPositions) {
            Animal a = new Animal(this.map, pos);
            if (this.map.place(a)) {
                v.add(a);
            }
        }
        this.animals = v.toArray(new Animal[v.size()]);
        this.moveDelay = moveDelay;
    }

    public SimulationEngine(MoveDirection[] mvDirs, IWorldMap map, Vector2d[] initialPositions) {
        this(mvDirs, map, initialPositions, 0);
    }

    public SimulationEngine(IWorldMap map, Vector2d[] initialPositions, int moveDelay) {
        this(null, map, initialPositions, moveDelay);
    }

    @Override
    public void run() {
        int animIndex = 0;
        for (MoveDirection mvDir : mvDirs) {
            try {
                Thread.sleep(moveDelay);
            } catch (InterruptedException e) {
                System.out.println("Simulation interrupted.");
            }
            Vector2d oldPos = animals[animIndex].getPosition();
            animals[animIndex].move(mvDir);
            Vector2d newPos = animals[animIndex].getPosition();
            notifyPositionChanged(oldPos, newPos);
            System.out.println(String.format("ANIMAL %d: %s\n%s", animIndex, mvDir, map));
            if (++animIndex == animals.length) {
                animIndex = 0;
            }
        }
    }

    public void setDirections(MoveDirection[] directions) {
        mvDirs = directions;
    }

    public void addObserver(IPositionChangeObserver observer) {
        observers.add(observer);
    }

    public void removeObserver(IPositionChangeObserver observer) {
        for (IPositionChangeObserver o : observers) {
            if (o == observer) {
                observers.remove(o);
            }
        }
    }

    private void notifyPositionChanged(Vector2d oldPos, Vector2d newPos) {
        for (IPositionChangeObserver o : observers) {
            o.positionChanged(oldPos, newPos);
        }
    }
}
