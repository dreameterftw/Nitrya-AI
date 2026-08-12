"use client";

import { motion } from "framer-motion";
import type { Theme } from "@/lib/theme-context";

export function ScoreDisplay({ score, theme }: { score: number; theme: Theme }) {
  const scale = theme === "western" ? 1.4 : 1.0;
  const duration = theme === "western" ? 0.4 : 0.8;

  return (
    <motion.div
      initial={{ scale: 0.5, opacity: 0 }}
      animate={{ scale, opacity: 1 }}
      transition={{ duration, type: "spring" }}
      className="score-display"
      style={{ color: "var(--accent)" }}
    >
      {Math.round(score * 100)}%
    </motion.div>
  );
}
