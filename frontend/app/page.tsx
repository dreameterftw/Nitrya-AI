import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <h1>Nritya AI</h1>
      <p>Dance scoring MVP.</p>
      <nav className="home-actions">
        <Link href="/onboarding">Choose theme</Link>
        <Link href="/discover">Discover profiles</Link>
        <Link href="/record">Record an attempt</Link>
      </nav>
    </main>
  );
}
