package ru.applecosmetic.effect;

import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import org.bukkit.World;
import org.bukkit.entity.Player;

/** Формы анимаций. В скобках — значения по умолчанию для слоя. */
public enum Animation {

    /** Вспышка частиц в одной точке. */
    BURST(30, 0.4, 0.0, 1.0, 1, 0.1) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            layer.particle().spawn(frame.world, frame.receivers, frame.x, frame.y + layer.yOffset(), frame.z,
                    layer.amount(), layer.radius(), layer.radius(), layer.radius(), layer.speed(), frame.progress);
        }
    },

    /** Кольцо, расходящееся по земле. */
    RING(24, 2.0, 0.0, 0.1, 12, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            double radius = layer.radius() * frame.progress;
            int points = layer.amount();
            for (int i = 0; i < points; i++) {
                double angle = TAU * i / points;
                point(layer, frame, frame.x + Math.cos(angle) * radius, frame.y + layer.yOffset(),
                        frame.z + Math.sin(angle) * radius, (double) i / points);
            }
        }
    },

    /** Спираль, поднимающаяся вверх; amount — число витков-нитей. */
    HELIX(2, 0.8, 2.2, 0.0, 25, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            for (int step = 0; step < 2; step++) {
                double progress = (frame.tick + step / 2.0) / layer.duration();
                double turn = progress * TAU * 2;
                for (int strand = 0; strand < layer.amount(); strand++) {
                    double angle = turn + TAU * strand / layer.amount();
                    point(layer, frame, frame.x + Math.cos(angle) * layer.radius(),
                            frame.y + layer.yOffset() + progress * layer.height(),
                            frame.z + Math.sin(angle) * layer.radius(), progress);
                }
            }
        }
    },

    /** Расширяющаяся сфера. */
    SPHERE(40, 1.5, 0.0, 1.0, 8, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            sphere(layer, frame, layer.radius() * frame.progress);
        }
    },

    /** Сфера, сжимающаяся в точку. */
    IMPLODE(30, 2.0, 0.0, 1.0, 12, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            sphere(layer, frame, layer.radius() * (1.0 - frame.progress) + 0.1);
        }
    },

    /** Фонтан: частицы вылетают вверх. */
    FOUNTAIN(6, 0.35, 0.0, 0.3, 20, 0.45) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            for (int i = 0; i < layer.amount(); i++) {
                layer.particle().spawnDirected(frame.world, frame.receivers, frame.x, frame.y + layer.yOffset(),
                        frame.z, (random.nextDouble() - 0.5) * 2 * layer.radius(), 1.0,
                        (random.nextDouble() - 0.5) * 2 * layer.radius(), layer.speed(), random.nextDouble());
            }
        }
    },

    /** Дождь из частиц с высоты height. */
    RAIN(6, 1.2, 3.0, 0.0, 30, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            for (int i = 0; i < layer.amount(); i++) {
                double angle = random.nextDouble() * TAU;
                double distance = Math.sqrt(random.nextDouble()) * layer.radius();
                point(layer, frame, frame.x + Math.cos(angle) * distance,
                        frame.y + layer.yOffset() + layer.height(),
                        frame.z + Math.sin(angle) * distance, random.nextDouble());
            }
        }
    },

    /** Вертикальный столб. */
    COLUMN(10, 0.25, 3.0, 0.0, 20, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            for (int i = 0; i < layer.amount(); i++) {
                point(layer, frame, frame.x + random.nextGaussian() * layer.radius(),
                        frame.y + layer.yOffset() + random.nextDouble() * layer.height(),
                        frame.z + random.nextGaussian() * layer.radius(), random.nextDouble());
            }
        }
    },

    /** Вихрь, расширяющийся кверху. */
    VORTEX(16, 1.4, 3.0, 0.0, 30, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            int points = layer.amount();
            for (int i = 0; i < points; i++) {
                double fraction = (double) i / points;
                double angle = frame.tick * 0.45 + fraction * TAU * 2;
                double radius = layer.radius() * (0.15 + 0.85 * fraction);
                point(layer, frame, frame.x + Math.cos(angle) * radius,
                        frame.y + layer.yOffset() + layer.height() * fraction,
                        frame.z + Math.sin(angle) * radius, fraction);
            }
        }
    },

    /** Вращающееся сердце. */
    HEART(36, 0.9, 0.0, 1.6, 30, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            if (frame.tick % 2 != 0) {
                return;
            }
            double rotation = TAU * frame.tick / layer.duration();
            int points = layer.amount();
            for (int i = 0; i < points; i++) {
                double t = TAU * i / points;
                double across = Math.pow(Math.sin(t), 3) * layer.radius();
                double up = (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t))
                        / 16.0 * layer.radius();
                point(layer, frame, frame.x + Math.cos(rotation) * across, frame.y + layer.yOffset() + up,
                        frame.z + Math.sin(rotation) * across, (double) i / points);
            }
        }
    },

    /** Пентаграмма на земле; amount — точек на каждый луч. */
    STAR(10, 1.8, 0.0, 0.15, 40, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            if (frame.tick % 3 != 0) {
                return;
            }
            double y = frame.y + layer.yOffset();
            double radius = layer.radius();
            int perLine = layer.amount();
            for (int vertex = 0; vertex < 5; vertex++) {
                double from = TAU * vertex / 5 - Math.PI / 2;
                double to = TAU * ((vertex + 2) % 5) / 5 - Math.PI / 2;
                double fromX = Math.cos(from) * radius;
                double fromZ = Math.sin(from) * radius;
                double toX = Math.cos(to) * radius;
                double toZ = Math.sin(to) * radius;
                for (int i = 0; i <= perLine; i++) {
                    double t = (double) i / perLine;
                    point(layer, frame, frame.x + fromX + (toX - fromX) * t, y,
                            frame.z + fromZ + (toZ - fromZ) * t, vertex / 5.0);
                }
            }
            int circle = perLine * 4;
            for (int i = 0; i < circle; i++) {
                double angle = TAU * i / circle;
                point(layer, frame, frame.x + Math.cos(angle) * radius, y, frame.z + Math.sin(angle) * radius,
                        (double) i / circle);
            }
        }
    },

    /** Крест: height — высота, radius — половина перекладины. */
    CROSS(14, 0.6, 2.2, 0.0, 40, 0.0) {
        @Override
        void render(EffectLayer layer, Frame frame) {
            if (frame.tick % 3 != 0) {
                return;
            }
            double base = frame.y + layer.yOffset();
            int points = layer.amount();
            for (int i = 0; i <= points; i++) {
                double t = (double) i / points;
                point(layer, frame, frame.x, base + layer.height() * t, frame.z, t);
            }
            int arm = Math.max(2, points / 2);
            for (int i = 0; i <= arm; i++) {
                double t = (double) i / arm;
                point(layer, frame, frame.x - layer.radius() + 2 * layer.radius() * t,
                        base + layer.height() * 0.68, frame.z, t);
            }
        }
    };

    private static final double TAU = Math.PI * 2;
    private static final double GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));

    final int amount;
    final double radius;
    final double height;
    final double yOffset;
    final int duration;
    final double speed;

    Animation(int amount, double radius, double height, double yOffset, int duration, double speed) {
        this.amount = amount;
        this.radius = radius;
        this.height = height;
        this.yOffset = yOffset;
        this.duration = duration;
        this.speed = speed;
    }

    abstract void render(EffectLayer layer, Frame frame);

    private static void point(EffectLayer layer, Frame frame, double x, double y, double z, double hue) {
        layer.particle().spawn(frame.world, frame.receivers, x, y, z, 1, 0, 0, 0, layer.speed(), hue);
    }

    private static void sphere(EffectLayer layer, Frame frame, double radius) {
        int points = layer.amount();
        for (int i = 0; i < points; i++) {
            double vertical = 1 - 2 * (i + 0.5) / points;
            double ring = Math.sqrt(1 - vertical * vertical);
            double angle = i * GOLDEN_ANGLE;
            point(layer, frame, frame.x + Math.cos(angle) * ring * radius,
                    frame.y + layer.yOffset() + vertical * radius,
                    frame.z + Math.sin(angle) * ring * radius, (double) i / points);
        }
    }

    /** Состояние одного кадра: где и для кого рисуется эффект. */
    static final class Frame {
        final World world;
        final List<Player> receivers;
        final double x;
        final double y;
        final double z;
        int tick;
        double progress;

        Frame(World world, List<Player> receivers, double x, double y, double z) {
            this.world = world;
            this.receivers = receivers;
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }
}
