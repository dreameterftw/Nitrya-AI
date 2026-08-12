"use client";

import { useEffect, useRef, useState } from "react";

const STAGE_LABELS: Record<string, string> = {
  queued: "Starting the analysis worker...",
  loading_profile: "Loading your reference...",
  downloading_video: "Preparing your video...",
  extracting_pose: "Reading your movement...",
  scoring_rhythm: "Checking your rhythm...",
  finalizing: "Finishing up...",
};

export function AnalyzingScreen({
  taskId,
  onDone,
}: {
  taskId: string;
  onDone: (result: Record<string, unknown>) => void;
}) {
  const [stage, setStage] = useState("queued");
  const [pct, setPct] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const lastStage = useRef("queued");
  const isColdStartLikely = stage === "queued" && elapsed >= 15;

  useEffect(() => {
    const startTime = Date.now();
    const poll = window.setInterval(async () => {
      setElapsed(Math.round((Date.now() - startTime) / 1000));
      const res = await fetch(`/api/attempts/${taskId}/status`);
      const data = await res.json();
      if (data.status === "done") {
        window.clearInterval(poll);
        onDone(data.result);
      } else if (data.status === "failed") {
        window.clearInterval(poll);
        onDone({ error: data.error, stage: lastStage.current });
      } else {
        const nextStage = data.stage || "queued";
        lastStage.current = nextStage;
        setStage(nextStage);
        setPct(data.pct || 0);
      }
    }, 1500);
    return () => window.clearInterval(poll);
  }, [taskId, onDone]);

  return (
    <section className="analyzing-screen">
      <div className="spinner" />
      <p>{STAGE_LABELS[stage] || "Starting up..."}</p>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${pct}%` }} />
      </div>
      <p className="muted-text">
        {isColdStartLikely
          ? "The free pilot server may be waking up. First requests can take up to a minute."
          : "Usually takes 15-25s once the worker is awake."}
      </p>
      <p className="muted-text">{elapsed}s elapsed</p>
    </section>
  );
}
