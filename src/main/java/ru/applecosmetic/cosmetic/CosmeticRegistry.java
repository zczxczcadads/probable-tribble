package ru.applecosmetic.cosmetic;

import java.io.File;
import java.util.ArrayList;
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
        ItemResolver resolver = plugin.items();
        List<String> items = specs(section, "item");
        List<String> icons = specs(section, "icon");
        EffectDefinition effect = null;
        TrailDefinition trail = null;

        switch (category.kind()) {
            case SKIN, HAT -> {
                if (items.isEmpty()) {
                    warn.accept("не указан предмет (item)");
                    return null;
                }
                List<String> usable = new ArrayList<>();
                for (String spec : items) {
                    if (!ItemResolver.isBetterModel(spec)) {
                        resolver.check(spec, warn);
                    } else if (category.kind() != Category.Kind.HAT) {
                        warn.accept("модели BetterModel подходят только для шляп, «" + spec + "» пропущен");
                        continue;
                    }
                    usable.add(spec);
                }
                if (usable.isEmpty()) {
                    return null;
                }
                items = usable;
                if (icons.isEmpty()) {
                    icons = usable.stream().filter(spec -> !ItemResolver.isBetterModel(spec)).toList();
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
        icons.forEach(icon -> resolver.check(icon, warn));

        return new Cosmetic(
                category,
                id,
                section.getString("name", id),
                List.copyOf(section.getStringList("lore")),
                List.copyOf(icons),
                List.copyOf(items),
                section.getString("permission", "applecosmetic." + category.key() + "." + id).trim(),
                effect,
                trail);
    }

    /** Значение поля: одна строка или список вариантов по убыванию предпочтения. */
    private static List<String> specs(ConfigurationSection section, String key) {
        List<String> raw = section.isList(key) ? section.getStringList(key)
                : section.isSet(key) ? List.of(String.valueOf(section.get(key))) : List.of();
        return raw.stream().map(String::trim).filter(spec -> !spec.isEmpty()).toList();
    }
}
