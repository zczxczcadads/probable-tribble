package ru.applecosmetic.hat;

import com.destroystokyo.paper.event.player.PlayerArmorChangeEvent;
import io.papermc.paper.event.player.PlayerTrackEntityEvent;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import org.bukkit.Bukkit;
import org.bukkit.GameMode;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityPotionEffectEvent;
import org.bukkit.event.player.PlayerChangedWorldEvent;
import org.bukkit.event.player.PlayerGameModeChangeEvent;
import org.bukkit.event.player.PlayerRespawnEvent;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.components.EquippableComponent;
import org.bukkit.potion.PotionEffectType;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.Settings;
import ru.applecosmetic.cosmetic.Category;
import ru.applecosmetic.cosmetic.Cosmetic;
import ru.applecosmetic.item.BetterModelHook;
import ru.applecosmetic.item.ItemResolver;

/**
 * Шляпы. Обычная шляпа — это предмет, который клиенты видят в слоте шлема:
 * настоящий шлем остаётся на месте и продолжает защищать. Сервер заново
 * рассылает настоящую экипировку при её смене и при появлении игрока в зоне
 * видимости, поэтому после таких событий шляпа отправляется повторно.
 */
public final class HatService implements Listener {

    private final AppleCosmeticPlugin plugin;
    private final Map<UUID, ItemStack> hats = new HashMap<>();
    private final Set<UUID> shownToOthers = new HashSet<>();
    private final Set<UUID> shownToSelf = new HashSet<>();
    private final Map<UUID, ModelHat> models = new HashMap<>();
    private final Set<String> reported = new HashSet<>();
    private BetterModelHook betterModel;

    private record ModelHat(String name, Object tracker) {
    }

