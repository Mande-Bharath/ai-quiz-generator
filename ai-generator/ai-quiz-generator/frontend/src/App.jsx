import { useState } from "react";
import GenerateQuizTab from "./tabs/GenerateQuizTab";
import HistoryTab from "./tabs/HistoryTab";

export default function App() {
  const [activeTab, setActiveTab] = useState("generate");

  return (
    <div className="max-w-4xl mx-auto py-8">
      <h1 className="text-3xl font-bold text-center mb-6">AI Wiki Quiz Generator</h1>
      <div className="flex justify-center gap-4 mb-6">
        <button
          onClick={() => setActiveTab("generate")}
          className={`px-4 py-2 rounded ${activeTab === "generate" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
        >
          Generate Quiz
        </button>
        <button
          onClick={() => setActiveTab("history")}
          className={`px-4 py-2 rounded ${activeTab === "history" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
        >
          History
        </button>
      </div>

      {activeTab === "generate" && <GenerateQuizTab />}
      {activeTab === "history" && <HistoryTab />}
    </div>
  );
}
