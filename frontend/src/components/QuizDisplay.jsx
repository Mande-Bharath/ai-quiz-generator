export default function QuizDisplay({quiz}){
  if(!quiz) return null;
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">{quiz.title}</h2>
      <div className="text-sm text-gray-600">{quiz.summary}</div>
      <div className="mt-3 space-y-3">
        {quiz.questions.map(q=>(
          <div key={q.id} className="p-3 border rounded">
            <div className="font-medium">Q{q.id}: {q.question}</div>
            {q.type === "multiple_choice" && q.options && (
              <ul className="mt-2 list-disc list-inside">
                {q.options.map((opt, idx) => <li key={idx}>{opt}</li>)}
              </ul>
            )}
            {q.explanation && <div className="mt-2 text-sm text-gray-700">Explanation: {q.explanation}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
