// src/api.js
const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function generateQuiz(url) {
  const res = await fetch(`${BASE}/generate_quiz`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ url })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${BASE}/history`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getQuizById(id) {
  const res = await fetch(`${BASE}/quiz/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
