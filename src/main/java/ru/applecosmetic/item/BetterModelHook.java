package ru.applecosmetic.item;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.logging.Logger;
import org.bukkit.Bukkit;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;

/**
 * Закрепляет модели BetterModel на игроках (шляпы вида bettermodel:имя).
 * API вызывается через рефлексию: оно менялось между версиями 1.x и 2.x/3.x.
 */
public final class BetterModelHook {

    private static final String API = "kr.toxicity.model.api.BetterModel";
    private static final String ADAPTER = "kr.toxicity.model.api.bukkit.platform.BukkitAdapter";
    private static final String HIDE_OPTION = "kr.toxicity.model.api.tracker.EntityHideOption";

    private final Logger logger;
    private final Method findModel;
    private final Method adapt;

    private BetterModelHook(Logger logger, Method findModel, Method adapt) {
        this.logger = logger;
        this.findModel = findModel;
        this.adapt = adapt;
    }

    /** Возвращает null, если BetterModel не установлен или его версия не подходит. */
    public static BetterModelHook create(Logger logger) {
        if (!Bukkit.getPluginManager().isPluginEnabled("BetterModel")) {
            return null;
        }
        try {
            Method findModel = Class.forName(API).getMethod("model", String.class);
            Method adapt = null;
            try {
                adapt = Class.forName(ADAPTER).getMethod("adapt", Entity.class);
            } catch (ClassNotFoundException ignored) {
                // BetterModel 1.x принимает сущности Bukkit напрямую.
            }
            return new BetterModelHook(logger, findModel, adapt);
        } catch (ReflectiveOperationException | LinkageError e) {
            logger.warning("Эта версия BetterModel не поддерживается: " + e);
            return null;
        }
    }

    /** Загружена ли в BetterModel модель с таким именем. */
    public boolean hasModel(String model) {
        try {
            return findModel.invoke(null, model) instanceof Optional<?> optional && optional.isPresent();
        } catch (ReflectiveOperationException | LinkageError e) {
            return false;
        }
    }

    /** Закрепляет модель на игроке и возвращает её трекер или null при ошибке. */
    public Object attach(Player player, String model) {
        try {
            Object found = findModel.invoke(null, model);
            if (!(found instanceof Optional<?> optional) || optional.isEmpty()) {
                logger.warning("Модель BetterModel «" + model + "» не найдена.");
                return null;
            }
            Object renderer = optional.get();
            Object target = adapt != null ? adapt.invoke(null, player) : player;
            Object tracker = create(renderer, target);
            if (tracker == null) {
                logger.warning("Эта версия BetterModel не поддерживается: не найден метод getOrCreate.");
                return null;
            }
            if (!keepEntityVisible(tracker)) {
                detach(tracker);
                logger.warning("Модель «" + model + "» не закреплена: эта версия BetterModel скрыла бы игрока.");
                return null;
            }
            return tracker;
        } catch (InvocationTargetException e) {
            logger.warning("BetterModel не смог закрепить модель «" + model + "»: " + e.getCause());
        } catch (ReflectiveOperationException | LinkageError e) {
            logger.warning("Эта версия BetterModel не поддерживается: " + e);
        }
        return null;
    }

    private Object create(Object renderer, Object target) throws ReflectiveOperationException {
        Method simple = null;
        for (Method method : renderer.getClass().getMethods()) {
            Class<?>[] types = method.getParameterTypes();
            if (!method.getName().equals("getOrCreate") || types.length == 0 || !types[0].isInstance(target)) {
                continue;
            }
            if (types.length == 3 && types[1].getSimpleName().equals("TrackerModifier")
                    && types[2] == Consumer.class) {
                // Настройка до появления модели: иначе игрок на мгновение пропадает у зрителей.
                Consumer<Object> beforeSpawn = this::keepEntityVisible;
                return method.invoke(renderer, target, types[1].getField("DEFAULT").get(null), beforeSpawn);
            }
            if (types.length == 1) {
                simple = method;
            }
        }
        return simple == null ? null : simple.invoke(renderer, target);
    }

    /** По умолчанию BetterModel скрывает саму сущность; игрок должен остаться видимым. */
    private boolean keepEntityVisible(Object tracker) {
        try {
            Class<?> hideOption = Class.forName(HIDE_OPTION);
            tracker.getClass().getMethod("hideOption", hideOption)
                    .invoke(tracker, hideOption.getField("FALSE").get(null));
            return true;
        } catch (ReflectiveOperationException | LinkageError e) {
            return false;
        }
    }

    public void detach(Object tracker) {
        try {
            tracker.getClass().getMethod("close").invoke(tracker);
        } catch (ReflectiveOperationException | LinkageError e) {
            logger.warning("Не удалось убрать модель BetterModel: " + e);
        }
    }

    public boolean isClosed(Object tracker) {
        try {
            return Boolean.TRUE.equals(tracker.getClass().getMethod("isClosed").invoke(tracker));
        } catch (ReflectiveOperationException | LinkageError e) {
            return false;
        }
    }
}
