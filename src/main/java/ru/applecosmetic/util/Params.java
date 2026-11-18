package ru.applecosmetic.util;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import org.bukkit.Color;
import org.bukkit.configuration.ConfigurationSection;

/** Параметры из YAML: одинаково читает и секцию, и запись вида { ключ: значение }. */
public final class Params {

    private final Map<?, ?> values;

    private Params(Map<?, ?> values) {
        this.values = values;
    }

    public static Params of(Object source) {
        if (source instanceof ConfigurationSection section) {
            return new Params(section.getValues(false));
        }
        if (source instanceof Map<?, ?> map) {
            return new Params(map);
        }
        return new Params(Map.of());
    }

    public boolean has(String key) {
        return values.get(key) != null;
    }

    public String string(String key, String fallback) {
        Object value = values.get(key);
        return value == null ? fallback : value.toString();
    }

    public int integer(String key, int fallback) {
        return values.get(key) instanceof Number number ? number.intValue() : fallback;
    }

    public double decimal(String key, double fallback) {
        return values.get(key) instanceof Number number ? number.doubleValue() : fallback;
    }

    public boolean flag(String key, boolean fallback) {
        return values.get(key) instanceof Boolean bool ? bool : fallback;
    }

    public List<String> strings(String key) {
        List<String> result = new ArrayList<>();
        Object value = values.get(key);
        if (value instanceof List<?> list) {
            for (Object entry : list) {
                result.add(String.valueOf(entry));
            }
        } else if (value != null) {
            result.add(value.toString());
        }
        return result;
    }

    public Color color(String key, Color fallback) {
        Color color = parseColor(string(key, null));
        return color == null ? fallback : color;
    }

    /** Цвет в формате #RRGGBB; null, если строка не является цветом. */
    public static Color parseColor(String raw) {
        if (raw == null) {
            return null;
        }
        String hex = raw.trim().toLowerCase(Locale.ROOT);
        if (hex.startsWith("#")) {
            hex = hex.substring(1);
        }
        if (!hex.matches("[0-9a-f]{6}")) {
            return null;
        }
        return Color.fromRGB(Integer.parseInt(hex, 16));
    }
}