    public HatService(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    /** Пересчитывает шляпу игрока по его выбору. */
    public void update(Player player) {
        UUID id = player.getUniqueId();
        Cosmetic cosmetic = plugin.cosmetics().selected(player, Category.HAT);
        String model = null;
        ItemStack hat = null;
        if (cosmetic != null) {
            // Используется первый доступный вариант из списка item.
            for (String spec : cosmetic.items()) {
                if (ItemResolver.isBetterModel(spec)) {
                    String name = ItemResolver.betterModelName(spec);
                    BetterModelHook hook = hook();
                    if (hook != null && hook.hasModel(name)) {
                        model = name;
                        break;
                    }
                } else if ((hat = build(spec)) != null) {
                    break;
                }
            }
            if (model == null && hat == null && reported.add(cosmetic.id())) {
                plugin.getLogger().warning("Шляпа «" + cosmetic.id() + "» недоступна: не найден ни один из её предметов.");
            }
        }

        updateModel(player, model);
        if (hat == null) {
            hats.remove(id);
        } else {
            hats.put(id, hat);
        }
        refresh(player);
    }

    /** Заново показывает шляпу игрока всем, кто его видит, и ему самому. */
    public void refresh(Player wearer) {
        UUID id = wearer.getUniqueId();
        ItemStack hat = visibleHat(wearer);
        if (hat != null) {
            shownToOthers.add(id);
            for (Player viewer : wearer.getTrackedBy()) {
                viewer.sendEquipmentChange(wearer, EquipmentSlot.HEAD, hat);
            }
        } else if (shownToOthers.remove(id)) {
            ItemStack real = realHelmet(wearer);
            for (Player viewer : wearer.getTrackedBy()) {
                viewer.sendEquipmentChange(wearer, EquipmentSlot.HEAD, real);
            }
        }

        // В творческом режиме клиент сам сообщает серверу содержимое слотов, и поддельный
        // предмет стал бы настоящим, поэтому себе шляпа там не показывается.
        boolean self = hat != null && plugin.settings().hatShowToSelf() && wearer.getGameMode() != GameMode.CREATIVE;
        if (self) {
            shownToSelf.add(id);
            wearer.sendEquipmentChange(wearer, EquipmentSlot.HEAD, hat);
        } else if (shownToSelf.remove(id)) {
            wearer.sendEquipmentChange(wearer, EquipmentSlot.HEAD, realHelmet(wearer));
        }
    }

    public void refreshAll() {
        for (UUID id : List.copyOf(hats.keySet())) {
            Player player = Bukkit.getPlayer(id);
            if (player != null) {
                refresh(player);
            }
        }
        for (Map.Entry<UUID, ModelHat> entry : List.copyOf(models.entrySet())) {
            Player player = Bukkit.getPlayer(entry.getKey());
            BetterModelHook hook = hook();
            // После возрождения или смены мира BetterModel может закрыть модель.
            if (player != null && hook != null && hook.isClosed(entry.getValue().tracker())) {
                models.remove(entry.getKey());
                updateModel(player, entry.getValue().name());
            }
        }
    }

    /** Забывает игрока при выходе. */
    public void remove(Player player) {
        UUID id = player.getUniqueId();
        hats.remove(id);
        shownToOthers.remove(id);
        shownToSelf.remove(id);
        updateModel(player, null);
    }

    /** После перезагрузки о недоступных шляпах сообщается заново. */
    public void resetWarnings() {
        reported.clear();
    }

    /** Возвращает всем настоящие шлемы: при выключении плагина. */
    public void clearAll() {
        for (Player player : Bukkit.getOnlinePlayers()) {
            hats.remove(player.getUniqueId());
            refresh(player);
            updateModel(player, null);
        }
        reported.clear();
    }

    private ItemStack visibleHat(Player wearer) {
        ItemStack hat = hats.get(wearer.getUniqueId());
        if (hat == null || wearer.getGameMode() == GameMode.SPECTATOR) {
            return null;
        }
        Settings settings = plugin.settings();
        if (settings.hatHideWhenInvisible()
                && (wearer.isInvisible() || wearer.hasPotionEffect(PotionEffectType.INVISIBILITY))) {
            return null;
        }
        if (settings.hatOnlyWithoutHelmet() && !realHelmet(wearer).isEmpty()) {
            return null;
        }
        return hat;
    }

    private static ItemStack realHelmet(Player player) {
        ItemStack helmet = player.getInventory().getHelmet();
        return helmet == null ? ItemStack.empty() : helmet;
    }

    private ItemStack build(String spec) {
        ItemStack item = plugin.items().resolve(spec);
        if (item == null) {
            return null;
        }
        item.setAmount(1);
        // Без модели брони предмет рисуется на голове как есть, даже если это шлем;
        // без наложения тыква не закрывает экран.
        item.editMeta(meta -> {
            EquippableComponent equippable = meta.getEquippable();
            equippable.setSlot(EquipmentSlot.HEAD);
            equippable.setModel(null);
            equippable.setCameraOverlay(null);
            meta.setEquippable(equippable);
        });
        return item;
    }

    private void updateModel(Player player, String model) {
        UUID id = player.getUniqueId();
        ModelHat current = models.get(id);
        if (current != null && current.name().equals(model)) {
            return;
        }
        BetterModelHook hook = hook();
        if (current != null) {
            models.remove(id);
            if (hook != null) {
                hook.detach(current.tracker());
            }
        }
        if (model == null || hook == null) {
            return;
        }
        Object tracker = hook.attach(player, model);
        if (tracker != null) {
            models.put(id, new ModelHat(model, tracker));
        }
    }

    private BetterModelHook hook() {
        if (betterModel == null) {
            betterModel = BetterModelHook.create(plugin.getLogger());
        }
        return betterModel;
    }

    private void refreshLater(Player player) {
        if (hats.containsKey(player.getUniqueId()) || shownToOthers.contains(player.getUniqueId())) {
            // Через два тика: признак невидимости сервер обновляет позже, чем снимает эффект.
            Bukkit.getScheduler().runTaskLater(plugin, () -> {
                if (player.isOnline()) {
                    refresh(player);
                }
            }, 2L);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onTrack(PlayerTrackEntityEvent event) {
        if (!(event.getEntity() instanceof Player wearer) || !hats.containsKey(wearer.getUniqueId())) {
            return;
        }
        Player viewer = event.getPlayer();
        // Настоящая экипировка уходит зрителю сразу после события, шляпа — следом.
        Bukkit.getScheduler().runTask(plugin, () -> {
            if (!viewer.isOnline() || !wearer.isOnline()) {
                return;
            }
            ItemStack hat = visibleHat(wearer);
            if (hat != null) {
                viewer.sendEquipmentChange(wearer, EquipmentSlot.HEAD, hat);
            }
        });
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onArmorChange(PlayerArmorChangeEvent event) {
        if (event.getSlot() == EquipmentSlot.HEAD) {
            refreshLater(event.getPlayer());
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onGameMode(PlayerGameModeChangeEvent event) {
        refreshLater(event.getPlayer());
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onPotion(EntityPotionEffectEvent event) {
        if (event.getEntity() instanceof Player player
                && PotionEffectType.INVISIBILITY.equals(event.getModifiedType())) {
            refreshLater(player);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onRespawn(PlayerRespawnEvent event) {
        refreshLater(event.getPlayer());
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onWorldChange(PlayerChangedWorldEvent event) {
        refreshLater(event.getPlayer());
    }
}
