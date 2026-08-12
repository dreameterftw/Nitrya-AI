"use client";

import { useRef, useState } from "react";
import { AnalyzingScreen } from "@/components/AnalyzingScreen";
import { ErrorScreen } from "@/components/ErrorScreen";
import { trackFunnel } from "@/lib/track";

export default function RecordPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const [profileId, setProfileId] = useState(() => {
    if (typeof window === "undefined") return "";
    return new URLSearchParams(window.location.search).get("profileId") ?? "";
  });
  const [userId, setUserId] = useState("");
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    trackFunnel("camera_enabled");
    if (videoRef.current) videoRef.current.srcObject = stream;

    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) chunksRef.current.push(event.data);
    };
    recorderRef.current = recorder;
    setStatus("camera_ready");
  }

  function startRecording() {
    chunksRef.current = [];
    recorderRef.current?.start();
    trackFunnel("recording_started");
    setStatus("recording");
  }

  async function stopAndUpload() {
    const recorder = recorderRef.current;
    if (!recorder || !profileId) return;

    const stopped = new Promise<void>((resolve) => {
      recorder.onstop = () => resolve();
    });
    recorder.stop();
    await stopped;

    setStatus("uploading");
    trackFunnel("upload_started", { profileId });
    const blob = new Blob(chunksRef.current, { type: "video/webm" });
    const formData = new FormData();
    formData.append("video", blob, "attempt.webm");
    formData.append("profile_id", profileId);
    if (userId) formData.append("user_id", userId);

    const res = await fetch("/api/attempts", { method: "POST", body: formData });
    const data = await res.json();
    setStatus("processing");
    setResult({ taskId: data.task_id });
  }

  function handleDone(doneResult: Record<string, unknown>) {
    if (doneResult.error) {
      trackFunnel("analysis_failed", { stage: String(doneResult.stage ?? "unknown") });
    } else {
      trackFunnel("analysis_complete", {
        score: Number(doneResult.total_score ?? 0),
        profileId,
      });
    }
    setStatus("done");
    setResult(doneResult);
  }

  if (status === "processing" && typeof result?.taskId === "string") {
    return <AnalyzingScreen taskId={result.taskId} onDone={handleDone} />;
  }

  if (result?.error) {
    return (
      <main>
        <ErrorScreen
          message="Analysis failed - try recording again with better lighting or framing."
          onRetry={() => {
            setResult(null);
            setStatus("camera_ready");
          }}
        />
      </main>
    );
  }

  return (
    <main>
      <h1>Record Attempt</h1>
      <label>
        Profile ID
        <input value={profileId} onChange={(event) => setProfileId(event.target.value)} />
      </label>
      <label>
        User ID
        <input value={userId} onChange={(event) => setUserId(event.target.value)} />
      </label>
      <video ref={videoRef} autoPlay muted playsInline />
      <button onClick={startCamera}>Enable Camera</button>
      <button onClick={startRecording}>Record</button>
      <button onClick={stopAndUpload}>Stop & Analyze</button>
      <p>Status: {status}</p>
      {result ? <pre>{JSON.stringify(result, null, 2)}</pre> : null}
    </main>
  );
}
