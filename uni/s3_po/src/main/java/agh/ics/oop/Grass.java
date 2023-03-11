package agh.ics.oop;

public class Grass extends AbstractWorldMapElement {
    public Grass(Vector2d pos) {
        this.pos = pos;
    }

    @Override
    public String toString() {
        return "*";
    }

    @Override
    public String getResource() {
        return "src/main/resources/grass.png";
    }

    @Override
    public String getLabel() {
        return "Trawa";
    }
}
