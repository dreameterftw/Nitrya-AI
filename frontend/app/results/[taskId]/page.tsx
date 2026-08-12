import { ResultsView } from "@/components/results/ResultsView";

async function getStatus(taskId: string) {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  const res = await fetch(`${apiBaseUrl}/attempts/${taskId}/status`, { cache: "no-store" });
  return res.json();
}

export default async function ResultsPage({ params }: { params: Promise<{ taskId: string }> }) {
  const { taskId } = await params;
  const data = await getStatus(taskId);

  return <ResultsView result={data.result ?? {}} />;
}
