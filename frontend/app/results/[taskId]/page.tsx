async function getStatus(taskId: string) {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  const res = await fetch(`${apiBaseUrl}/attempts/${taskId}/status`, { cache: "no-store" });
  return res.json();
}

export default async function ResultsPage({ params }: { params: Promise<{ taskId: string }> }) {
  const { taskId } = await params;
  const data = await getStatus(taskId);

  return (
    <main>
      <h1>Result</h1>
      <h2>Score: {data.result?.total_score}</h2>
      <p>Form component: {data.result?.form_component}</p>
      <p>Beat alignment: {data.result?.bas}</p>
      {data.result?.keyframe_accuracy ? <p>Keyframe accuracy: {data.result.keyframe_accuracy}</p> : null}
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </main>
  );
}
