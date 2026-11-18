package ru.applecosmetic;

import java.util.ArrayList;
import java.util.List;
import org.bukkit.Bukkit;
import org.bukkit.command.PluginCommand;
import org.bukkit.entity.Player;
import org.bukkit.plugin.PluginManager;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;
import ru.applecosmetic.command.CosmeticsCommand;
import ru.applecosmetic.cosmetic.CosmeticManager;
import ru.applecosmetic.cosmetic.CosmeticRegistry;
import ru.applecosmetic.data.PlayerDataStore;
import ru.applecosmetic.effect.EffectService;
import ru.applecosmetic.effect.TrailService;
import ru.applecosmetic.hat.HatService;
import ru.applecosmetic.item.ItemResolver;
import ru.applecosmetic.menu.MenuManager;
import ru.applecosmetic.pack.PackInstaller;
import ru.applecosmetic.skin.SkinListener;
import ru.applecosmetic.skin.SkinService;

public final class AppleCosmeticPlugin extends JavaPlugin {

    private final Settings settings = new Settings();
    private final List<BukkitTask> tasks = new ArrayList<>();
    private Messages messages;
    private ItemResolver items;
    private CosmeticRegistry registry;
    private CosmeticManager cosmetics;
    private PlayerDataStore store;
    private SkinService skins;
    private HatService hats;
    private EffectService effects;
    private TrailService trails;
    private MenuManager menus;

    @Override
    public void onLoad() {
        // До включения ItemsAdder и BetterModel, чтобы они увидели модели уже при этом запуске.
        saveDefaultConfig();
        installModels(true);
    }

    @Override
    public void onEnable() {
        messages = new Messages(this);
        items = new ItemResolver(this);
        registry = new CosmeticRegistry(this);
        cosmetics = new CosmeticManager(this);
        store = new PlayerDataStore(this);
        skins = new SkinService(this);
        hats = new HatService(this);
        effects = new EffectService(this);
        trails = new TrailService(this);
        menus = new MenuManager(this);
        loadConfiguration();

        PluginManager pluginManager = getServer().getPluginManager();
        pluginManager.registerEvents(new PlayerListener(this), this);
        pluginManager.registerEvents(new SkinListener(this), this);
        pluginManager.registerEvents(hats, this);
        pluginManager.registerEvents(effects, this);
        pluginManager.registerEvents(trails, this);
        pluginManager.registerEvents(menus, this);
        items.registerLoadHooks(this, this::onExternalItemsLoaded);

        PluginCommand command = getCommand("cosmetics");
        if (command != null) {
            CosmeticsCommand executor = new CosmeticsCommand(this);
            command.setExecutor(executor);
            command.setTabCompleter(executor);
        }

        startTasks();
        // При самом первом запуске ItemsAdder и BetterModel создают свои папки уже после включения.
        Bukkit.getScheduler().runTask(this, () -> installModels(false));
        // Если плагин включён при игроках на сервере.
        applyToOnlinePlayers();
    }

    @Override
    public void onDisable() {
        tasks.forEach(BukkitTask::cancel);
        tasks.clear();
        if (store == null) {
            return;
        }
        menus.closeAll();
        skins.restoreAll();
        hats.clearAll();
        trails.clear();
        store.shutdown();
    }

    /** Перечитывает все файлы и заново применяет косметику игрокам. */
    public void reload() {
        menus.closeAll();
        skins.restoreAll();
        loadConfiguration();
        startTasks();
        applyToOnlinePlayers();
    }

    private void loadConfiguration() {
        saveDefaultConfig();
        reloadConfig();
        settings.load(getConfig(), getLogger());
        messages.load();
        installModels(false);
        items.invalidate();
        skins.invalidate();
        hats.resetWarnings();
        registry.load();
    }

    private void installModels(boolean beforeEnable) {
        if (getConfig().getBoolean("models.auto-install", true)) {
            new PackInstaller(getFile(), getLogger()).install(beforeEnable);
        }
    }

    private void startTasks() {
        tasks.forEach(BukkitTask::cancel);
        tasks.clear();
        tasks.add(Bukkit.getScheduler().runTaskTimer(this, () -> {
            skins.flushDirty();
            trails.tick();
        }, 1L, 1L));
        int skinInterval = settings.skinSyncInterval();
        tasks.add(Bukkit.getScheduler().runTaskTimer(this, () -> {
            for (Player player : Bukkit.getOnlinePlayers()) {
                cosmetics.validate(player);
                skins.sync(player);
            }
        }, skinInterval, skinInterval));
        int hatInterval = settings.hatRefreshInterval();
        tasks.add(Bukkit.getScheduler().runTaskTimer(this, hats::refreshAll, hatInterval, hatInterval));
    }

    private void applyToOnlinePlayers() {
        for (Player player : Bukkit.getOnlinePlayers()) {
            cosmetics.validate(player);
            skins.sync(player);
            hats.update(player);
        }
    }

    /** ItemsAdder сообщает о загрузке предметов не из основного потока. */
    private void onExternalItemsLoaded() {
        items.invalidate();
        if (!isEnabled()) {
            return;
        }
        Bukkit.getScheduler().runTask(this, () -> {
            skins.invalidate();
            hats.resetWarnings();
            menus.closeAll();
            applyToOnlinePlayers();
        });
    }

    public Settings settings() {
        return settings;
    }

    public Messages messages() {
        return messages;
    }

    public ItemResolver items() {
        return items;
    }

    public CosmeticRegistry registry() {
        return registry;
    }

    public CosmeticManager cosmetics() {
        return cosmetics;
    }

    public PlayerDataStore store() {
        return store;
    }

    public SkinService skins() {
        return skins;
    }

    public HatService hats() {
        return hats;
    }

    public EffectService effects() {
        return effects;
    }

    public TrailService trails() {
        return trails;
    }

    public MenuManager menus() {
        return menus;
    }
}
