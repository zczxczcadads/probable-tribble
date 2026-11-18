package ru.applecosmetic.cosmetic;

import java.io.File;
import java.util.Collection;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.function.Consumer;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.YamlConfiguration;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.effect.EffectDefinition;
import ru.applecosmetic.effect.TrailDefinition;
import ru.applecosmetic.item.ItemResolver;
import ru.applecosmetic.util.Params;

/** Вся косметика из папок cosmetics/ и effects/. */
public final class CosmeticRegistry {

    private final AppleCosmeticPlugin plugin;
    private final Map<Category, Map<String, Cosmetic>> byCategory = new EnumMap<>(Category.class);

    public CosmeticRegistry(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    public void load() {
        byCategory.clear();
        int total = 0;
        for (Category category : Category.values()) {
            Map<String, Cosmetic> loaded = loadCategory(category);
            byCategory.put(category, loaded);
            total += loaded.size();
        }
        plugin.getLogger().info("Загружено косметики: " + total + ".");
    }

    /** Косметика категории в том порядке, в каком она записана в файле. */
    public Collection<Cosmetic> list(Category category) {
        return byCategory.getOrDefault(category, Map.of()).values();
    }

    public Cosmetic get(Category category, String id) {
        return byCategory.getOrDefault(category, Map.of()).get(id);
    }

    private Map<String, Cosmetic> loadCategory(Category category) {
        Map<String, Cosmetic> result = new LinkedHashMap<>();
        File file = new File(plugin.getDataFolder(), category.file());
        if (!file.exists()) {
            plugin.saveResource(category.file(), false);
        }
        YamlConfiguration yaml = new YamlConfiguration();
        try {
            yaml.load(file);
        } catch (Exception e) {
            plugin.getLogger().severe("Не удалось прочитать " + category.file() + ": " + e.getMessage());
            return result;
        }
        ConfigurationSection root = yaml.getConfigurationSection(category.rootKey());
        if (root == null) {
            plugin.getLogger().warning(category.file() + ": нет раздела «" + category.rootKey() + "».");
            return result;
        }
        for (String rawId : root.getKeys(false)) {
            ConfigurationSection section = root.getConfigurationSection(rawId);
            if (section == null) {
                continue;
            }
            String id = rawId.toLowerCase(Locale.ROOT);
            Consumer<String> warn = message ->
                    plugin.getLogger().warning(category.file() + " → " + rawId + ": " + message + ".");
            if (!id.matches("[a-z0-9_-]+")) {
                warn.accept("идентификатор может содержать только латинские буквы, цифры, «_» и «-»");
                continue;
            }
            Cosmetic cosmetic = parse(category, id, section, warn);
            if (cosmetic != null) {
                result.put(id, cosmetic);
            }
        }
        return result;
    }

    private Cosmetic parse(Category category, String id, ConfigurationSection section, Consumer<String> warn) {
        ItemResolver items = plugin.items();
        String item = section.getString("item");
        String icon = section.getString("icon");
        EffectDefinition effect = null;
        TrailDefinition trail = null;

        switch (category.kind()) {
            case SKIN, HAT -> {
                if (item == null || item.isBlank()) {
                    warn.accept("не указан предмет (item)");
                    return null;
                }
                if (ItemResolver.isBetterModel(item)) {
                    if (category.kind() != Category.Kind.HAT) {
                        warn.accept("модели BetterModel можно использовать только для шляп");
                        return null;
                    }
                } else {
                    items.check(item, warn);
                    if (icon == null) {
                        icon = item;
                    }
                }
            }
            case EFFECT -> {
                effect = EffectDefinition.parse(section, warn);
                if (effect.isEmpty()) {
                    warn.accept("эффект пуст: добавьте layers, sounds, lightning или firework");
                    return null;
                }
            }
            case TRAIL -> {
                Object raw = section.get("trail");
                if (raw == null) {
                    warn.accept("не указан след (trail)");
                    return null;
                }
                trail = TrailDefinition.parse(Params.of(raw), warn);
                if (trail == null) {
                    return null;
                }
            }
        }
        if (icon == null || icon.isBlank()) {
            icon = category.defaultIcon().name();
        }
        items.check(icon, warn);

        return new Cosmetic(
                category,
                id,
                section.getString("name", id),
                List.copyOf(section.getStringList("lore")),
                icon,
                item,
                section.getString("permission", "applecosmetic." + category.key() + "." + id).trim(),
                effect,
                trail);
    }
}
