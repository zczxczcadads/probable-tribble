package ru.applecosmetic.effect;

import java.util.Arrays;
import java.util.Locale;
import java.util.function.Consumer;
import ru.applecosmetic.util.Params;

/** Один слой эффекта: форма, частица и её параметры. */
public record EffectLayer(
        Animation animation,
        ParticleSpec particle,
        int amount,
        double radius,
        double height,
        double yOffset,
        int duration,
        int delay,
        double speed) {

    public static EffectLayer parse(Params params, Consumer<String> warn) {
        String name = params.string("animation", "BURST");
        Animation animation;
        try {
            animation = Animation.valueOf(name.trim().toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            warn.accept("неизвестная анимация «" + name + "». Доступные: " + Arrays.toString(Animation.values()));
            return null;
        }
        ParticleSpec particle = ParticleSpec.parse(params, warn);
        if (particle == null) {
            return null;
        }
        return new EffectLayer(
                animation,
                particle,
                clamp(params.integer("amount", animation.amount), 1, 500),
                params.decimal("radius", animation.radius),
                params.decimal("height", animation.height),
                params.decimal("y-offset", animation.yOffset),
                clamp(params.integer("duration", animation.duration), 1, 200),
                clamp(params.integer("delay", 0), 0, 200),
                params.decimal("speed", animation.speed));
    }

    private static int clamp(int value, int min, int max) {
        return Math.max(min, Math.min(max, value));
    }
}
