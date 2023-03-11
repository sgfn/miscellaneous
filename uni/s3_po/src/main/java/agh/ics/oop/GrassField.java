package agh.ics.oop;

import java.util.Random;

public class GrassField extends AbstractWorldMap {
    private final int grassGenUpperBound;
    private final Random rng = new Random();

    private void generateGrass() {
        Vector2d pos;
            do {
                // Jest szansa, że ta pętla nigdy się nie zakończy. Szansa nikła, ale niezerowa. Too bad!
                pos = new Vector2d(rng.nextInt(grassGenUpperBound), rng.nextInt(grassGenUpperBound));
            } while (isOccupied(pos));
            Grass g = new Grass(pos);
            incorporealEntities.put(pos, g);
            mapBoundary.placeElem(g);
            notifyPositionChanged(pos, pos);
    }

    public GrassField(int n) {
        grassGenUpperBound = (int)(Math.sqrt((double)(n*10)))+1;
        for (int i=0; i<n; ++i) {
            generateGrass();
        }
    }

    @Override
    public Vector2d[] getBounds() {
        return mapBoundary.getEntityBounds();
    }

    // efektem ubocznym dzisiejszych labów jest to, że istoty cielesne zaczęły zjadać trawę
    @Override
    protected void handleRemovalOfIncorporealEntities(int amount) {
        for (int i=0; i<amount; ++i) {
            generateGrass();
        }
    }
}
