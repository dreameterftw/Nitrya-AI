"use client";

export function ErrorScreen({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <section className="theme-card">
      <h2>Analysis failed</h2>
      <p>{message}</p>
      <button onClick={onRetry}>Try Again</button>
    </section>
  );
}
