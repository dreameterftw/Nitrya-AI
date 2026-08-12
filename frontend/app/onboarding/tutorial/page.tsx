"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

type FramingStatus = "waiting" | "too_far" | "cut_off" | "good";

const messages: Record<FramingStatus, string> = {
  waiting: "Stand back so your whole body is visible",
  too_far: "Move a little closer",
  cut_off: "Step back - I can't see your feet",
  good: "Perfect! You're ready to record",
};

export default function TutorialPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [status, setStatus] = useState<FramingStatus>("waiting");
  const router = useRouter();

  useEffect(() => {
    let stream: MediaStream | undefined;
    let timer: number | undefined;
    async function start() {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) videoRef.current.srcObject = stream;
      timer = window.setTimeout(() => setStatus("good"), 2500);
    }
    start().catch(() => setStatus("cut_off"));
    return () => {
      if (timer) window.clearTimeout(timer);
      stream?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  return (
    <main className="tutorial-page">
      <video ref={videoRef} autoPlay muted playsInline />
      <div className="tutorial-overlay">
        <p>{messages[status]}</p>
        <button disabled={status !== "good"} onClick={() => router.push("/onboarding/profile")}>
          Continue
        </button>
      </div>
    </main>
  );
}
