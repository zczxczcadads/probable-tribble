package ru.applecosmetic.effect;

import java.util.List;
import org.bukkit.Location;
import org.bukkit.NamespacedKey;
import org.bukkit.SoundCategory;
import org.bukkit.World;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.Firework;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Mob;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageByEntityEvent;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.inventory.meta.FireworkMeta;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.scheduler.BukkitRunnable;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.Settings;
import ru.applecosmetic.cosmetic.Category;
import ru.applecosmetic.cosmetic.Cosmetic;

/** Проигрывает эффекты убийства, смерти и критического удара. */
public final class EffectService implements Listener {

    private final AppleCosmeticPlugin plugin;
    private final NamespacedKey fireworkKey;

    public EffectService(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
        this.fireworkKey = new NamespacedKey(plugin, "firework");
    }

    /**
     * @param origin точка у ног цели
     * @param only   единственный зритель (предпросмотр); null — видят все поблизости
     */
    public void play(EffectDefinition effect, Location origin, Player only) {
        World world = origin.getWorld();
        if (world == null) {
            return;
        }
        for (SoundSpec sound : effect.sounds()) {
            sound.play(origin, only);
        }
        if (effect.lightning()) {
            if (only == null) {
                world.strikeLightningEffect(origin);
            } else {
                // Молнию нельзя показать одному игроку, поэтому в предпросмотре только гром.
                only.playSound(origin, "entity.lightning_bolt.thunder", SoundCategory.WEATHER, 1.0f, 1.0f);
                only.playSound(origin, "entity.lightning_bolt.impact", SoundCategory.WEATHER, 1.0f, 1.0f);
            }
        }
        if (effect.firework() != null) {
            launch(effect.firework(), origin, only);
        }
        if (effect.layers().isEmpty()) {
            return;
        }

        Animation.Frame frame = new Animation.Frame(world, only == null ? null : List.of(only),
                origin.getX(), origin.getY(), origin.getZ());
        int total = effect.ticks();
        new BukkitRunnable() {
            private int tick;

            @Override
            public void run() {
                try {
                    for (EffectLayer layer : effect.layers()) {
                        int local = tick - layer.delay();
                        if (local >= 0 && local < layer.duration()) {
                            frame.tick = local;
                            frame.progress = (local + 1.0) / layer.duration();
                            layer.animation().render(layer, frame);
                        }
                    }
                } catch (RuntimeException e) {
                    plugin.getLogger().warning("Эффект остановлен из-за ошибки: " + e);
                    cancel();
                    return;
                }
                if (++tick >= total) {
                    cancel();
                }
            }
        }.runTaskTimer(plugin, 0L, 1L);
    }

    private void launch(FireworkSpec spec, Location origin, Player only) {
        Location at = origin.clone().add(0, 1.2, 0);
        Firework firework = at.getWorld().spawn(at, Firework.class, spawned -> {
            FireworkMeta meta = spawned.getFireworkMeta();
            meta.addEffect(spec.effect());
            spawned.setFireworkMeta(meta);
            spawned.setSilent(true);
            spawned.getPersistentDataContainer().set(fireworkKey, PersistentDataType.BYTE, (byte) 1);
            if (only != null) {
                spawned.setVisibleByDefault(false);
            }
        });
        if (only != null) {
            only.showEntity(plugin, firework);
        }
        firework.detonate();
    }

    private void playSelected(Player owner, Category category, Location at) {
        Cosmetic cosmetic = plugin.cosmetics().selected(owner, category);
        if (cosmetic != null && cosmetic.effect() != null) {
            play(cosmetic.effect(), at, null);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onDeath(EntityDeathEvent event) {
        LivingEntity victim = event.getEntity();
        Location at = victim.getLocation();
        if (victim instanceof Player dead) {
            playSelected(dead, Category.DEATH, at);
        }
        Player killer = victim.getKiller();
        if (killer == null || killer.equals(victim)) {
            return;
        }
        Settings settings = plugin.settings();
        boolean allowed = victim instanceof Player ? settings.killOnPlayers()
                : victim instanceof Mob && settings.killOnMobs();
        if (allowed) {
            playSelected(killer, Category.KILL, at);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onCriticalHit(EntityDamageByEntityEvent event) {
        if (!event.isCritical() || !(event.getDamager() instanceof Player attacker)
                || !(event.getEntity() instanceof LivingEntity victim) || victim instanceof ArmorStand) {
            return;
        }
        Settings settings = plugin.settings();
        if (victim instanceof Player ? settings.critOnPlayers() : settings.critOnMobs()) {
            playSelected(attacker, Category.CRIT, victim.getLocation());
        }
    }

    @EventHandler(priority = EventPriority.LOW, ignoreCancelled = true)
    public void onFireworkDamage(EntityDamageByEntityEvent event) {
        if (event.getDamager() instanceof Firework firework
                && firework.getPersistentDataContainer().has(fireworkKey)) {
            event.setCancelled(true);
        }
    }
}
