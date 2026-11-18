package ru.applecosmetic.menu;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.BiConsumer;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.MemoryConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.ClickType;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.cosmetic.Category;
import ru.applecosmetic.cosmetic.Cosmetic;
import ru.applecosmetic.cosmetic.CosmeticManager;
import ru.applecosmetic.effect.SoundSpec;
import ru.applecosmetic.effect.TrailService;
import ru.applecosmetic.util.Text;

/** Меню /cosmetics: главное окно с категориями и окна категорий. */
public final class MenuManager implements Listener {

    private static final long PREVIEW_COOLDOWN_MS = 1500;
    private static final List<Integer> DEFAULT_ITEM_SLOTS = List.of(
            10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34);

    private final AppleCosmeticPlugin plugin;
    private final Map<UUID, Long> lastPreview = new HashMap<>();

    public MenuManager(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    public void openMain(Player player) {
        ConfigurationSection config = section("menu.main");
        Menu menu = new Menu(rows(config, 5), Text.parse(config.getString("title", "Косметика")));
        fill(menu);

        CosmeticManager cosmetics = plugin.cosmetics();
        for (Category category : Category.values()) {
            ConfigurationSection button = config.getConfigurationSection("categories." + category.key());
            if (button == null) {
                continue;
            }
            Cosmetic selected = cosmetics.selected(player, category);
            List<String> lore = new ArrayList<>(button.getStringList("lore"));
            lore.addAll(config.getStringList("category-lore"));
            ItemStack icon = icon(one(button.getString("icon")), category.defaultIcon(),
                    button.getString("name", cosmetics.title(category)), lore, false,
                    "selected", selected == null ? plugin.messages().raw("none") : selected.name(),
                    "owned", String.valueOf(cosmetics.owned(player, category)),
                    "total", String.valueOf(plugin.registry().list(category).size()));
            menu.set(button.getInt("slot", -1), icon, (clicker, click) -> {
                sound(clicker, "click");
                openCategory(clicker, category, 0);
            });
        }

        ConfigurationSection reset = config.getConfigurationSection("reset");
        if (reset != null) {
            menu.set(reset.getInt("slot", -1), button(reset, Material.BARRIER), (clicker, click) -> {
                if (plugin.cosmetics().resetAll(clicker)) {
                    sound(clicker, "unselect");
                    plugin.messages().send(clicker, "reset-all");
                    openMain(clicker);
                } else {
                    sound(clicker, "deny");
                    plugin.messages().send(clicker, "nothing-selected");
                }
            });
        }
        ConfigurationSection close = config.getConfigurationSection("close");
        if (close != null) {
            menu.set(close.getInt("slot", -1), button(close, Material.OAK_DOOR), (clicker, click) -> {
                sound(clicker, "click");
                clicker.closeInventory();
            });
        }
        player.openInventory(menu.getInventory());
    }

    public void openCategory(Player player, Category category, int requestedPage) {
        ConfigurationSection config = section("menu.category");
        int rows = rows(config, 5);
        List<Integer> slots = itemSlots(config, rows * 9);
        int total = plugin.registry().list(category).size();
        int pages = Math.max(1, (total + slots.size() - 1) / slots.size());
        int page = Math.max(0, Math.min(pages - 1, requestedPage));

        String title = Text.replace(config.getString("title", "{category}"),
                "category", plugin.cosmetics().title(category),
                "page", String.valueOf(page + 1),
                "pages", String.valueOf(pages));
        Menu menu = new Menu(rows, Text.parse(title));
        render(menu, player, category, page, pages, slots);
        player.openInventory(menu.getInventory());
    }

    /** Закрывает меню у всех игроков: перед перезагрузкой и выключением. */
    public void closeAll() {
        for (Player player : Bukkit.getOnlinePlayers()) {
            if (player.getOpenInventory().getTopInventory().getHolder(false) instanceof Menu) {
                player.closeInventory();
            }
        }
    }

    public void forget(UUID id) {
        lastPreview.remove(id);
    }

    private void render(Menu menu, Player player, Category category, int page, int pages, List<Integer> slots) {
        ConfigurationSection config = section("menu.category");
        CosmeticManager cosmetics = plugin.cosmetics();
        boolean glint = plugin.getConfig().getBoolean("menu.selected-glint", true);
        menu.clear();
        fill(menu);

        List<Cosmetic> list = List.copyOf(plugin.registry().list(category));
        int from = page * slots.size();
        for (int i = 0; i < slots.size() && from + i < list.size(); i++) {
            Cosmetic cosmetic = list.get(from + i);
            boolean selected = cosmetics.isSelected(player, cosmetic);
            String status = selected ? "selected" : cosmetics.has(player, cosmetic) ? "available" : "locked";
            List<String> lore = new ArrayList<>(cosmetic.lore());
            lore.addAll(config.getStringList("status." + status));
            if (category.previewable()) {
                lore.addAll(config.getStringList("status.preview"));
            }
            ItemStack icon = icon(cosmetic.icons(), category.defaultIcon(), cosmetic.name(), lore, selected && glint);
            menu.set(slots.get(i), icon, (clicker, click) -> {
                if (click.isRightClick() && category.previewable()) {
                    preview(clicker, cosmetic);
                    return;
                }
                toggle(clicker, cosmetic);
                render(menu, clicker, category, page, pages, slots);
            });
        }

        Cosmetic current = cosmetics.selected(player, category);
        String currentName = current == null ? plugin.messages().raw("none") : current.name();
        ConfigurationSection back = config.getConfigurationSection("back");
        if (back != null) {
            menu.set(back.getInt("slot", -1), button(back, Material.ARROW), (clicker, click) -> {
                sound(clicker, "click");
                openMain(clicker);
            });
        }
        ConfigurationSection unequip = config.getConfigurationSection("unequip");
        if (unequip != null) {
            menu.set(unequip.getInt("slot", -1), button(unequip, Material.BARRIER, "selected", currentName),
                    (clicker, click) -> {
                        Cosmetic worn = plugin.cosmetics().selected(clicker, category);
                        if (plugin.cosmetics().unselect(clicker, category)) {
                            sound(clicker, "unselect");
                            if (worn != null) {
                                plugin.messages().send(clicker, "unselected", "name", worn.name());
                            }
                            render(menu, clicker, category, page, pages, slots);
                        } else {
                            sound(clicker, "deny");
                            plugin.messages().send(clicker, "nothing-selected");
                        }
                    });
        }
        ConfigurationSection previous = config.getConfigurationSection("previous");
        if (previous != null && page > 0) {
            menu.set(previous.getInt("slot", -1), button(previous, Material.ARROW), (clicker, click) -> {
                sound(clicker, "click");
                openCategory(clicker, category, page - 1);
            });
        }
        ConfigurationSection next = config.getConfigurationSection("next");
        if (next != null && page < pages - 1) {
            menu.set(next.getInt("slot", -1), button(next, Material.ARROW), (clicker, click) -> {
                sound(clicker, "click");
                openCategory(clicker, category, page + 1);
            });
        }
    }

    private void toggle(Player player, Cosmetic cosmetic) {
        CosmeticManager cosmetics = plugin.cosmetics();
        if (!cosmetics.has(player, cosmetic)) {
            sound(player, "deny");
            plugin.messages().send(player, "locked", "name", cosmetic.name());
        } else if (cosmetics.isSelected(player, cosmetic)) {
            cosmetics.unselect(player, cosmetic.category());
            sound(player, "unselect");
            plugin.messages().send(player, "unselected", "name", cosmetic.name());
        } else {
            cosmetics.select(player, cosmetic);
            sound(player, "select");
            plugin.messages().send(player, "selected", "name", cosmetic.name());
        }
    }

    /** Показывает эффект только самому игроку, в нескольких блоках перед ним. */
    private void preview(Player player, Cosmetic cosmetic) {
        long now = System.currentTimeMillis();
        Long last = lastPreview.get(player.getUniqueId());
        if (last != null && now - last < PREVIEW_COOLDOWN_MS) {
            sound(player, "deny");
            return;
        }
        lastPreview.put(player.getUniqueId(), now);
        player.closeInventory();
        plugin.messages().send(player, "preview", "name", cosmetic.name());
        if (cosmetic.trail() != null) {
            plugin.trails().preview(player, cosmetic.trail());
        } else if (cosmetic.effect() != null) {
            Location origin = player.getLocation().add(TrailService.forward(player).multiply(3));
            plugin.effects().play(cosmetic.effect(), origin, player);
        }
    }

    private void fill(Menu menu) {
        ItemStack filler = plugin.items().resolve(plugin.getConfig().getString("menu.filler", ""));
        if (filler == null) {
            return;
        }
        filler.editMeta(meta -> meta.setHideTooltip(true));
        for (int slot = 0; slot < menu.size(); slot++) {
            menu.set(slot, filler, null);
        }
    }

    private ItemStack button(ConfigurationSection config, Material fallback, String... placeholders) {
        return icon(one(config.getString("icon")), fallback, config.getString("name", ""),
                config.getStringList("lore"), false, placeholders);
    }

    private static List<String> one(String spec) {
        return spec == null || spec.isBlank() ? List.of() : List.of(spec);
    }

    /** Значок меню из первого доступного предмета; если нет ни одного — из запасного материала. */
    private ItemStack icon(List<String> specs, Material fallback, String name, List<String> lore, boolean glint,
                           String... placeholders) {
        ItemStack item = plugin.items().resolveFirst(specs);
        if (item == null) {
            item = new ItemStack(fallback);
        }
        item.setAmount(1);
        item.editMeta(meta -> {
            meta.displayName(Text.item(Text.replace(name, placeholders)));
            meta.lore(lore.stream().map(line -> Text.item(Text.replace(line, placeholders))).toList());
            meta.addItemFlags(ItemFlag.values());
            if (glint) {
                meta.setEnchantmentGlintOverride(true);
            }
        });
        return item;
    }

    private void sound(Player player, String key) {
        SoundSpec sound = SoundSpec.parse(plugin.getConfig().get("menu.sounds." + key));
        if (sound != null) {
            sound.playTo(player);
        }
    }

    private ConfigurationSection section(String path) {
        ConfigurationSection section = plugin.getConfig().getConfigurationSection(path);
        return section == null ? new MemoryConfiguration() : section;
    }

    private static int rows(ConfigurationSection config, int fallback) {
        return Math.max(1, Math.min(6, config.getInt("rows", fallback)));
    }

    private static List<Integer> itemSlots(ConfigurationSection config, int size) {
        List<Integer> slots = new ArrayList<>();
        List<Integer> configured = config.getIntegerList("item-slots");
        for (int slot : configured.isEmpty() ? DEFAULT_ITEM_SLOTS : configured) {
            if (slot >= 0 && slot < size && !slots.contains(slot)) {
                slots.add(slot);
            }
        }
        if (slots.isEmpty()) {
            slots.add(0);
        }
        return slots;
    }

    @EventHandler
    public void onClick(InventoryClickEvent event) {
        if (!(event.getView().getTopInventory().getHolder(false) instanceof Menu menu)) {
            return;
        }
        event.setCancelled(true);
        ClickType click = event.getClick();
        int slot = event.getRawSlot();
        if (slot < 0 || slot >= menu.size() || !(event.getWhoClicked() instanceof Player player)
                || click == ClickType.DOUBLE_CLICK || !(click.isLeftClick() || click.isRightClick())) {
            return;
        }
        BiConsumer<Player, ClickType> action = menu.action(slot);
        if (action != null) {
            // Открывать и закрывать окна прямо в обработчике клика нельзя.
            Bukkit.getScheduler().runTask(plugin, () -> {
                if (player.isOnline() && player.getOpenInventory().getTopInventory().getHolder(false) == menu) {
                    action.accept(player, click);
                }
            });
        }
    }

    @EventHandler
    public void onDrag(InventoryDragEvent event) {
        if (event.getView().getTopInventory().getHolder(false) instanceof Menu) {
            event.setCancelled(true);
        }
    }
}
