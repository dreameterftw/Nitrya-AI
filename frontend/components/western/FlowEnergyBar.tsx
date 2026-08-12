"use client";

export function FlowEnergyBar({ bas }: { bas: number }) {
  const width = `${Math.max(0, Math.min(1, bas)) * 100}%`;

  return (
    <section className="theme-card">
      <h2>Flow Energy</h2>
      <div className="energy-track">
        <div className="energy-fill" style={{ width }} />
      </div>
      <p>{Math.round(bas * 100)}% beat lock</p>
    </section>
  );
}
