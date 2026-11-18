package ru.applecosmetic.cosmetic;

import org.bukkit.Material;
import org.bukkit.Tag;

public enum Category {

    SWORD("sword", "cosmetics/swords.yml", "items", Kind.SKIN, Material.DIAMOND_SWORD),
    PICKAXE("pickaxe", "cosmetics/pickaxes.yml", "items", Kind.SKIN, Material.DIAMOND_PICKAXE),
    TOTEM("totem", "cosmetics/totems.yml", "items", Kind.SKIN, Material.TOTEM_OF_UNDYING),
    HAT("hat", "cosmetics/hats.yml", "items", Kind.HAT, Material.LEATHER_HELMET),
    KILL("kill", "effects/kill.yml", "effects", Kind.EFFECT, Material.WITHER_SKELETON_SKULL),
    CRIT("crit", "effects/crit.yml", "effects", Kind.EFFECT, Material.BLAZE_POWDER),
    PROJECTILE("projectile", "effects/projectile.yml", "effects", Kind.TRAIL, Material.BOW),
    DEATH("death", "effects/death.yml", "effects", Kind.EFFECT, Material.SKELETON_SKULL);

    public enum Kind {
        /** Облик предмета в инвентаре. */
        SKIN,
        /** Шляпа на голове. */
        HAT,
        /** Разовый эффект из частиц. */
        EFFECT,
        /** След за снарядом. */
        TRAIL
    }

    private final String key;
    private final String file;
    private final String rootKey;
    private final Kind kind;
    private final Material defaultIcon;

    Category(String key, String file, String rootKey, Kind kind, Material defaultIcon) {
        this.key = key;
        this.file = file;
        this.rootKey = rootKey;
        this.kind = kind;
        this.defaultIcon = defaultIcon;
    }

    /** Ключ категории: используется в правах, конфиге меню и файлах игроков. */
    public String key() {
        return key;
    }

    public String file() {
        return file;
    }

    public String rootKey() {
        return rootKey;
    }

    public Kind kind() {
        return kind;
    }

    public Material defaultIcon() {
        return defaultIcon;
    }

    public boolean previewable() {
        return kind == Kind.EFFECT || kind == Kind.TRAIL;
    }

    /** Категория облика, к которой относится предмет, или null. */
    public static Category skinFor(Material material) {
        if (material == Material.TOTEM_OF_UNDYING) {
            return TOTEM;
        }
        if (Tag.ITEMS_SWORDS.isTagged(material)) {
            return SWORD;
        }
        if (Tag.ITEMS_PICKAXES.isTagged(material)) {
            return PICKAXE;
        }
        return null;
    }
}
