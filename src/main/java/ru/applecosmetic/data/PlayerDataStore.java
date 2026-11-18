package ru.applecosmetic.data;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import org.bukkit.configuration.file.YamlConfiguration;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.cosmetic.Category;

/** Выбранная игроками косметика: по файлу players/&lt;uuid&gt;.yml на игрока. */
public final class PlayerDataStore {

    private final AppleCosmeticPlugin plugin;
    private final File folder;
    private final Map<UUID, Map<Category, String>> loaded = new HashMap<>();
    // Один поток, чтобы записи одного игрока не обгоняли друг друга.
    private final ExecutorService writer = Executors.newSingleThreadExecutor(task -> {
        Thread thread = new Thread(task, "AppleCosmetic-Storage");
        thread.setDaemon(true);
        return thread;
    });

    public PlayerDataStore(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
        this.folder = new File(plugin.getDataFolder(), "players");
    }

    /** Выбор игрока по категориям; при первом обращении читается с диска. */
    public Map<Category, String> get(UUID id) {
        return loaded.computeIfAbsent(id, this::read);
    }

    public void save(UUID id) {
        Map<Category, String> data = loaded.get(id);
        if (data != null) {
            Map<Category, String> snapshot = new EnumMap<>(data);
            writer.execute(() -> write(id, snapshot));
        }
    }

    public void unload(UUID id) {
        loaded.remove(id);
    }

    public void shutdown() {
        writer.shutdown();
        try {
            if (!writer.awaitTermination(5, TimeUnit.SECONDS)) {
                plugin.getLogger().warning("Не все данные игроков успели сохраниться.");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private File file(UUID id) {
        return new File(folder, id + ".yml");
    }

    private Map<Category, String> read(UUID id) {
        Map<Category, String> data = new EnumMap<>(Category.class);
        File file = file(id);
        if (!file.isFile()) {
            return data;
        }
        YamlConfiguration yaml = new YamlConfiguration();
        try {
            yaml.load(file);
        } catch (Exception e) {
            plugin.getLogger().warning("Не удалось прочитать данные игрока " + id + ": " + e.getMessage());
            return data;
        }
        for (Category category : Category.values()) {
            String value = yaml.getString(category.key());
            if (value != null && !value.isBlank()) {
                data.put(category, value.toLowerCase(Locale.ROOT));
            }
        }
        return data;
    }

    private void write(UUID id, Map<Category, String> snapshot) {
        Path target = file(id).toPath();
        try {
            if (snapshot.isEmpty()) {
                Files.deleteIfExists(target);
                return;
            }
            YamlConfiguration yaml = new YamlConfiguration();
            snapshot.forEach((category, value) -> yaml.set(category.key(), value));
            Files.createDirectories(folder.toPath());
            // Сначала во временный файл, чтобы сбой не оставил половину записи.
            Path temporary = folder.toPath().resolve(id + ".yml.tmp");
            Files.writeString(temporary, yaml.saveToString(), StandardCharsets.UTF_8);
            Files.move(temporary, target, StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            plugin.getLogger().warning("Не удалось сохранить данные игрока " + id + ": " + e.getMessage());
        }
    }
}
