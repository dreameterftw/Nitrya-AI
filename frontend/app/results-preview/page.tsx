import { ResultsView } from "@/components/results/ResultsView";

const previewResult = {
  total_score: 0.86,
  form_component: 0.82,
  bas: 0.91,
  keyframe_accuracy: 0.08,
  mudra_layer_available: true,
};

export default function ResultsPreviewPage() {
  return <ResultsView result={previewResult} />;
}
