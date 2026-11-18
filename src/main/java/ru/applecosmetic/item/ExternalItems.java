package ru.applecosmetic.item;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Logger;
import org.bukkit.Bukkit;
import org.bukkit.event.Event;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.Plugin;

/**
 * Предметы из сторонних плагинов. Их API вызывается через рефлексию, чтобы
 * сборка не зависела от чужих репозиториев, а плагин работал и без них.
 */
final class ExternalItems {

    enum Provider {
        ITEMS_ADDER("ItemsAdder", "dev.lone.itemsadder.api.CustomStack", "getInstance", "getItemStack",
                "dev.lone.itemsadder.api.Events.ItemsAdderLoadDataEvent", "itemsadder", "ia"),
        NEXO("Nexo", "com.nexomc.nexo.api.NexoItems", "itemFromId", "build",
                "com.nexomc.nexo.api.events.NexoItemsLoadedEvent", "nexo"),
        ORAXEN("Oraxen", "io.th0rgal.oraxen.api.OraxenItems", "getItemById", "build",
                "io.th0rgal.oraxen.api.events.OraxenItemsLoadedEvent", "oraxen"),
        CRAFT_ENGINE("CraftEngine", "net.momirealms.craftengine.bukkit.api.CraftEngineItems", "byId",
                "buildBukkitItem", "net.momirealms.craftengine.bukkit.api.event.CraftEngineReloadEvent",
                "craftengine", "ce");

        final String plugin;
        final String apiClass;
        final String lookupMethod;
        final String buildMethod;
        final String loadEvent;
        final String[] prefixes;

        Provider(String plugin, String apiClass, String lookupMethod, String buildMethod, String loadEvent,
                 String... prefixes) {
            this.plugin = plugin;
            this.apiClass = apiClass;
            this.lookupMethod = lookupMethod;
            this.buildMethod = buildMethod;
            this.loadEvent = loadEvent;
            this.prefixes = prefixes;
        }

        static Provider byPrefix(String prefix) {
            for (Provider provider : values()) {
                for (String candidate : provider.prefixes) {
                    if (candidate.equals(prefix)) {
                        return provider;
                    }
                }
            }
            return null;
        }
    }

    private final Logger logger;
    // Событие загрузки ItemsAdder приходит не из основного потока.
    private final Set<Provider> ready = ConcurrentHashMap.newKeySet();
    private final Set<String> reported = ConcurrentHashMap.newKeySet();

    ExternalItems(Logger logger) {
        this.logger = logger;
    }

    /** После сброса о недоступных предметах сообщается заново. */
    void resetWarnings() {
        reported.clear();
    }

    ItemStack fetch(Provider provider, String id, String spec) {
        if (!Bukkit.getPluginManager().isPluginEnabled(provider.plugin)) {
            if (reported.add(provider.plugin)) {
                logger.info("Плагин " + provider.plugin + " не установлен: его предметы («" + spec
                        + "» и другие) заменяются запасными вариантами.");
            }
            return null;
        }
        try {
            Method lookup = Class.forName(provider.apiClass).getMethod(provider.lookupMethod, String.class);
            Object found = lookup.invoke(null, id);
            Object built = found == null ? null : lookup.getReturnType().getMethod(provider.buildMethod).invoke(found);
            if (built instanceof ItemStack stack && !stack.isEmpty()) {
                ready.add(provider);
                return stack.clone();
            }
            // Пока плагин не сообщил, что загрузил предметы, их отсутствие — не ошибка.
            if (ready.contains(provider) && reported.add(spec)) {
                logger.warning("Предмет «" + spec + "» не найден в " + provider.plugin + ".");
            }
        } catch (InvocationTargetException e) {
            if (reported.add(spec)) {
                logger.warning("Не удалось получить предмет «" + spec + "» из " + provider.plugin + ": " + e.getCause());
            }
        } catch (ReflectiveOperationException | LinkageError e) {
            if (reported.add(provider.plugin)) {
                logger.warning("Версия " + provider.plugin + " не поддерживается, предмет «" + spec
                        + "» недоступен: " + e);
            }
        }
        return null;
    }

    /** Подписывается на события «предметы загружены», чтобы обновить облики после загрузки или перезагрузки. */
    void registerLoadHooks(Plugin owner, Runnable onLoaded) {
        Listener marker = new Listener() {
        };
        for (Provider provider : Provider.values()) {
            if (Bukkit.getPluginManager().getPlugin(provider.plugin) == null) {
                continue;
            }
            try {
                Class<? extends Event> event = Class.forName(provider.loadEvent).asSubclass(Event.class);
                Bukkit.getPluginManager().registerEvent(event, marker, EventPriority.MONITOR, (listener, fired) -> {
                    ready.add(provider);
                    onLoaded.run();
                }, owner);
                logger.info("Подключена поддержка " + provider.plugin + ".");
            } catch (ReflectiveOperationException | LinkageError | ClassCastException e) {
                logger.warning("Не удалось подписаться на загрузку предметов " + provider.plugin + ": " + e);
            }
        }
    }
}
