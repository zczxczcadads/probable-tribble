package ru.applecosmetic.effect;

import java.util.function.Consumer;
import ru.applecosmetic.util.Params;

/**
 * След за снарядом.
 *
 * @param amount частиц в каждой точке следа
 * @param spread разброс частиц
 * @param spiral радиус спирали вокруг траектории; 0 — прямой след
 */
public record TrailDefinition(ParticleSpec particle, int amount, double spread, double speed, double spiral) {

    public static TrailDefinition parse(Params params, Consumer<String> warn) {
        ParticleSpec particle = ParticleSpec.parse(params, warn);
        if (particle == null) {
            return null;
        }
        return new TrailDefinition(
                particle,
                Math.max(1, Math.min(20, params.integer("amount", 1))),
                Math.max(0, params.decimal("spread", 0.02)),
                Math.max(0, params.decimal("speed", 0.0)),
                Math.max(0, Math.min(2, params.decimal("spiral", 0.0))));
    }
}
