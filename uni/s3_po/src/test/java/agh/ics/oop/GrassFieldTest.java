package agh.ics.oop;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class GrassFieldTest {
    @Test
    void testGrassFieldCanMoveTo() {
        IWorldMap map = new GrassField(10);

        assertTrue(map.canMoveTo(new Vector2d(0, 0)));
        assertTrue(map.canMoveTo(new Vector2d(5, 3)));
        assertTrue(map.canMoveTo(new Vector2d(9, 9)));

        assertTrue(map.canMoveTo(new Vector2d(-1, 0)));
        assertTrue(map.canMoveTo(new Vector2d(0, -2)));
        assertTrue(map.canMoveTo(new Vector2d(-62, -100)));

        assertTrue(map.canMoveTo(new Vector2d(10, 9)));
        assertTrue(map.canMoveTo(new Vector2d(8, 15)));
        assertTrue(map.canMoveTo(new Vector2d(200, 200000)));

        assertTrue(map.canMoveTo(new Vector2d(5, 5)));
        assertTrue(map.place(new Animal(map, new Vector2d(5, 5))));
        assertFalse(map.canMoveTo(new Vector2d(5, 5)));
    }

    @Test
    void testGrassFieldPlace() {
        IWorldMap map = new GrassField(4);

        assertTrue(map.place(new Animal(map)));
        assertTrue(map.place(new Animal(map, new Vector2d(1, 1))));

        assertTrue(map.place(new Animal(map, new Vector2d(-100, -2))));
        assertTrue(map.place(new Animal(map, new Vector2d(2, 100000))));
        assertTrue(map.place(new Animal(map, new Vector2d(13, 1))));

        Exception e = assertThrows(IllegalArgumentException.class, 
            () -> map.place(new Animal(map, new Vector2d(2, 2))));
        assertTrue(e.getMessage().equals(String.format("Unable to place animal at position %s",
            new Vector2d(2, 2).toString())));

        e = assertThrows(IllegalArgumentException.class, 
            () -> map.place(new Animal(map, new Vector2d(1, 1))));
        assertTrue(e.getMessage().equals(String.format("Unable to place animal at position %s",
            new Vector2d(1, 1).toString())));
    }

    @Test
    void testGrassFieldIsOccupied() {
        IWorldMap map = new GrassField(6);

        assertTrue(map.place(new Animal(map, new Vector2d(3, 3))));
        assertTrue(map.place(new Animal(map, new Vector2d(3, 9))));

        if (map.isOccupied(new Vector2d(0, 0))) {
            assertTrue(map.objectAt(new Vector2d(0, 0)) instanceof Grass);
        }
        assertFalse(map.isOccupied(new Vector2d(20, 5)));
        assertFalse(map.isOccupied(new Vector2d(-5, 20000)));

        assertTrue(map.isOccupied(new Vector2d(3, 3)));
        assertTrue(map.isOccupied(new Vector2d(3, 9)));
    }

    @Test
    void testGrassFieldObjectAt() {
        IWorldMap map = new GrassField(10);

        Object o = map.objectAt(new Vector2d(0, 0));
        assertTrue(o == null || o instanceof Grass);

        assertNull(map.objectAt(new Vector2d(-50, 200000)));
        assertNull(map.objectAt(new Vector2d(40, 20)));

        Animal a = new Animal(map, new Vector2d(5, 6));
        assertTrue(map.place(a));
        assertTrue(map.objectAt(new Vector2d(5, 6)) == a);
    }
}
