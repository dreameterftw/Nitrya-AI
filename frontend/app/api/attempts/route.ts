const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  const formData = await request.formData();
  const res = await fetch(`${apiBaseUrl}/attempts`, {
    method: "POST",
    body: formData,
  });
  return Response.json(await res.json(), { status: res.status });
}
