const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function generateQuiz(url) {
    const response = await fetch(`${API_BASE}/generate_quiz?url=${encodeURIComponent(url)}`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
    });
    if (!response.ok) throw new Error('Failed to generate quiz');
    return response.json();
}

export async function getHistory() {
    const response = await fetch(`${API_BASE}/history`);
    if (!response.ok) throw new Error('Failed to fetch history');
    return response.json();
}

export async function getQuiz(id) {
    const response = await fetch(`${API_BASE}/quiz/${id}`);
    if (!response.ok) throw new Error('Failed to fetch quiz');
    return response.json();
}