import { useEffect, useState } from "react";
import { fetchHistory, fetchQuizById } from "../services/api";
import HistoryTable from "../components/HistoryTable";
import Modal from "../components/Modal";
import QuizDisplay from "../components/QuizDisplay";

export default function HistoryTab() {
  const [history, setHistory] = useState([]);
  const [selectedQuiz, setSelectedQuiz] = useState(null);

  useEffect(() => {
    fetchHistory().then(setHistory);
  }, []);

  const handleSelect = async (id) => {
    const quiz = await fetchQuizById(id);
    setSelectedQuiz(quiz);
  };

  return (
    <div className="p-4">
      <HistoryTable history={history} onSelect={handleSelect} />
      <Modal open={!!selectedQuiz} onClose={() => setSelectedQuiz(null)}>
        {selectedQuiz && <QuizDisplay quiz={selectedQuiz} />}
      </Modal>
    </div>
  );
}
