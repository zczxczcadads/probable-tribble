package ru.applecosmetic.effect;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.function.Consumer;
import org.bukkit.Color;
import org.bukkit.FireworkEffect;
import ru.applecosmetic.util.Params;

/** Фейерверк, который взрывается на месте и никому не наносит урона. */
public record FireworkSpec(FireworkEffect effect) {

    public static FireworkSpec parse(Params params, Consumer<String> warn) {
        String typeName = params.string("type", "BALL_LARGE");
        FireworkEffect.Type type;
        try {
            type = FireworkEffect.Type.valueOf(typeName.trim().toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            warn.accept("неизвестный тип фейерверка «" + typeName + "», использован BALL_LARGE");
            type = FireworkEffect.Type.BALL_LARGE;
        }
        List<Color> colors = colors(params.strings("colors"), warn);
        if (colors.isEmpty()) {
            colors.add(Color.WHITE);
        }
        return new FireworkSpec(FireworkEffect.builder()
                .with(type)
                .withColor(colors)
                .withFade(colors(params.strings("fade"), warn))
                .flicker(params.flag("flicker", false))
                .trail(params.flag("trail", false))
                .build());
    }

    private static List<Color> colors(List<String> raw, Consumer<String> warn) {
        List<Color> colors = new ArrayList<>();
        for (String entry : raw) {
            Color color = Params.parseColor(entry);
            if (color == null) {
                warn.accept("неверный цвет «" + entry + "», нужен формат #RRGGBB");
            } else {
                colors.add(color);
            }
        }
        return colors;
    }
}
