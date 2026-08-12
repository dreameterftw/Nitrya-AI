"use client";

import { createContext, ReactNode, useContext, useEffect, useState } from "react";

export type Theme = "western" | "indian";

const ThemeContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
}>({
  theme: "western",
  setTheme: () => {},
});

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>("western");

  useEffect(() => {
    const saved = window.localStorage.getItem("nritya-theme");
    if (saved === "western" || saved === "indian") {
      setThemeState(saved);
    }
  }, []);

  function setTheme(nextTheme: Theme) {
    setThemeState(nextTheme);
    window.localStorage.setItem("nritya-theme", nextTheme);
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <div data-theme={theme}>{children}</div>
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
