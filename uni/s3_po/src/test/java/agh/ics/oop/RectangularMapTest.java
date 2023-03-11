package agh.ics.oop;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class RectangularMapTest {
    @Test
    void testRectangularMapCanMoveTo() {
        IWorldMap map = new RectangularMap(10, 10);

        assertTrue(map.canMoveTo(new Vector2d(0, 0)));
        assertTrue(map.canMoveTo(new Vector2d(5, 3)));
        assertTrue(map.canMoveTo(new Vector2d(9, 9)));

        assertFalse(map.canMoveTo(new Vector2d(-1, 0)));
        assertFalse(map.canMoveTo(new Vector2d(0, -2)));
        assertFalse(map.canMoveTo(new Vector2d(-62, -100)));

        assertFalse(map.canMoveTo(new Vector2d(10, 9)));
        assertFalse(map.canMoveTo(new Vector2d(8, 15)));
        assertFalse(map.canMoveTo(new Vector2d(200, 200000)));

        assertTrue(map.canMoveTo(new Vector2d(5, 5)));
        assertTrue(map.place(new Animal(map, new Vector2d(5, 5))));
        assertFalse(map.canMoveTo(new Vector2d(5, 5)));
    }

    @Test
    void testRectangularMapPlace() {
        IWorldMap map = new RectangularMap(4, 7);

        assertTrue(map.place(new Animal(map)));
        assertTrue(map.place(new Animal(map, new Vector2d(1, 1))));

        final Vector2d[] illegals = new Vector2d[] {
            new Vector2d(-100, -2), new Vector2d(2, 100000), new Vector2d(13, 1),
            new Vector2d(2, 2), new Vector2d(1, 1)
        };

        for (Vector2d illegal : illegals) {
            Exception e = assertThrows(IllegalArgumentException.class, 
                () -> map.place(new Animal(map, illegal)));
            assertTrue(e.getMessage().equals(String.format("Unable to place animal at position %s",
                illegal.toString())));
        }
    }

    @Test
    void testRectangularMapIsOccupied() {
        IWorldMap map = new RectangularMap(5, 12);

        assertTrue(map.place(new Animal(map, new Vector2d(3, 3))));
        assertTrue(map.place(new Animal(map, new Vector2d(3, 9))));

        assertFalse(map.isOccupied(new Vector2d(0, 0)));
        assertFalse(map.isOccupied(new Vector2d(3, 5)));
        assertFalse(map.isOccupied(new Vector2d(-5, 20000)));

        assertTrue(map.isOccupied(new Vector2d(3, 3)));
        assertTrue(map.isOccupied(new Vector2d(3, 9)));
    }

    @Test
    void testRectangularMapObjectAt() {
        IWorldMap map = new RectangularMap(50, 100);

        assertNull(map.objectAt(new Vector2d(0, 0)));
        assertNull(map.objectAt(new Vector2d(-50, 200000)));
        assertNull(map.objectAt(new Vector2d(40, 20)));

        Animal a = new Animal(map, new Vector2d(5, 6));
        assertTrue(map.place(a));
        assertTrue(map.objectAt(new Vector2d(5, 6)) == a);
    }
}
