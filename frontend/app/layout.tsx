import "./globals.css";

export const metadata = {
  title: "Nritya AI",
  description: "Dance scoring plumbing prototype",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
