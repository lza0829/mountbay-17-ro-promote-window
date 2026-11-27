const base = "/api";
export async function get(path) {
  const r = await fetch(base + path);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
export async function post(path, body) {
  const r = await fetch(base + path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
