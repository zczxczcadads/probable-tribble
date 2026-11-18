package ru.applecosmetic.cosmetic;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.bukkit.entity.Player;
import ru.applecosmetic.AppleCosmeticPlugin;

/** Выбор косметики игроками и проверка прав на неё. */
public final class CosmeticManager {

    private final AppleCosmeticPlugin plugin;

    public CosmeticManager(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    public boolean has(Player player, Cosmetic cosmetic) {
        if (!plugin.settings().requirePermissions() || cosmetic.permission().isEmpty()) {
            return true;
        }
        return player.hasPermission("applecosmetic.all")
                || player.hasPermission("applecosmetic." + cosmetic.category().key() + ".*")
                || player.hasPermission(cosmetic.permission());
    }

    public int owned(Player player, Category category) {
        int count = 0;
        for (Cosmetic cosmetic : plugin.registry().list(category)) {
            if (has(player, cosmetic)) {
                count++;
            }
        }
        return count;
    }

    /** Выбранная косметика или null. Выбор, которого больше нет в конфиге, не действует, но и не стирается. */
    public Cosmetic selected(Player player, Category category) {
        String id = plugin.store().get(player.getUniqueId()).get(category);
        return id == null ? null : plugin.registry().get(category, id);
    }

    public boolean isSelected(Player player, Cosmetic cosmetic) {
        return cosmetic.id().equals(plugin.store().get(player.getUniqueId()).get(cosmetic.category()));
    }

    public void select(Player player, Cosmetic cosmetic) {
        plugin.store().get(player.getUniqueId()).put(cosmetic.category(), cosmetic.id());
        plugin.store().save(player.getUniqueId());
        apply(player, cosmetic.category());
    }

    public boolean unselect(Player player, Category category) {
        if (plugin.store().get(player.getUniqueId()).remove(category) == null) {
            return false;
        }
        plugin.store().save(player.getUniqueId());
        apply(player, category);
        return true;
    }

    /** Снимает всю косметику и возвращает, было ли что снимать. */
    public boolean resetAll(Player player) {
        Map<Category, String> data = plugin.store().get(player.getUniqueId());
        if (data.isEmpty()) {
            return false;
        }
        List<Category> categories = new ArrayList<>(data.keySet());
        data.clear();
        plugin.store().save(player.getUniqueId());
        categories.forEach(category -> apply(player, category));
        return true;
    }

    /** Снимает косметику, право на которую игрок потерял. */
    public void validate(Player player) {
        Map<Category, String> data = plugin.store().get(player.getUniqueId());
        if (data.isEmpty()) {
            return;
        }
        List<Category> revoked = new ArrayList<>();
        for (Iterator<Map.Entry<Category, String>> iterator = data.entrySet().iterator(); iterator.hasNext(); ) {
            Map.Entry<Category, String> entry = iterator.next();
            Category category = entry.getKey();
            Cosmetic cosmetic = plugin.registry().get(category, entry.getValue());
            if (cosmetic != null && !has(player, cosmetic)) {
                // Запись EnumMap нельзя читать после удаления.
                iterator.remove();
                revoked.add(category);
                plugin.messages().send(player, "lost-access", "name", cosmetic.name());
            }
        }
        if (!revoked.isEmpty()) {
            plugin.store().save(player.getUniqueId());
            revoked.forEach(category -> apply(player, category));
        }
    }

    /** Название категории для заголовков и сообщений. */
    public String title(Category category) {
        return plugin.getConfig().getString("menu.main.categories." + category.key() + ".title", category.key());
    }

    private void apply(Player player, Category category) {
        switch (category.kind()) {
            case SKIN -> plugin.skins().sync(player);
            case HAT -> plugin.hats().update(player);
            default -> {
                // Эффекты читают выбор в момент срабатывания.
            }
        }
    }
}
