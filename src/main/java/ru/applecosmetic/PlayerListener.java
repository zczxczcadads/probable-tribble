package ru.applecosmetic;

import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

public final class PlayerListener implements Listener {

    private final AppleCosmeticPlugin plugin;

    public PlayerListener(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.LOWEST)
    public void onJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        plugin.cosmetics().validate(player);
        plugin.skins().sync(player);
        // Шляпа отправляется чуть позже, когда клиент уже получил свой инвентарь.
        Bukkit.getScheduler().runTaskLater(plugin, () -> {
            if (player.isOnline()) {
                plugin.hats().update(player);
            }
        }, 10L);
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onQuit(PlayerQuitEvent event) {
        Player player = event.getPlayer();
        // В сохранённых данных игрока предметы остаются без обликов.
        plugin.skins().restore(player);
        plugin.hats().remove(player);
        plugin.menus().forget(player.getUniqueId());
        plugin.store().unload(player.getUniqueId());
    }
}
