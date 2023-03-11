package agh.ics.oop.gui;

import java.io.FileInputStream;
import java.io.FileNotFoundException;

import agh.ics.oop.IMapElement;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;

public class GuiElementBox {
    final VBox box;

    public GuiElementBox(IMapElement elem) {
        Image image;
        try {
            image = new Image(new FileInputStream(elem.getResource()));
        } catch (FileNotFoundException e) {
            throw new RuntimeException();
        }
        ImageView view = new ImageView(image);
        view.setFitWidth(20);
        view.setFitHeight(20);

        Label label = new Label(elem.getLabel());
        label.setFont(new Font("Arial", 8));

        box = new VBox();
        box.getChildren().add(view);
        box.getChildren().add(label);
        box.setAlignment(Pos.CENTER);
    }
}
