package ru.applecosmetic.util;

import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.TextDecoration;
import net.kyori.adventure.text.minimessage.MiniMessage;

/** Разбор текста из конфигов: MiniMessage и привычные коды (&c, &l, &#rrggbb). */
public final class Text {

    private static final MiniMessage MINI = MiniMessage.miniMessage();
    private static final Pattern HEX = Pattern.compile("[&§]#([0-9a-fA-F]{6})");
    private static final Pattern CODE = Pattern.compile("[&§]([0-9a-fk-orA-FK-OR])");
    private static final Map<Character, String> TAGS = Map.ofEntries(
            Map.entry('0', "black"), Map.entry('1', "dark_blue"), Map.entry('2', "dark_green"),
            Map.entry('3', "dark_aqua"), Map.entry('4', "dark_red"), Map.entry('5', "dark_purple"),
            Map.entry('6', "gold"), Map.entry('7', "gray"), Map.entry('8', "dark_gray"),
            Map.entry('9', "blue"), Map.entry('a', "green"), Map.entry('b', "aqua"),
            Map.entry('c', "red"), Map.entry('d', "light_purple"), Map.entry('e', "yellow"),
            Map.entry('f', "white"), Map.entry('k', "obfuscated"), Map.entry('l', "bold"),
            Map.entry('m', "strikethrough"), Map.entry('n', "underlined"), Map.entry('o', "italic"),
            Map.entry('r', "reset"));

    private Text() {
    }

    public static Component parse(String raw) {
        if (raw == null || raw.isEmpty()) {
            return Component.empty();
        }
        return MINI.deserialize(legacyToMini(raw));
    }

    /** Текст для названий и описаний предметов: без курсива, если он не задан явно. */
    public static Component item(String raw) {
        return parse(raw).decorationIfAbsent(TextDecoration.ITALIC, TextDecoration.State.FALSE);
    }

    /** Подставляет значения вида {ключ}; аргументы идут парами «ключ, значение». */
    public static String replace(String raw, String... pairs) {
        String result = raw;
        for (int i = 0; i + 1 < pairs.length; i += 2) {
            result = result.replace('{' + pairs[i] + '}', pairs[i + 1]);
        }
        return result;
    }

    private static String legacyToMini(String raw) {
        if (raw.indexOf('&') < 0 && raw.indexOf('§') < 0) {
            return raw;
        }
        String text = HEX.matcher(raw).replaceAll("<reset><#$1>");
        Matcher matcher = CODE.matcher(text);
        StringBuilder out = new StringBuilder();
        while (matcher.find()) {
            char code = Character.toLowerCase(matcher.group(1).charAt(0));
            String tag = TAGS.get(code);
            // Как и в старых кодах, цвет сбрасывает предыдущее оформление.
            boolean color = code <= 'f' && code != 'r';
            matcher.appendReplacement(out, (color ? "<reset><" : "<") + tag + ">");
        }
        matcher.appendTail(out);
        return out.toString();
    }
}
