import "./globals.css";
import { Analytics } from "@vercel/analytics/react";
import { ThemeShell } from "@/components/ThemeShell";
import { ThemeProvider } from "@/lib/theme-context";

export const metadata = {
  title: "Nritya AI",
  description: "Dance scoring plumbing prototype",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ThemeProvider>
          <ThemeShell>{children}</ThemeShell>
        </ThemeProvider>
        <Analytics />
      </body>
    </html>
  );
}
