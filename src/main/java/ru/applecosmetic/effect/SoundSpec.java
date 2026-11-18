package ru.applecosmetic.effect;

import java.util.Locale;
import org.bukkit.Location;
import org.bukkit.NamespacedKey;
import org.bukkit.Registry;
import org.bukkit.SoundCategory;
import org.bukkit.entity.Player;
import ru.applecosmetic.util.Params;

/** Звук по ключу, например entity.blaze.shoot; подходят и звуки из ресурспака. */
public record SoundSpec(String name, float volume, float pitch) {

    public static SoundSpec parse(Object source) {
        if (source == null) {
            return null;
        }
        if (source instanceof String text) {
            return text.isBlank() ? null : new SoundSpec(text.trim().toLowerCase(Locale.ROOT), 1.0f, 1.0f);
        }
        Params params = Params.of(source);
        String name = params.string("name", "");
        if (name.isBlank()) {
            return null;
        }
        return new SoundSpec(name.trim().toLowerCase(Locale.ROOT),
                (float) params.decimal("volume", 1.0), (float) params.decimal("pitch", 1.0));
    }

    /** Звуки Minecraft сверяются с реестром; звуки из ресурспаков проверить нельзя. */
    public boolean known() {
        NamespacedKey key = NamespacedKey.fromString(name);
        if (key == null) {
            return false;
        }
        return !key.getNamespace().equals(NamespacedKey.MINECRAFT) || Registry.SOUND_EVENT.get(key) != null;
    }

    /** @param only единственный слушатель; null — слышат все поблизости */
    public void play(Location at, Player only) {
        if (only != null) {
            only.playSound(at, name, SoundCategory.PLAYERS, volume, pitch);
        } else if (at.getWorld() != null) {
            at.getWorld().playSound(at, name, SoundCategory.PLAYERS, volume, pitch);
        }
    }

    public void playTo(Player player) {
        player.playSound(player.getLocation(), name, SoundCategory.MASTER, volume, pitch);
    }
}
