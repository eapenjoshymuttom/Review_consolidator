import React, { useState } from 'react';

export default function AskQuestions({ productName, fetchData, loading }) {
  const [query, setQuery] = useState('');
  const [questions, setQuestions] = useState([]);

  const answerQuery = async () => {
    const data = await fetchData('/answer_query', { product_name: productName, query }, 'query');
    if (data) {
      setQuestions((prev) => [...prev, { query, answer: data.answer }]);
      setQuery('');
    }
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Ask a Question</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query"
        className="border p-3 rounded-lg shadow-sm w-full mb-4"
      />
      <button
        onClick={answerQuery}
        className="bg-green-600 text-white p-3 rounded-lg shadow-md hover:bg-green-700 transition"
        disabled={loading.query}
      >
        {loading.query ? 'Loading...' : 'Ask Question'}
      </button>
      {questions.map((q, index) => (
        <div key={index} className="mt-4">
          <h3 className="text-lg font-bold mb-2">Question: {q.query}</h3>
          <p className="text-gray-700">Answer: {q.answer}</p>
        </div>
      ))}
    </div>
  );
}