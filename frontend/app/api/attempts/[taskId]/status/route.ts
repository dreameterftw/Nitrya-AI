const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function GET(_: Request, { params }: { params: Promise<{ taskId: string }> }) {
  const { taskId } = await params;
  const res = await fetch(`${apiBaseUrl}/attempts/${taskId}/status`, { cache: "no-store" });
  return Response.json(await res.json(), { status: res.status });
}
