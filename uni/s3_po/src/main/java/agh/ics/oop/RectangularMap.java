package agh.ics.oop;

public class RectangularMap extends AbstractWorldMap {
    private final Vector2d boundaryLowerLeft;
    private final Vector2d boundaryUpperRight;

    public RectangularMap(int width, int height) {
        boundaryLowerLeft  = new Vector2d(0, 0);
        boundaryUpperRight = new Vector2d(width-1, height-1);
    }

    @Override
    public boolean canMoveTo(Vector2d position) {
        return boundaryLowerLeft.precedes(position) &&
               boundaryUpperRight.follows(position) &&
               !isOccupied(position);
    }

    @Override
    public Vector2d[] getBounds() {
        return new Vector2d[] { boundaryLowerLeft, boundaryUpperRight };
    }

    @Override
    protected void handleRemovalOfIncorporealEntities(int amount) {};
}
