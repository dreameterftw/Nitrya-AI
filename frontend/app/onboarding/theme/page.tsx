"use client";

import { useRouter } from "next/navigation";
import { useTheme, type Theme } from "@/lib/theme-context";

export default function ThemeStepPage() {
  const { setTheme } = useTheme();
  const router = useRouter();

  function choose(theme: Theme) {
    setTheme(theme);
    router.push("/onboarding/tutorial");
  }

  return (
    <main className="theme-picker">
      <button className="theme-choice western-choice" onClick={() => choose("western")}>
        Western
      </button>
      <button className="theme-choice indian-choice" onClick={() => choose("indian")}>
        Indian Classical
      </button>
    </main>
  );
}
