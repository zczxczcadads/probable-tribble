package ru.applecosmetic.skin;

import io.papermc.paper.datacomponent.DataComponentTypes;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import net.kyori.adventure.key.Key;
import org.bukkit.Bukkit;
import org.bukkit.NamespacedKey;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.PlayerInventory;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.inventory.meta.components.CustomModelDataComponent;
import org.bukkit.persistence.PersistentDataType;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.cosmetic.Category;
import ru.applecosmetic.cosmetic.Cosmetic;

/**
 * Облики мечей, кирок и тотемов. Предмету в инвентаре владельца подменяется модель
 * и ставится метка; при выходе предмета из инвентаря модель возвращается обратно.
 * Предметы, у которых уже есть своя модель, не трогаются, поэтому при снятии
 * облика достаточно сбросить модель к стандартной.
 */
public final class SkinService {

    private static final Category[] CATEGORIES = {Category.SWORD, Category.PICKAXE, Category.TOTEM};

    private final AppleCosmeticPlugin plugin;
    private final NamespacedKey tagKey;
    private final Map<Cosmetic, Optional<Skin>> skins = new IdentityHashMap<>();
    private final Set<UUID> dirty = new HashSet<>();

    /** @param tag метка на предмете: идентификатор облика и отпечаток его модели */
    private record Skin(String tag, NamespacedKey model, CustomModelDataComponent modelData) {
    }

    public SkinService(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
        this.tagKey = new NamespacedKey(plugin, "skin");
    }

    /** Забывает рассчитанные модели: после перезагрузки конфига или сторонних предметов. */
    public void invalidate() {
        skins.clear();
    }

    /** Приводит инвентарь игрока в соответствие с выбранными обликами. */
    public void sync(Player player) {
        Map<Category, Skin> wanted = new EnumMap<>(Category.class);
        for (Category category : CATEGORIES) {
            Skin skin = skin(plugin.cosmetics().selected(player, category));
            if (skin != null) {
                wanted.put(category, skin);
            }
        }
        PlayerInventory inventory = player.getInventory();
        for (int slot = 0, size = inventory.getSize(); slot < size; slot++) {
            ItemStack item = inventory.getItem(slot);
            if (item != null && update(item, wanted)) {
                inventory.setItem(slot, item);
            }
        }
        ItemStack cursor = player.getItemOnCursor();
        if (!cursor.isEmpty() && update(cursor, wanted)) {
            player.setItemOnCursor(cursor);
        }
    }

    /** Возвращает стандартный вид всем предметам игрока. */
    public void restore(Player player) {
        strip(player.getInventory());
        ItemStack cursor = player.getItemOnCursor();
        if (strip(cursor)) {
            player.setItemOnCursor(cursor);
        }
    }

    public void restoreAll() {
        Bukkit.getOnlinePlayers().forEach(this::restore);
    }

    /** Снимает облики со всех предметов в инвентаре (сундук, верстак и т. п.). */
    public void strip(Inventory inventory) {
        for (int slot = 0, size = inventory.getSize(); slot < size; slot++) {
            ItemStack item = inventory.getItem(slot);
            if (strip(item)) {
                inventory.setItem(slot, item);
            }
        }
    }

    /** Снимает облик с предмета; true, если предмет изменился. */
    public boolean strip(ItemStack item) {
        if (item == null || tag(item) == null) {
            return false;
        }
        item.editMeta(this::clear);
        return true;
    }

    /** Откладывает проверку инвентаря до следующего тика. */
    public void markDirty(Player player) {
        dirty.add(player.getUniqueId());
    }

    public void flushDirty() {
        if (dirty.isEmpty()) {
            return;
        }
        for (UUID id : List.copyOf(dirty)) {
            Player player = Bukkit.getPlayer(id);
            if (player != null) {
                sync(player);
            }
        }
        dirty.clear();
    }

    private boolean update(ItemStack item, Map<Category, Skin> wanted) {
        if (item.isEmpty()) {
            return false;
        }
        Category category = Category.skinFor(item.getType());
        Skin skin = category == null ? null : wanted.get(category);
        String tag = tag(item);
        if (tag == null) {
            if (skin == null || hasOwnModel(item)) {
                return false;
            }
            item.editMeta(meta -> write(meta, skin));
            return true;
        }
        if (skin != null && skin.tag().equals(tag)) {
            return false;
        }
        item.editMeta(meta -> {
            clear(meta);
            if (skin != null) {
                write(meta, skin);
            }
        });
        return true;
    }

    private String tag(ItemStack item) {
        return item.hasItemMeta() ? item.getPersistentDataContainer().get(tagKey, PersistentDataType.STRING) : null;
    }

    private static boolean hasOwnModel(ItemStack item) {
        if (!item.hasItemMeta()) {
            return false;
        }
        ItemMeta meta = item.getItemMeta();
        return meta.hasItemModel() || meta.hasCustomModelDataComponent();
    }

    private void write(ItemMeta meta, Skin skin) {
        meta.setItemModel(skin.model());
        meta.setCustomModelDataComponent(skin.modelData());
        meta.getPersistentDataContainer().set(tagKey, PersistentDataType.STRING, skin.tag());
    }

    private void clear(ItemMeta meta) {
        meta.setItemModel(null);
        meta.setCustomModelDataComponent(null);
        meta.getPersistentDataContainer().remove(tagKey);
    }

    private Skin skin(Cosmetic cosmetic) {
        if (cosmetic == null) {
            return null;
        }
        return skins.computeIfAbsent(cosmetic, this::build).orElse(null);
    }

    private Optional<Skin> build(Cosmetic cosmetic) {
        ItemStack source = plugin.items().resolveFirst(cosmetic.items());
        if (source == null) {
            return Optional.empty();
        }
        // Действующая модель: заданная явно либо стандартная для этого предмета.
        Key key = source.getData(DataComponentTypes.ITEM_MODEL);
        NamespacedKey model = key == null ? source.getType().getKey() : new NamespacedKey(key.namespace(), key.value());
        ItemMeta meta = source.getItemMeta();
        CustomModelDataComponent modelData =
                meta != null && meta.hasCustomModelDataComponent() ? meta.getCustomModelDataComponent() : null;
        int fingerprint = modelData == null ? model.hashCode() : Objects.hash(model, modelData.getFloats(),
                modelData.getFlags(), modelData.getStrings(), modelData.getColors());
        return Optional.of(new Skin(cosmetic.id() + "|" + Integer.toHexString(fingerprint), model, modelData));
    }
}
