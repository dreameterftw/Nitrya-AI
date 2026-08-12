"use client";

import Link from "next/link";
import { useTheme } from "@/lib/theme-context";

export function ThemeShell({ children }: { children: React.ReactNode }) {
  const { theme } = useTheme();

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link href="/" className="brand">
          Nritya AI
        </Link>
        <span className="theme-label">{theme === "western" ? "Western" : "Indian Classical"}</span>
      </header>
      {children}
    </div>
  );
}
