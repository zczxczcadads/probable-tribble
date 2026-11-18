package ru.applecosmetic.effect;

import java.util.List;
import java.util.Locale;
import java.util.concurrent.ThreadLocalRandom;
import java.util.function.Consumer;
import org.bukkit.Color;
import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.World;
import org.bukkit.block.data.BlockData;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import ru.applecosmetic.util.Params;

/** Частица вместе с её данными (цвет, блок, предмет и т. д.). */
public final class ParticleSpec {

    private static final int MAX_RAINBOW_BATCH = 100;

    private final Particle particle;
    private final Object data;
    private final boolean rainbow;
    private final float size;

    private ParticleSpec(Particle particle, Object data, boolean rainbow, float size) {
        this.particle = particle;
        this.data = data;
        this.rainbow = rainbow;
        this.size = size;
    }

    /** Возвращает null и сообщает причину, если частицу нельзя использовать. */
    public static ParticleSpec parse(Params params, Consumer<String> warn) {
        String name = params.string("particle", null);
        if (name == null) {
            warn.accept("не указана частица (particle)");
            return null;
        }
        Particle particle;
        try {
            particle = Particle.valueOf(name.trim().toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            warn.accept("неизвестная частица «" + name + "»");
            return null;
        }

        Color color = params.color("color", Color.WHITE);
        float size = (float) Math.max(0.1, Math.min(4.0, params.decimal("size", 1.0)));
        Class<?> type = particle.getDataType();
        boolean tintable = true;
        Object data;
        if (type == Void.class) {
            data = null;
            tintable = false;
        } else if (type == Particle.DustOptions.class) {
            data = new Particle.DustOptions(color, size);
        } else if (type == Particle.DustTransition.class) {
            data = new Particle.DustTransition(color, params.color("to-color", Color.WHITE), size);
        } else if (type == Color.class) {
            data = color;
        } else if (type == Particle.Spell.class) {
            data = new Particle.Spell(color, (float) params.decimal("power", 1.0));
        } else if (type == BlockData.class) {
            Material material = material(params);
            if (material == null || !material.isBlock()) {
                warn.accept("для частицы «" + name + "» нужен блок в поле material");
                return null;
            }
            data = material.createBlockData();
            tintable = false;
        } else if (type == ItemStack.class) {
            Material material = material(params);
            if (material == null || !material.isItem() || material.isAir()) {
                warn.accept("для частицы «" + name + "» нужен предмет в поле material");
                return null;
            }
            data = new ItemStack(material);
            tintable = false;
        } else if (type == Float.class) {
            data = (float) params.decimal("power", particle == Particle.SCULK_CHARGE ? 0.0 : 1.0);
            tintable = false;
        } else if (type == Integer.class) {
            data = params.integer("delay", 0);
            tintable = false;
        } else {
            warn.accept("частица «" + name + "» не поддерживается");
            return null;
        }
        return new ParticleSpec(particle, data, tintable && params.flag("rainbow", false), size);
    }

    private static Material material(Params params) {
        String name = params.string("material", null);
        return name == null ? null : Material.matchMaterial(name);
    }

    /**
     * @param receivers кому показать; null — всем игрокам поблизости
     * @param hue       оттенок от 0 до 1 для радужных частиц
     */
    public void spawn(World world, List<Player> receivers, double x, double y, double z, int count,
                      double offsetX, double offsetY, double offsetZ, double extra, double hue) {
        if (rainbow && count > 1) {
            // У каждой частицы свой цвет, поэтому разброс считается на сервере.
            ThreadLocalRandom random = ThreadLocalRandom.current();
            for (int i = 0, n = Math.min(count, MAX_RAINBOW_BATCH); i < n; i++) {
                emit(world, receivers, x + random.nextGaussian() * offsetX, y + random.nextGaussian() * offsetY,
                        z + random.nextGaussian() * offsetZ, 1, 0, 0, 0, extra, tinted(random.nextDouble()));
            }
            return;
        }
        emit(world, receivers, x, y, z, count, offsetX, offsetY, offsetZ, extra, rainbow ? tinted(hue) : data);
    }

    /** Одна частица, летящая в заданном направлении со скоростью speed. */
    public void spawnDirected(World world, List<Player> receivers, double x, double y, double z,
                              double dirX, double dirY, double dirZ, double speed, double hue) {
        emit(world, receivers, x, y, z, 0, dirX, dirY, dirZ, speed, rainbow ? tinted(hue) : data);
    }

    private void emit(World world, List<Player> receivers, double x, double y, double z, int count,
                      double offsetX, double offsetY, double offsetZ, double extra, Object value) {
        world.spawnParticle(particle, receivers, null, x, y, z, count, offsetX, offsetY, offsetZ, extra, value, false);
    }

    private Object tinted(double hue) {
        Color color = fromHue(hue);
        if (data instanceof Particle.DustTransition transition) {
            return new Particle.DustTransition(color, transition.getToColor(), size);
        }
        if (data instanceof Particle.DustOptions) {
            return new Particle.DustOptions(color, size);
        }
        if (data instanceof Particle.Spell spell) {
            return new Particle.Spell(color, spell.getPower());
        }
        return color;
    }

    private static Color fromHue(double hue) {
        double h = (hue - Math.floor(hue)) * 6.0;
        int rising = (int) Math.round((h - Math.floor(h)) * 255);
        int falling = 255 - rising;
        return switch ((int) h) {
            case 0 -> Color.fromRGB(255, rising, 0);
            case 1 -> Color.fromRGB(falling, 255, 0);
            case 2 -> Color.fromRGB(0, 255, rising);
            case 3 -> Color.fromRGB(0, falling, 255);
            case 4 -> Color.fromRGB(rising, 0, 255);
            default -> Color.fromRGB(255, 0, falling);
        };
    }
}
