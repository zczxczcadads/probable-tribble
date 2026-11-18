package ru.applecosmetic.skin;

import io.papermc.paper.event.player.PlayerInventorySlotChangeEvent;
import io.papermc.paper.event.player.PlayerItemFrameChangeEvent;
import org.bukkit.Bukkit;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.Item;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.ItemSpawnEvent;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.event.inventory.InventoryType;
import org.bukkit.event.player.PlayerArmorStandManipulateEvent;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryView;
import org.bukkit.inventory.ItemStack;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.cosmetic.Category;

/** Следит, чтобы облик был только на предметах в инвентаре владельца. */
public final class SkinListener implements Listener {

    private final AppleCosmeticPlugin plugin;

    public SkinListener(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onSlotChange(PlayerInventorySlotChangeEvent event) {
        if (Category.skinFor(event.getNewItemStack().getType()) != null) {
            plugin.skins().markDirty(event.getPlayer());
        }
    }

    @EventHandler(priority = EventPriority.LOWEST)
    public void onItemSpawn(ItemSpawnEvent event) {
        Item entity = event.getEntity();
        ItemStack item = entity.getItemStack();
        if (plugin.skins().strip(item)) {
            entity.setItemStack(item);
        }
    }

    // Список выпавших вещей могут забрать другие плагины (например, могилы), не создавая предметы в мире.
    @EventHandler(priority = EventPriority.LOWEST)
    public void onDeath(PlayerDeathEvent event) {
        event.getDrops().forEach(plugin.skins()::strip);
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onClick(InventoryClickEvent event) {
        cleanContainerLater(event.getView());
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onDrag(InventoryDragEvent event) {
        cleanContainerLater(event.getView());
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onClose(InventoryCloseEvent event) {
        Inventory top = event.getView().getTopInventory();
        if (isContainer(top)) {
            plugin.skins().strip(top);
        }
    }

    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onItemFrame(PlayerItemFrameChangeEvent event) {
        ItemStack item = event.getItemStack();
        if (plugin.skins().strip(item)) {
            event.setItemStack(item);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onArmorStand(PlayerArmorStandManipulateEvent event) {
        ArmorStand stand = event.getRightClicked();
        EquipmentSlot slot = event.getSlot();
        Bukkit.getScheduler().runTask(plugin, () -> {
            if (!stand.isValid()) {
                return;
            }
            ItemStack item = stand.getEquipment().getItem(slot);
            if (plugin.skins().strip(item)) {
                stand.getEquipment().setItem(slot, item);
            }
        });
    }

    private void cleanContainerLater(InventoryView view) {
        Inventory top = view.getTopInventory();
        if (isContainer(top)) {
            // Предмет попадает в контейнер уже после события.
            Bukkit.getScheduler().runTask(plugin, () -> plugin.skins().strip(top));
        }
    }

    /** Чужой инвентарь игрока (например, /invsee) контейнером не считается: там облики на своём месте. */
    private static boolean isContainer(Inventory inventory) {
        return inventory.getType() != InventoryType.PLAYER;
    }
}
