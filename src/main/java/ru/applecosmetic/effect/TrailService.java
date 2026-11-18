package ru.applecosmetic.effect;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.AbstractArrow;
import org.bukkit.entity.Player;
import org.bukkit.entity.Projectile;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.ProjectileLaunchEvent;
import org.bukkit.scheduler.BukkitRunnable;
import org.bukkit.util.Vector;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.cosmetic.Category;
import ru.applecosmetic.cosmetic.Cosmetic;

/** Рисует следы за снарядами игроков. */
public final class TrailService implements Listener {

    private static final double STEP = 0.5;
    private static final int MAX_STEPS = 8;

    private final AppleCosmeticPlugin plugin;
    private final Map<Projectile, State> active = new HashMap<>();

    public TrailService(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onLaunch(ProjectileLaunchEvent event) {
        Projectile projectile = event.getEntity();
        if (!(projectile.getShooter() instanceof Player shooter)
                || !plugin.settings().projectileTypes().contains(projectile.getType())) {
            return;
        }
        Cosmetic cosmetic = plugin.cosmetics().selected(shooter, Category.PROJECTILE);
        if (cosmetic != null && cosmetic.trail() != null) {
            active.put(projectile, new State(cosmetic.trail(), projectile.getLocation()));
        }
    }

    /** Вызывается каждый тик. */
    public void tick() {
        if (active.isEmpty()) {
            return;
        }
        int maxTicks = plugin.settings().projectileMaxTicks();
        Iterator<Map.Entry<Projectile, State>> iterator = active.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<Projectile, State> entry = iterator.next();
            Projectile projectile = entry.getKey();
            State state = entry.getValue();
            if (!projectile.isValid() || state.age > maxTicks
                    || projectile instanceof AbstractArrow arrow && arrow.isInBlock()) {
                iterator.remove();
                continue;
            }
            Location now = projectile.getLocation();
            if (now.getWorld() == state.last.getWorld()) {
                draw(state, now, null);
            }
            state.last = now;
        }
    }

    public void clear() {
        active.clear();
    }

    /** Показывает след только одному игроку: частицы пролетают перед ним слева направо. */
    public void preview(Player viewer, TrailDefinition trail) {
        Vector forward = forward(viewer);
        Vector right = new Vector(-forward.getZ(), 0, forward.getX());
        Location start = viewer.getEyeLocation().add(forward.clone().multiply(3)).subtract(right.clone().multiply(3));
        State state = new State(trail, start);
        List<Player> receivers = List.of(viewer);
        new BukkitRunnable() {
            private int tick;

            @Override
            public void run() {
                if (!viewer.isOnline() || tick++ >= 20) {
                    cancel();
                    return;
                }
                Location next = state.last.clone().add(right.clone().multiply(0.3));
                draw(state, next, receivers);
                state.last = next;
            }
        }.runTaskTimer(plugin, 0L, 1L);
    }

    /** Направление взгляда без наклона вверх или вниз. */
    public static Vector forward(Player player) {
        double yaw = Math.toRadians(player.getLocation().getYaw());
        return new Vector(-Math.sin(yaw), 0, Math.cos(yaw));
    }

    private void draw(State state, Location to, List<Player> receivers) {
        World world = to.getWorld();
        TrailDefinition trail = state.trail;
        Location from = state.last;
        double dx = to.getX() - from.getX();
        double dy = to.getY() - from.getY();
        double dz = to.getZ() - from.getZ();
        double distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
        int steps = Math.max(1, Math.min(MAX_STEPS, (int) Math.ceil(distance / STEP)));
        double hue = (state.age % 40) / 40.0;

        Vector side = null;
        Vector up = null;
        if (trail.spiral() > 0 && distance > 1.0E-4) {
            Vector direction = new Vector(dx, dy, dz).multiply(1 / distance);
            Vector reference = Math.abs(direction.getY()) > 0.95 ? new Vector(1, 0, 0) : new Vector(0, 1, 0);
            side = direction.getCrossProduct(reference).normalize();
            up = direction.getCrossProduct(side).normalize();
        }

        for (int step = 1; step <= steps; step++) {
            double t = (double) step / steps;
            double x = from.getX() + dx * t;
            double y = from.getY() + dy * t;
            double z = from.getZ() + dz * t;
            if (side == null) {
                trail.particle().spawn(world, receivers, x, y, z, trail.amount(),
                        trail.spread(), trail.spread(), trail.spread(), trail.speed(), hue);
                continue;
            }
            state.angle += 0.55;
            for (int strand = 0; strand < 2; strand++) {
                double angle = state.angle + Math.PI * strand;
                double a = Math.cos(angle) * trail.spiral();
                double b = Math.sin(angle) * trail.spiral();
                trail.particle().spawn(world, receivers,
                        x + side.getX() * a + up.getX() * b,
                        y + side.getY() * a + up.getY() * b,
                        z + side.getZ() * a + up.getZ() * b,
                        trail.amount(), trail.spread(), trail.spread(), trail.spread(), trail.speed(), hue);
            }
        }
        state.age++;
    }

    private static final class State {
        final TrailDefinition trail;
        Location last;
        int age;
        double angle;

        State(TrailDefinition trail, Location last) {
            this.trail = trail;
            this.last = last;
        }
    }
}
