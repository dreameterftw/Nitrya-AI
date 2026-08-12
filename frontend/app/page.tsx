import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <h1>Nritya AI</h1>
      <p>Phase 4 plumbing prototype.</p>
      <Link href="/record">Record an attempt</Link>
    </main>
  );
}
