package ru.applecosmetic.item;

import com.destroystokyo.paper.profile.PlayerProfile;
import com.destroystokyo.paper.profile.ProfileProperty;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Consumer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.SkullMeta;
import org.bukkit.inventory.meta.components.CustomModelDataComponent;
import org.bukkit.plugin.Plugin;

/**
 * Превращает строку из конфига в предмет. Форматы:
 * DIAMOND_SWORD, PAPER:1001, model:ns:path, head:текстура,
 * itemsadder:ns:id, nexo:id, oraxen:id, craftengine:ns:id.
 * Там, где в конфиге указан список, берётся первый доступный вариант.
 */
public final class ItemResolver {

    private static final String BETTER_MODEL = "bettermodel:";
    private static final Pattern WITH_MODEL_DATA = Pattern.compile("^(.+):(\\d{1,9})$");
    private static final Pattern TEXTURE_HASH = Pattern.compile("^[0-9a-fA-F]{32,64}$");

    private final ExternalItems external;
    // Событие загрузки ItemsAdder приходит не из основного потока.
    private final Map<String, Optional<ItemStack>> cache = new ConcurrentHashMap<>();

    public ItemResolver(Plugin plugin) {
        this.external = new ExternalItems(plugin.getLogger());
    }

    /** Возвращает копию предмета или null, если его нет. */
    public ItemStack resolve(String spec) {
        if (spec == null || spec.isBlank()) {
            return null;
        }
        Optional<ItemStack> cached = cache.get(spec);
        if (cached == null) {
            cached = Optional.ofNullable(create(spec.trim()));
            cache.put(spec, cached);
        }
        return cached.map(ItemStack::clone).orElse(null);
    }

    /** Первый доступный предмет из списка; модели BetterModel пропускаются. */
    public ItemStack resolveFirst(List<String> specs) {
        for (String spec : specs) {
            if (isBetterModel(spec)) {
                continue;
            }
            ItemStack item = resolve(spec);
            if (item != null) {
                return item;
            }
        }
        return null;
    }

    /** Сбрасывает кэш: после перезагрузки конфига или предметов стороннего плагина. */
    public void invalidate() {
        cache.clear();
        external.resetWarnings();
    }

    /** Проверяет при загрузке конфига те предметы, которые не зависят от сторонних плагинов. */
    public void check(String spec, Consumer<String> warn) {
        if (isExternal(spec) || isBetterModel(spec)) {
            return;
        }
        if (resolve(spec) == null) {
            warn.accept("неизвестный предмет «" + spec + "»");
        }
    }

    public void registerLoadHooks(Plugin owner, Runnable onLoaded) {
        external.registerLoadHooks(owner, onLoaded);
    }

    public static boolean isBetterModel(String spec) {
        return spec != null && spec.trim().toLowerCase(Locale.ROOT).startsWith(BETTER_MODEL);
    }

    /** Имя модели BetterModel из строки вида bettermodel:имя. */
    public static String betterModelName(String spec) {
        return spec.trim().substring(BETTER_MODEL.length()).trim();
    }

    private static boolean isExternal(String spec) {
        return spec != null && ExternalItems.Provider.byPrefix(prefix(spec.trim())) != null;
    }

    private static String prefix(String spec) {
        int colon = spec.indexOf(':');
        return colon > 0 ? spec.substring(0, colon).toLowerCase(Locale.ROOT) : "";
    }

    private ItemStack create(String spec) {
        String prefix = prefix(spec);
        String rest = spec.substring(spec.indexOf(':') + 1).trim();
        ExternalItems.Provider provider = ExternalItems.Provider.byPrefix(prefix);
        if (provider != null) {
            return external.fetch(provider, rest, spec);
        }
        return switch (prefix) {
            case "model" -> model(rest);
            case "head" -> head(rest);
            case "bettermodel" -> null;
            default -> vanilla(spec);
        };
    }

    private static ItemStack vanilla(String spec) {
        Material material = null;
        Integer modelData = null;
        Matcher matcher = WITH_MODEL_DATA.matcher(spec);
        if (matcher.matches()) {
            material = Material.matchMaterial(matcher.group(1));
            if (material != null) {
                modelData = Integer.parseInt(matcher.group(2));
            }
        }
        if (material == null) {
            material = Material.matchMaterial(spec);
        }
        if (material == null || !material.isItem() || material.isAir()) {
            return null;
        }
        ItemStack item = new ItemStack(material);
        if (modelData != null) {
            float value = modelData;
            item.editMeta(meta -> {
                CustomModelDataComponent component = meta.getCustomModelDataComponent();
                component.setFloats(List.of(value));
                meta.setCustomModelDataComponent(component);
            });
        }
        return item;
    }

    private static ItemStack model(String key) {
        NamespacedKey model = NamespacedKey.fromString(key.toLowerCase(Locale.ROOT));
        if (model == null) {
            return null;
        }
        ItemStack item = new ItemStack(Material.PAPER);
        item.editMeta(meta -> meta.setItemModel(model));
        return item;
    }

    private static ItemStack head(String value) {
        if (value.isEmpty()) {
            return null;
        }
        String texture = value;
        if (TEXTURE_HASH.matcher(value).matches()) {
            texture = encodeTextureUrl("http://textures.minecraft.net/texture/" + value);
        } else if (value.startsWith("http://") || value.startsWith("https://")) {
            texture = encodeTextureUrl(value);
        }
        String encoded = texture;
        ItemStack item = new ItemStack(Material.PLAYER_HEAD);
        item.editMeta(SkullMeta.class, meta -> {
            PlayerProfile profile = Bukkit.createProfile(
                    UUID.nameUUIDFromBytes(encoded.getBytes(StandardCharsets.UTF_8)), null);
            profile.setProperty(new ProfileProperty("textures", encoded));
            meta.setPlayerProfile(profile);
        });
        return item;
    }

    private static String encodeTextureUrl(String url) {
        String json = "{\"textures\":{\"SKIN\":{\"url\":\"" + url + "\"}}}";
        return Base64.getEncoder().encodeToString(json.getBytes(StandardCharsets.UTF_8));
    }
}
