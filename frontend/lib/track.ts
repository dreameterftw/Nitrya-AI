import { track } from "@vercel/analytics";

type FunnelStep =
  | "camera_enabled"
  | "recording_started"
  | "upload_started"
  | "analysis_complete"
  | "analysis_failed";

export function trackFunnel(step: FunnelStep, meta?: Record<string, string | number | boolean | undefined>) {
  track(step, meta);
}
