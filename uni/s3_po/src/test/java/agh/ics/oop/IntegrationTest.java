package agh.ics.oop;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;

import org.junit.jupiter.api.Test;

public class IntegrationTest {
    private static class AnimalData {
        final Vector2d position;
        final MapDirection orientation;
        AnimalData(Vector2d p, MapDirection o) {
            position = p; orientation = o;
        }
    }
    private static class SimpleSimulEngTestData {
        final String[] args;
        final MoveDirection[] moves;
        final Vector2d finalPosition;
        final MapDirection finalOrientation;
        final int invalidArgIndex;
        final int invalidAnimalIndex;
        SimpleSimulEngTestData(String[] a, MoveDirection[] m, Vector2d p, MapDirection o, int i, int j) {
            args = a; moves = m; finalPosition = p; finalOrientation = o; invalidArgIndex = i; invalidAnimalIndex = j;
        }
        SimpleSimulEngTestData(String[] a, MoveDirection[] m, Vector2d p, MapDirection o) {
            args = a; moves = m; finalPosition = p; finalOrientation = o; invalidArgIndex = -1; invalidAnimalIndex = -1;
        }
    }

    private static class SimulEngTestData {
        final Vector2d mapDimensions;
        final String[] args;
        final MoveDirection[] moves;
        final Vector2d[] initialPositions;
        final AnimalData[] animData;
        final int invalidArgIndex;
        final int invalidAnimalIndex;
        SimulEngTestData(Vector2d dims, String[] a, MoveDirection[] m, Vector2d[] pos, AnimalData[] data, int i, int j) {
            mapDimensions = dims; args = a; moves = m; initialPositions = pos; animData = data; invalidArgIndex = i; invalidAnimalIndex = j;
        }
        SimulEngTestData(Vector2d dims, String[] a, MoveDirection[] m, Vector2d[] pos, AnimalData[] data) {
            mapDimensions = dims; args = a; moves = m; initialPositions = pos; animData = data; invalidArgIndex = -1; invalidAnimalIndex = -1;
        }
        SimulEngTestData(SimpleSimulEngTestData td) {
            mapDimensions = new Vector2d(5, 5);
            args = td.args;
            moves = td.moves;
            initialPositions = new Vector2d[] {new Vector2d(2, 2)};
            animData = new AnimalData[] {
                new AnimalData(td.finalPosition, td.finalOrientation)
            };
            invalidArgIndex = td.invalidArgIndex;
            invalidAnimalIndex = td.invalidAnimalIndex;
        }
    }

    private static void runTestOnSimulEng(SimulEngTestData td) {
        IWorldMap map = new RectangularMap(td.mapDimensions.x, td.mapDimensions.y);

        if (td.invalidArgIndex >= 0) {
            Exception e = assertThrows(IllegalArgumentException.class, 
                () -> OptionsParser.parse(td.args));
            assertTrue(e.getMessage().equals(String.format("Invalid move: `%s'", td.args[td.invalidArgIndex])));
            return;
        }
        MoveDirection[] moves = OptionsParser.parse(td.args);
        assertTrue(Arrays.equals(moves, td.moves));

        if (td.invalidAnimalIndex >= 0) {
            Exception e = assertThrows(IllegalArgumentException.class, 
                () -> new SimulationEngine(moves, map, td.initialPositions));
            assertTrue(e.getMessage().equals(String.format("Unable to place animal at position %s", td.initialPositions[td.invalidAnimalIndex])));
            return;
        }
        IEngine engine = new SimulationEngine(moves, map, td.initialPositions);
        engine.run();

        for (AnimalData expectedAnimal : td.animData) {
            Exception e = assertThrows(IllegalArgumentException.class, 
                () -> map.place(new Animal(map, expectedAnimal.position)));
            assertTrue(e.getMessage().equals(String.format("Unable to place animal at position %s", expectedAnimal.position)));
    
            assertTrue(map.isOccupied(expectedAnimal.position));
            Animal animal = (Animal) map.objectAt(expectedAnimal.position);
            assertTrue(animal.isAt(expectedAnimal.position));
            assertTrue(animal.isFacing(expectedAnimal.orientation));
        }

    }
    private static void runTestSuiteOnSimulEng(SimulEngTestData[] testData) {
        for (SimulEngTestData td : testData) {
            runTestOnSimulEng(td);
        }
    }
    private static void runTestSuiteOnSimulEng(SimpleSimulEngTestData[] testData) {
        for (SimpleSimulEngTestData td : testData) {
            runTestOnSimulEng(new SimulEngTestData(td));
        }
    }

