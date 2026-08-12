"use client";

export function KeyframeBreakdown({ accuracy }: { accuracy: number }) {
  return (
    <section className="theme-card">
      <h2>Keyframe Accuracy</h2>
      <p>{Math.round((1 - accuracy) * 100)}% structural match</p>
    </section>
  );
}
