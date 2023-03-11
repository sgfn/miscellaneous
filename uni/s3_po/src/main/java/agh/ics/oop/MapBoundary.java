package agh.ics.oop;

import java.util.Comparator;
import java.util.SortedSet;
import java.util.TreeSet;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class MapBoundary implements IPositionChangeObserver {
    private SortedSet<PosTypeEntry> positionsX;
    private SortedSet<PosTypeEntry> positionsY;

    private static final class PosTypeEntry {
        private final Vector2d pos;
        private final Class<?> type;

        public PosTypeEntry(Vector2d p, Class<?> t) {
            pos = p; type = t;
        }

        public PosTypeEntry(IMapElement elem) {
            pos = elem.getPosition();
            type = elem.getClass();
        }
    }

    private final Comparator<PosTypeEntry> genericComparator(Method compareFirst, Method compareSecond) {
        return new Comparator<PosTypeEntry>() {
            public final int compare(PosTypeEntry first, PosTypeEntry second) {
                try {
                    int res = (int)(compareFirst.invoke(first.pos, second.pos));
                    if (res == 0) {
                        res = (int)(compareSecond.invoke(first.pos, second.pos));
                    }
                    if (res == 0) {
                        if (first.type.equals(Animal.class)) {
                            res = (second.type.equals(Animal.class)) ? 0 : -1;
                        } else {
                            res = (second.type.equals(Animal.class)) ? 1 : 0;
                        }
                    }
                    return res;
                } catch (IllegalAccessException e) {
                    throw new RuntimeException();
                } catch (InvocationTargetException e) {
                    throw new RuntimeException();
                }
            }
        };
    }

    private boolean hasPosTypeEntry(PosTypeEntry e) {
        return positionsX.contains(e);
    }

    private void addPosTypeEntry(PosTypeEntry e) {
        positionsX.add(e);
        positionsY.add(e);
    }

    private void removePosTypeEntry(PosTypeEntry e) {
        positionsX.remove(e);
        positionsY.remove(e);
    }

    public MapBoundary() {
        Method v2dMethodX;
        Method v2dMethodY;
        try {
            v2dMethodX = Vector2d.class.getMethod("compareAlongXaxis", new Class[] {Vector2d.class});
            v2dMethodY = Vector2d.class.getMethod("compareAlongYaxis", new Class[] {Vector2d.class});
        } catch (NoSuchMethodException e) {
            throw new RuntimeException();
        }

        positionsX = new TreeSet<PosTypeEntry>(genericComparator(v2dMethodX, v2dMethodY));
        positionsY = new TreeSet<PosTypeEntry>(genericComparator(v2dMethodY, v2dMethodX));
    }

    @Override
    public void positionChanged(Vector2d oldPosition, Vector2d newPosition) {
        PosTypeEntry tryEntry = new PosTypeEntry(oldPosition, Animal.class);
        if (hasPosTypeEntry(tryEntry)) {
            removePosTypeEntry(tryEntry);
            addPosTypeEntry(new PosTypeEntry(newPosition, Animal.class));

            // usuń trawę (na wszelki wypadek), jeśli zwierzę z niej zeszło/na nią weszło
            removePosTypeEntry(new PosTypeEntry(oldPosition, Grass.class));
            removePosTypeEntry(new PosTypeEntry(newPosition, Grass.class));
        }
        // trawa nie ma nóg
    }

    public void placeElem(IMapElement elem) {
        addPosTypeEntry(new PosTypeEntry(elem));
    }

    public Vector2d[] getEntityBounds() {
        if (positionsX.isEmpty()) {
            return new Vector2d[] {new Vector2d(0, 0), new Vector2d(0, 0)};
        } else {
            return new Vector2d[] {
                positionsX.first().pos.lowerLeft(positionsY.first().pos),
                positionsX.last().pos.upperRight(positionsY.last().pos)
            };
        }
    }
}
