package ru.applecosmetic.menu;

import java.util.HashMap;
import java.util.Map;
import java.util.function.BiConsumer;
import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.event.inventory.ClickType;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;

/** Окно меню: предметы и действия по слотам. */
final class Menu implements InventoryHolder {

    private final Inventory inventory;
    private final Map<Integer, BiConsumer<Player, ClickType>> actions = new HashMap<>();

    Menu(int rows, Component title) {
        this.inventory = Bukkit.createInventory(this, rows * 9, title);
    }

    @Override
    public Inventory getInventory() {
        return inventory;
    }

    int size() {
        return inventory.getSize();
    }

    /** Ставит предмет в слот; action может быть null для декоративных предметов. */
    void set(int slot, ItemStack item, BiConsumer<Player, ClickType> action) {
        if (slot < 0 || slot >= inventory.getSize()) {
            return;
        }
        inventory.setItem(slot, item);
        if (action == null) {
            actions.remove(slot);
        } else {
            actions.put(slot, action);
        }
    }

    BiConsumer<Player, ClickType> action(int slot) {
        return actions.get(slot);
    }

    void clear() {
        inventory.clear();
        actions.clear();
    }
}
