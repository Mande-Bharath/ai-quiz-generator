import { useState } from "react";
import { generateQuiz } from "../api";
import QuizDisplay from "./QuizDisplay";

export default function GenerateQuizTab() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function onSubmit(e){
    e.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);
    try {
      const data = await generateQuiz(url);
      setResult(data.quiz);
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-4">
      <form onSubmit={onSubmit} className="space-y-3">
        <input value={url} onChange={e=>setUrl(e.target.value)}
               placeholder="Enter Wikipedia URL" className="w-full p-2 border rounded" />
        <button type="submit" className="px-4 py-2 bg-slate-700 text-white rounded" disabled={loading}>
          {loading ? "Generating..." : "Generate Quiz"}
        </button>
      </form>

      {error && <div className="mt-3 text-red-600">{error}</div>}
      {result && <div className="mt-6"><QuizDisplay quiz={result} /></div>}
    </div>
  );
}
