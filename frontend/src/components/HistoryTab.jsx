import { useEffect, useState } from "react";
import { getHistory, getQuizById } from "../api";
import Modal from "./Modal";
import QuizDisplay from "./QuizDisplay";

export default function HistoryTab(){
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [quizDetail, setQuizDetail] = useState(null);

  useEffect(()=> {
    getHistory().then(setRows).catch(console.error).finally(()=>setLoading(false));
  }, []);

  async function openDetails(id) {
    const data = await getQuizById(id);
    setQuizDetail(data.quiz);
    setSelected(id);
  }

  return (
    <div className="p-4">
      {loading ? <div>Loading history...</div> :
        <table className="w-full">
          <thead><tr><th>ID</th><th>Title</th><th>URL</th><th></th></tr></thead>
          <tbody>
            {rows.map(r=>(
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.title}</td>
                <td className="truncate max-w-xs">{r.url}</td>
                <td><button onClick={()=>openDetails(r.id)} className="underline">Details</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      }

      {selected && <Modal onClose={()=>{setSelected(null); setQuizDetail(null);}}>
        <QuizDisplay quiz={quizDetail} />
      </Modal>}
    </div>
  );
}
