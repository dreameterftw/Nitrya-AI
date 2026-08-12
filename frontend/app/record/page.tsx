"use client";

import { useRef, useState } from "react";

export default function RecordPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const [profileId, setProfileId] = useState("");
  const [userId, setUserId] = useState("");
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
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
    const blob = new Blob(chunksRef.current, { type: "video/webm" });
    const formData = new FormData();
    formData.append("video", blob, "attempt.webm");
    formData.append("profile_id", profileId);
    if (userId) formData.append("user_id", userId);

    const res = await fetch("/api/attempts", { method: "POST", body: formData });
    const data = await res.json();
    setStatus("processing");
    pollForResult(data.task_id);
  }

  async function pollForResult(taskId: string) {
    const interval = window.setInterval(async () => {
      const res = await fetch(`/api/attempts/${taskId}/status`);
      const data = await res.json();
      if (data.status === "done") {
        window.clearInterval(interval);
        setStatus("done");
        setResult(data.result);
      }
    }, 2000);
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