    @Test
    void testSimpleSimulationEngine() {
        final SimpleSimulEngTestData[] testData = {
            new SimpleSimulEngTestData(
                new String[] {
                    "r", "r", "f", "l", "b", "b", "r", "f"
                },
                new MoveDirection[] {
                    MoveDirection.RIGHT, MoveDirection.RIGHT, MoveDirection.FORWARD, MoveDirection.LEFT,
                    MoveDirection.BACKWARD, MoveDirection.BACKWARD, MoveDirection.RIGHT, MoveDirection.FORWARD
                },
                new Vector2d(0, 0),
                MapDirection.SOUTH
            ),
            new SimpleSimulEngTestData(
                new String[] {
                    "right", "right", "forward", "left", "backward", "backward", "right", "forward"
                },
                new MoveDirection[] {
                    MoveDirection.RIGHT, MoveDirection.RIGHT, MoveDirection.FORWARD, MoveDirection.LEFT,
                    MoveDirection.BACKWARD, MoveDirection.BACKWARD, MoveDirection.RIGHT, MoveDirection.FORWARD
                },
                new Vector2d(0, 0),
                MapDirection.SOUTH
            ),
            new SimpleSimulEngTestData(
                new String[] {
                    "right", "forward", "f", "forward"
                },
                new MoveDirection[] {
                    MoveDirection.RIGHT, MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD
                },
                new Vector2d(4, 2),
                MapDirection.EAST
            ),
            new SimpleSimulEngTestData(
                new String[] {
                    "f", "f", "f", "b", "f", "f", "r", "r", "b", "b"
                },
                new MoveDirection[] {
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.BACKWARD,
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.RIGHT, MoveDirection.RIGHT,
                    MoveDirection.BACKWARD, MoveDirection.BACKWARD
                },
                new Vector2d(2, 4),
                MapDirection.SOUTH
            ),
            new SimpleSimulEngTestData(
                new String[] {
                    "r", "b", "b", "l", "f", "f", "f", "f", "r", "b", "b", "r", "b", "b", "r", "f", "f", "b"
                },
                new MoveDirection[] {
                    MoveDirection.RIGHT, MoveDirection.BACKWARD, MoveDirection.BACKWARD, MoveDirection.LEFT,
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD,
                    MoveDirection.RIGHT, MoveDirection.BACKWARD, MoveDirection.BACKWARD, MoveDirection.RIGHT,
                    MoveDirection.BACKWARD, MoveDirection.BACKWARD, MoveDirection.RIGHT, MoveDirection.FORWARD,
                    MoveDirection.FORWARD, MoveDirection.BACKWARD
                },
                new Vector2d(1, 4),
                MapDirection.WEST
            ),
            new SimpleSimulEngTestData(
                new String[] {
                    "right", "roight", "letf", "przód", "x", "forward", "q", "AAAAAAAAAAA", "", "l"
                },
                new MoveDirection[] {
                    MoveDirection.RIGHT, MoveDirection.FORWARD, MoveDirection.LEFT
                },
                new Vector2d(3, 2),
                MapDirection.NORTH,
                1,
                -1
            )
        };
        runTestSuiteOnSimulEng(testData);
    }

