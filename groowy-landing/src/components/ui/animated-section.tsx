import { motion, useInView } from "motion/react";
import { useRef } from "react";
import type { ReactNode } from "react";

interface AnimatedSectionProps {
    children: ReactNode;
    className?: string;
    delay?: number;
    direction?: "up" | "down" | "left" | "right" | "fade";
    duration?: number;
}

export function AnimatedSection({
    children,
    className = "",
    delay = 0,
    direction = "up",
    duration = 0.6,
}: AnimatedSectionProps) {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.2 });

    const variants = {
        up: { y: 50, opacity: 0 },
        down: { y: -50, opacity: 0 },
        left: { x: 50, opacity: 0 },
        right: { x: -50, opacity: 0 },
        fade: { opacity: 0 },
    };

    return (
        <motion.div
            ref={ref}
            initial={variants[direction]}
            animate={
                isInView
                    ? { x: 0, y: 0, opacity: 1 }
                    : variants[direction]
            }
            transition={{
                duration,
                delay,
                ease: [0.21, 0.47, 0.32, 0.98],
            }}
            className={className}
        >
            {children}
        </motion.div>
    );
}

interface AnimatedElementProps {
    children: ReactNode;
    className?: string;
    delay?: number;
    scale?: boolean;
}

export function AnimatedElement({
    children,
    className = "",
    delay = 0,
    scale = false,
}: AnimatedElementProps) {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.5 });

    return (
        <motion.div
            ref={ref}
            initial={{ opacity: 0, scale: scale ? 0.9 : 1, y: 20 }}
            animate={
                isInView
                    ? { opacity: 1, scale: 1, y: 0 }
                    : { opacity: 0, scale: scale ? 0.9 : 1, y: 20 }
            }
            transition={{
                duration: 0.5,
                delay,
                ease: "easeOut",
            }}
            className={className}
        >
            {children}
        </motion.div>
    );
}
