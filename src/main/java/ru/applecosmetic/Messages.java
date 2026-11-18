package ru.applecosmetic;

import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import org.bukkit.command.CommandSender;
import org.bukkit.configuration.file.YamlConfiguration;
import ru.applecosmetic.util.Text;

/** Сообщения из messages.yml. */
public final class Messages {

    private final AppleCosmeticPlugin plugin;
    private YamlConfiguration yaml = new YamlConfiguration();

    public Messages(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    public void load() {
        File file = new File(plugin.getDataFolder(), "messages.yml");
        if (!file.exists()) {
            plugin.saveResource("messages.yml", false);
        }
        YamlConfiguration loaded = new YamlConfiguration();
        try {
            loaded.load(file);
        } catch (Exception e) {
            plugin.getLogger().severe("Не удалось прочитать messages.yml: " + e.getMessage());
        }
        // Недостающие строки берутся из файла внутри плагина.
        InputStream bundled = plugin.getResource("messages.yml");
        if (bundled != null) {
            loaded.setDefaults(YamlConfiguration.loadConfiguration(
                    new InputStreamReader(bundled, StandardCharsets.UTF_8)));
        }
        yaml = loaded;
    }

    public String raw(String key) {
        return yaml.getString(key, "");
    }

    public void send(CommandSender target, String key, String... pairs) {
        String raw = raw(key);
        if (raw.isEmpty()) {
            return;
        }
        String text = Text.replace(raw, pairs).replace("{prefix}", raw("prefix"));
        target.sendMessage(Text.parse(text));
    }
}
