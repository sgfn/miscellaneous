package agh.ics.oop;

import java.util.HashSet;
import java.util.Vector;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class OptionsParser {
    public static final HashSet<String> allowedArgs = Stream.of(
        "forward", "f", "backward", "b", "right", "r", "left", "l"
    ).collect(Collectors.toCollection(HashSet::new));

    public static MoveDirection[] parse(String[] args) throws IllegalArgumentException {
        Vector<MoveDirection> v = new Vector<MoveDirection>();
        for (String arg : args) {
            if (!allowedArgs.contains(arg)) {
                throw new IllegalArgumentException(String.format("Invalid move: `%s'", arg));
            }
            if (arg.equals("forward") || arg.equals("f")) {
                v.add(MoveDirection.FORWARD);
            } else if (arg.equals("backward") || arg.equals("b")) {
                v.add(MoveDirection.BACKWARD);
            } else if (arg.equals("right") || arg.equals("r")) {
                v.add(MoveDirection.RIGHT);
            } else if (arg.equals("left") || arg.equals("l")) {
                v.add(MoveDirection.LEFT);
            }
        }

        return v.toArray(new MoveDirection[v.size()]);
    }
}
