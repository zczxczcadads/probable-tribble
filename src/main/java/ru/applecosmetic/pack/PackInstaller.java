package ru.applecosmetic.pack;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Enumeration;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;
import java.util.logging.Logger;
import org.bukkit.Bukkit;
import org.bukkit.plugin.Plugin;

/**
 * Устанавливает встроенные 3D-модели: набор предметов в ItemsAdder и модели шляп в BetterModel.
 * Копируются только недостающие файлы, поэтому правки администратора не затираются.
 */
public final class PackInstaller {

    private static final String ITEMS_ADDER = "pack/itemsadder/";
    private static final String BETTER_MODEL = "pack/bettermodel/";

    private final File jar;
    private final Logger logger;

    public PackInstaller(File jar, Logger logger) {
        this.jar = jar;
        this.logger = logger;
    }

    /**
     * Файлы кладутся только в уже существующие папки contents и models: пока их нет, сторонний
     * плагин ещё не запускался и должен сначала сам создать свои файлы по умолчанию.
     *
     * @param beforeEnable true, пока сторонние плагины ещё не включены и сами увидят новые файлы
     */
    public void install(boolean beforeEnable) {
        int items = copy("ItemsAdder", ITEMS_ADDER, "contents");
        if (items > 0) {
            logger.info("Модели AppleCosmetic добавлены в ItemsAdder (contents/applecosmetic, файлов: " + items
                    + "). Выполните /iazip, чтобы они попали в ресурспак.");
        }
        int hats = copy("BetterModel", BETTER_MODEL, "models");
        if (hats > 0) {
            logger.info("Модели шляп добавлены в BetterModel (models, файлов: " + hats + ")."
                    + (beforeEnable ? "" : " Выполните /bettermodel reload, чтобы они загрузились."));
        }
    }

    private int copy(String pluginName, String prefix, String folder) {
        Plugin target = Bukkit.getPluginManager().getPlugin(pluginName);
        if (target == null) {
            return 0;
        }
        Path root = target.getDataFolder().toPath().toAbsolutePath().normalize();
        if (!Files.isDirectory(root.resolve(folder))) {
            return 0;
        }
        int copied = 0;
        try (JarFile archive = new JarFile(jar)) {
            for (Enumeration<JarEntry> entries = archive.entries(); entries.hasMoreElements(); ) {
                JarEntry entry = entries.nextElement();
                if (entry.isDirectory() || !entry.getName().startsWith(prefix)) {
                    continue;
                }
                Path file = root.resolve(entry.getName().substring(prefix.length())).normalize();
                if (!file.startsWith(root) || Files.exists(file)) {
                    continue;
                }
                Files.createDirectories(file.getParent());
                try (InputStream in = archive.getInputStream(entry)) {
                    Files.copy(in, file);
                }
                copied++;
            }
        } catch (IOException e) {
            logger.warning("Не удалось установить модели в " + pluginName + ": " + e.getMessage());
        }
        return copied;
    }
}
