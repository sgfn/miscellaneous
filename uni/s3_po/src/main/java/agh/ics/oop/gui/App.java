package agh.ics.oop.gui;

import static java.lang.System.out;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.HPos;
import javafx.stage.Stage;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.ColumnConstraints;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.RowConstraints;
import javafx.scene.layout.VBox;
import agh.ics.oop.*;

public class App extends Application implements IPositionChangeObserver {
    private AbstractWorldMap map;
    private GridPane grid;
    private Map<Vector2d, Node> nodeMap = new HashMap<>();
    private Vector2d[] prevBounds;
    private Stage pStage;
    private SimulationEngine engine;

    public void init() {
        final int moveDelay = 300;
        MoveDirection[] directions = null;
        try {
            directions = OptionsParser.parse(getParameters().getRaw().toArray(String[]::new));
        } catch (IllegalArgumentException ex) {
            out.println(ex.getMessage());
            System.exit(1);
        }

        // map = new RectangularMap(10, 5);
        map = new GrassField(10);
        map.addObserver(this);
        Vector2d[] positions = { new Vector2d(2, 2), new Vector2d(3, 4) };
        // engine = new SimulationEngine(directions, map, positions, moveDelay);
        engine = new SimulationEngine(map, positions, moveDelay);
        engine.addObserver(this);
        out.println(map);
    }

    public void start(Stage primaryStage) {
        pStage = primaryStage;
        drawMap();
    }

    @Override
    public void positionChanged(Vector2d oldPosition, Vector2d newPosition) {
        Platform.runLater(() -> {
            Vector2d[] bounds = map.getBounds();
            if (!Arrays.equals(bounds, prevBounds)) {
                drawMap();
                return;
            }
            grid.getChildren().removeAll(nodeMap.remove(oldPosition), nodeMap.remove(newPosition));
            Object object = this.map.objectAt(newPosition);
            Node n = new GuiElementBox((IMapElement)object).box;
            final Vector2d lowerLeft = bounds[0];
            final int dimY = bounds[1].y - bounds[0].y + 1;
            grid.add(n, newPosition.x - lowerLeft.x + 1, dimY - (newPosition.y - lowerLeft.y));
            nodeMap.put(newPosition, n);
        });
    }

    private void drawMap() {
        nodeMap.clear();

        prevBounds = map.getBounds();
        Vector2d lowerLeft = prevBounds[0];
        Vector2d upperRight = prevBounds[1];
        int dimX = upperRight.x - lowerLeft.x + 1;
        int dimY = upperRight.y - lowerLeft.y + 1;

        grid = new GridPane();
        grid.setGridLinesVisible(true);
        for (int i=0; i<=dimX; ++i) {
            grid.getColumnConstraints().add(new ColumnConstraints(30));
        }
        for (int i=0; i<=dimY; ++i) {
            grid.getRowConstraints().add(new RowConstraints(30));
        }

        grid.add(new Label("y\\x"), 0, 0);

        for (int dx=0; dx<dimX; ++dx) {
            grid.add(new Label(String.format("%d", lowerLeft.x+dx)), dx+1, 0);
        }

        for (int dy=0; dy<dimY; ++dy) {
            grid.add(new Label(String.format("%d", lowerLeft.y+dy)), 0, dimY-dy);
            for (int dx=0; dx<dimX; ++dx) {
                Vector2d currentPosition = new Vector2d(lowerLeft.x+dx, lowerLeft.y+dy);
                if (this.map.isOccupied(currentPosition)) {
                    Object object = this.map.objectAt(currentPosition);
                    if (object != null) {
                        Node n = new GuiElementBox((IMapElement)object).box;
                        nodeMap.put(currentPosition, n);
                        grid.add(n, dx+1, dimY-dy);
                    }
                }
            }
        }

        for (var x : grid.getChildren()) {
            GridPane.setHalignment(x, HPos.CENTER);
        }

        TextField tf = new TextField();
        Button button = new Button("Start");
        button.setOnAction(actionEvent -> {
            try {
                engine.setDirections(OptionsParser.parse(tf.getText().split(" ")));
            } catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
                return;
            }
            Thread engineThread = new Thread(engine);
            engineThread.start();
        });
        HBox hb = new HBox(tf, button);
        VBox vb = new VBox(grid, hb);

        Scene scene = new Scene(vb, 400, 400);

        pStage.setScene(scene);
        pStage.show();
    }
}
