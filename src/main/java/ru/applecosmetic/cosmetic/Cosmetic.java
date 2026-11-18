package ru.applecosmetic.cosmetic;

import java.util.List;
import ru.applecosmetic.effect.EffectDefinition;
import ru.applecosmetic.effect.TrailDefinition;

/**
 * Одна позиция косметики.
 *
 * @param name   название в исходном виде (MiniMessage)
 * @param icons  предметы для меню: используется первый доступный
 * @param items  источники модели для обликов и шляп: используется первый доступный
 * @param effect эффект из частиц для убийства, крита и смерти, иначе null
 * @param trail  след снаряда, иначе null
 */
public record Cosmetic(
        Category category,
        String id,
        String name,
        List<String> lore,
        List<String> icons,
        List<String> items,
        String permission,
        EffectDefinition effect,
        TrailDefinition trail) {
}
