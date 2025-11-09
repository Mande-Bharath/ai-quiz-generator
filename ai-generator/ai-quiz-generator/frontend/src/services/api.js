const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function generateQuiz(url) {
  const res = await fetch(`${API_BASE}/generate_quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/history`);
  return res.json();
}

export async function fetchQuizById(id) {
  const res = await fetch(`${API_BASE}/quiz/${id}`);
  return res.json();
}
