package ru.applecosmetic.command;

import java.util.List;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabExecutor;
import org.bukkit.entity.Player;
import ru.applecosmetic.AppleCosmeticPlugin;

/** Команда /cosmetics: меню для игроков и reload для администраторов. */
public final class CosmeticsCommand implements TabExecutor {

    private static final String ADMIN = "applecosmetic.admin";

    private final AppleCosmeticPlugin plugin;

    public CosmeticsCommand(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (args.length > 0 && args[0].equalsIgnoreCase("reload")) {
            if (!sender.hasPermission(ADMIN)) {
                plugin.messages().send(sender, "no-permission");
                return true;
            }
            plugin.reload();
            plugin.messages().send(sender, "reloaded");
            return true;
        }
        if (!(sender instanceof Player player)) {
            plugin.messages().send(sender, "only-players");
            return true;
        }
        if (!player.hasPermission("applecosmetic.use")) {
            plugin.messages().send(player, "no-permission");
            return true;
        }
        plugin.menus().openMain(player);
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (args.length == 1 && sender.hasPermission(ADMIN) && "reload".startsWith(args[0].toLowerCase())) {
            return List.of("reload");
        }
        return List.of();
    }
}
