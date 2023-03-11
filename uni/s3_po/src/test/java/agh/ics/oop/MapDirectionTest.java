package agh.ics.oop;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

public class MapDirectionTest {
    private static final MapDirection[] mapDirs = {MapDirection.NORTH, MapDirection.EAST, MapDirection.SOUTH, MapDirection.WEST};

    @Test
    void testMapDirectionNext() {
        MapDirection[] nextMapDirs = {MapDirection.EAST, MapDirection.SOUTH, MapDirection.WEST, MapDirection.NORTH};
        for (int i = 0; i < 4; ++i) {
            assertEquals(mapDirs[i].next(), nextMapDirs[i]);
        }
    }

    @Test
    void testMapDirectionPrevious() {
        MapDirection[] prevMapDirs = {MapDirection.WEST, MapDirection.NORTH, MapDirection.EAST, MapDirection.SOUTH};
        for (int i = 0; i < 4; ++i) {
            assertEquals(mapDirs[i].previous(), prevMapDirs[i]);
        }
    }
}
