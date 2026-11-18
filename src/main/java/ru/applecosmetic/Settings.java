package ru.applecosmetic;

import java.util.EnumSet;
import java.util.Locale;
import java.util.Set;
import java.util.logging.Logger;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.EntityType;

/** Значения из config.yml, которые читаются часто. */
public final class Settings {

    private boolean requirePermissions;
    private int skinSyncInterval;
    private boolean hatShowToSelf;
    private boolean hatHideWhenInvisible;
    private boolean hatOnlyWithoutHelmet;
    private int hatRefreshInterval;
    private boolean killOnPlayers;
    private boolean killOnMobs;
    private boolean critOnPlayers;
    private boolean critOnMobs;
    private final Set<EntityType> projectileTypes = EnumSet.noneOf(EntityType.class);
    private int projectileMaxTicks;

    public void load(FileConfiguration config, Logger logger) {
        requirePermissions = config.getBoolean("settings.require-permissions", true);
        skinSyncInterval = Math.max(1, config.getInt("skins.sync-interval-ticks", 20));
        hatShowToSelf = config.getBoolean("hats.show-to-self", true);
        hatHideWhenInvisible = config.getBoolean("hats.hide-when-invisible", true);
        hatOnlyWithoutHelmet = config.getBoolean("hats.only-without-helmet", false);
        hatRefreshInterval = Math.max(5, config.getInt("hats.refresh-interval-ticks", 40));
        killOnPlayers = config.getBoolean("effects.kill.players", true);
        killOnMobs = config.getBoolean("effects.kill.mobs", false);
        critOnPlayers = config.getBoolean("effects.crit.players", true);
        critOnMobs = config.getBoolean("effects.crit.mobs", true);
        projectileMaxTicks = Math.max(1, config.getInt("effects.projectile.max-ticks", 200));

        projectileTypes.clear();
        for (String name : config.getStringList("effects.projectile.types")) {
            try {
                projectileTypes.add(EntityType.valueOf(name.trim().toUpperCase(Locale.ROOT)));
            } catch (IllegalArgumentException e) {
                logger.warning("config.yml: неизвестный тип снаряда «" + name + "».");
            }
        }
    }

    public boolean requirePermissions() {
        return requirePermissions;
    }

    public int skinSyncInterval() {
        return skinSyncInterval;
    }

    public boolean hatShowToSelf() {
        return hatShowToSelf;
    }

    public boolean hatHideWhenInvisible() {
        return hatHideWhenInvisible;
    }

    public boolean hatOnlyWithoutHelmet() {
        return hatOnlyWithoutHelmet;
    }

    public int hatRefreshInterval() {
        return hatRefreshInterval;
    }

    public boolean killOnPlayers() {
        return killOnPlayers;
    }

    public boolean killOnMobs() {
        return killOnMobs;
    }

    public boolean critOnPlayers() {
        return critOnPlayers;
    }

    public boolean critOnMobs() {
        return critOnMobs;
    }

    public Set<EntityType> projectileTypes() {
        return projectileTypes;
    }

    public int projectileMaxTicks() {
        return projectileMaxTicks;
    }
}
