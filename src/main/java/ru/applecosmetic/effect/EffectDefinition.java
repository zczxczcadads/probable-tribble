package ru.applecosmetic.effect;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import org.bukkit.configuration.ConfigurationSection;
import ru.applecosmetic.util.Params;

/** Разовый эффект: слои частиц, звуки, молния и фейерверк. */
public record EffectDefinition(
        List<EffectLayer> layers,
        List<SoundSpec> sounds,
        boolean lightning,
        FireworkSpec firework) {

    public static EffectDefinition parse(ConfigurationSection section, Consumer<String> warn) {
        List<EffectLayer> layers = new ArrayList<>();
        for (Map<?, ?> entry : section.getMapList("layers")) {
            EffectLayer layer = EffectLayer.parse(Params.of(entry), warn);
            if (layer != null) {
                layers.add(layer);
            }
        }
        List<SoundSpec> sounds = new ArrayList<>();
        List<?> rawSounds = section.getList("sounds");
        if (rawSounds != null) {
            for (Object entry : rawSounds) {
                SoundSpec sound = SoundSpec.parse(entry);
                if (sound == null) {
                    warn.accept("звук без названия пропущен");
                } else {
                    if (!sound.known()) {
                        warn.accept("неизвестный звук «" + sound.name() + "»");
                    }
                    sounds.add(sound);
                }
            }
        }
        Object firework = section.get("firework");
        return new EffectDefinition(List.copyOf(layers), List.copyOf(sounds),
                section.getBoolean("lightning", false),
                firework == null ? null : FireworkSpec.parse(Params.of(firework), warn));
    }

    public boolean isEmpty() {
        return layers.isEmpty() && sounds.isEmpty() && !lightning && firework == null;
    }

    /** Сколько тиков длится эффект. */
    public int ticks() {
        int ticks = 0;
        for (EffectLayer layer : layers) {
            ticks = Math.max(ticks, layer.delay() + layer.duration());
        }
        return ticks;
    }
}
