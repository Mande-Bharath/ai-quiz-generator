import { useState } from "react";
import { generateQuiz } from "../services/api";
import QuizDisplay from "../components/QuizDisplay";

export default function GenerateQuizTab() {
  const [url, setUrl] = useState("");
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!url) return alert("Please enter a Wikipedia URL");
    setLoading(true);
    const data = await generateQuiz(url);
    setQuiz(data);
    setLoading(false);
  };

  return (
    <div className="p-4">
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Enter Wikipedia URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border p-2 flex-grow rounded"
        />
        <button
          onClick={handleGenerate}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Generate
        </button>
      </div>
      {loading && <p>Generating quiz...</p>}
      {quiz && <QuizDisplay quiz={quiz} />}
    </div>
  );
}
