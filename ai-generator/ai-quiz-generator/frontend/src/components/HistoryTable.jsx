export default function HistoryTable({ history, onSelect }) {
  return (
    <table className="w-full text-left border-collapse">
      <thead>
        <tr className="bg-gray-200">
          <th className="p-2">ID</th>
          <th className="p-2">Title</th>
          <th className="p-2">URL</th>
          <th className="p-2">Date</th>
          <th className="p-2">Action</th>
        </tr>
      </thead>
      <tbody>
        {history.map((q) => (
          <tr key={q.id} className="border-b">
            <td className="p-2">{q.id}</td>
            <td className="p-2">{q.title}</td>
            <td className="p-2 text-blue-600 underline">
              <a href={q.url} target="_blank">{q.url.slice(0, 30)}...</a>
            </td>
            <td className="p-2">{new Date(q.date_generated).toLocaleString()}</td>
            <td className="p-2">
              <button
                onClick={() => onSelect(q.id)}
                className="bg-blue-600 text-white px-3 py-1 rounded"
              >
                View
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
