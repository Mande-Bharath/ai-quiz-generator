export default function QuizDisplay({ quiz }) {
  if (!quiz) return null;
  return (
    <div className="bg-white p-6 rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-2">{quiz.title}</h2>
      <p className="text-gray-600 mb-4">{quiz.summary}</p>
      {quiz.questions.map((q, i) => (
        <div key={i} className="mb-4 border-b pb-2">
          <h3 className="font-semibold">{q.question}</h3>
          <ul className="list-disc ml-6">
            {q.options.map((opt, j) => (
              <li key={j}>{opt}</li>
            ))}
          </ul>
          <p className="text-green-600 mt-1">Answer: {q.answer}</p>
        </div>
      ))}
    </div>
  );
}
