import { useState } from "react";

export default function QueryBox({ setAnswer }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setAnswer(data.answer);
    setLoading(false);
  };

  return (
    <div className="card">
      <h3>Ask a Question</h3>
      <textarea
        placeholder="Ask something about the document..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={askQuestion} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>
    </div>
  );
}
