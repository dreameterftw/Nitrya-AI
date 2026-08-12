"use client";

import { FlowEnergyBar } from "@/components/western/FlowEnergyBar";
import { KeyframeBreakdown } from "@/components/indian/KeyframeBreakdown";
import { MudraLayerBadge } from "@/components/indian/MudraLayerBadge";
import { ScoreDisplay } from "@/components/ScoreDisplay";
import { useTheme } from "@/lib/theme-context";

type ResultData = {
  total_score?: number;
  form_component?: number;
  bas?: number;
  keyframe_accuracy?: number | null;
  mudra_layer_available?: boolean;
  [key: string]: unknown;
};

export function ResultsView({ result }: { result: ResultData }) {
  const { theme } = useTheme();
  const score = result.total_score ?? 0;

  return (
    <main className="results-view">
      <section className="score-panel">
        <p className="eyebrow">Analysis Complete</p>
        <ScoreDisplay score={score} theme={theme} />
        <dl className="score-metrics">
          <div>
            <dt>Form</dt>
            <dd>{formatNumber(result.form_component)}</dd>
          </div>
          <div>
            <dt>Beat Alignment</dt>
            <dd>{formatNumber(result.bas)}</dd>
          </div>
        </dl>
      </section>

      {theme === "indian" && result.keyframe_accuracy != null ? (
        <KeyframeBreakdown accuracy={result.keyframe_accuracy} />
      ) : null}

      {theme === "indian" && result.mudra_layer_available ? <MudraLayerBadge /> : null}

      {theme === "western" ? <FlowEnergyBar bas={result.bas ?? 0} /> : null}

      <details className="raw-result">
        <summary>Raw result</summary>
        <pre>{JSON.stringify(result, null, 2)}</pre>
      </details>
    </main>
  );
}

function formatNumber(value: number | undefined) {
  if (value == null) return "N/A";
  return `${Math.round(value * 100)}%`;
}
