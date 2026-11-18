package ru.applecosmetic.cosmetic;

import java.util.List;
import ru.applecosmetic.effect.EffectDefinition;
import ru.applecosmetic.effect.TrailDefinition;

/**
 * Одна позиция косметики.
 *
 * @param name   название в исходном виде (MiniMessage)
 * @param icon   предмет для меню
 * @param item   источник модели для обликов и шляп, иначе null
 * @param effect эффект из частиц для убийства, крита и смерти, иначе null
 * @param trail  след снаряда, иначе null
 */
public record Cosmetic(
        Category category,
        String id,
        String name,
        List<String> lore,
        String icon,
        String item,
        String permission,
        EffectDefinition effect,
        TrailDefinition trail) {
}