    @Test
    void testSimulationEngine() {
        final SimulEngTestData[] testData = {
            new SimulEngTestData(
                new Vector2d(10, 5),
                new String[] {
                    "f", "b", "r", "l", "f", "f", "r", "r", "f", "f", "f", "f", "f", "f", "f", "f"
                },
                new MoveDirection[] {
                    MoveDirection.FORWARD, MoveDirection.BACKWARD, MoveDirection.RIGHT, MoveDirection.LEFT,
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.RIGHT, MoveDirection.RIGHT,
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD,
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.FORWARD
                },
                new Vector2d[] {
                    new Vector2d(2, 2),
                    new Vector2d(3, 4)
                },
                new AnimalData[] {
                    new AnimalData(new Vector2d(2, 0), MapDirection.SOUTH),
                    new AnimalData(new Vector2d(3, 4), MapDirection.NORTH)
                }
            ),
            new SimulEngTestData(
                new Vector2d(3, 5),
                new String[] {
                    "l", "r", "f", "b", "f", "l", "l", "f", "l", "f", "r", "f", "r", "b", "f", "b"
                },
                new MoveDirection[] {
                    MoveDirection.LEFT, MoveDirection.RIGHT, MoveDirection.FORWARD, MoveDirection.BACKWARD,
                    MoveDirection.FORWARD, MoveDirection.LEFT, MoveDirection.LEFT, MoveDirection.FORWARD,
                    MoveDirection.LEFT, MoveDirection.FORWARD, MoveDirection.RIGHT, MoveDirection.FORWARD,
                    MoveDirection.RIGHT, MoveDirection.BACKWARD, MoveDirection.FORWARD, MoveDirection.BACKWARD
                },
                new Vector2d[] {
                    new Vector2d(2, 2),  // zwierzę 1
                    new Vector2d(8, 8),  // nie zostanie umieszczone (poza granicami mapy)
                    new Vector2d(0, 1),  // zwierzę 2
                    new Vector2d(2, 2),  // nie zostanie umieszczone (pole zajęte)
                    new Vector2d(1, 4)   // zwierzę 3
                },
                new AnimalData[] {
                    new AnimalData(new Vector2d(2, 2), MapDirection.WEST),
                    new AnimalData(new Vector2d(2, 1), MapDirection.SOUTH),
                    new AnimalData(new Vector2d(1, 2), MapDirection.SOUTH)
                },
                -1,
                1
            ),
            new SimulEngTestData(
                new Vector2d(2, 2),
                new String[] {
                    "f", "b", "r", "l", "f", "f", "l", "r"
                },
                new MoveDirection[] {
                    MoveDirection.FORWARD, MoveDirection.BACKWARD, MoveDirection.RIGHT, MoveDirection.LEFT,
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.LEFT, MoveDirection.RIGHT
                },
                new Vector2d[] {
                    new Vector2d(0, 0),  // zwierzę 1
                    new Vector2d(1, 1)   // zwierzę 2
                },
                new AnimalData[] {
                    new AnimalData(new Vector2d(1, 1), MapDirection.NORTH),  // zwierzę 1
                    new AnimalData(new Vector2d(0, 0), MapDirection.NORTH)   // zwierzę 2
                }
            ),
            // Aktualnie niemożliwe jest sprawdzenie, czy faktycznie to samo zwierzę trafiło tam, gdzie trafić miało
            // Ten sam test, co wyżej, zmieniona kolejność zwierząt
            // test zakłada:   zwierzę 1 z (0, 0) na (1, 1); zwierzę 2 z (1, 1) na (0, 0)
            // faktyczny ruch: zwierzę 1 z (0, 0) na (0, 0); zwierzę 2 z (1, 1) na (1, 1)
            // Test przestanie przechodzić, gdy zaczniemy kontrolować, które zwierzę gdzie trafiło
            new SimulEngTestData(
                new Vector2d(2, 2),
                new String[] {
                    "f", "b", "r", "l", "f", "f", "l", "r"
                },
                new MoveDirection[] {
                    MoveDirection.FORWARD, MoveDirection.BACKWARD, MoveDirection.RIGHT, MoveDirection.LEFT,
                    MoveDirection.FORWARD, MoveDirection.FORWARD, MoveDirection.LEFT, MoveDirection.RIGHT
                },
                new Vector2d[] {
                    new Vector2d(0, 0),  // zwierzę 1
                    new Vector2d(1, 1)   // zwierzę 2
                },
                new AnimalData[] {
                    new AnimalData(new Vector2d(0, 0), MapDirection.NORTH),  // zwierzę 2
                    new AnimalData(new Vector2d(1, 1), MapDirection.NORTH)   // zwierzę 1
                }
            ),
        };
        runTestSuiteOnSimulEng(testData);
    }
}
