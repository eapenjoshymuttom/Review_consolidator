import React from 'react';

export default function AskQuestions({ productName, query, setQuery, answerQuery, loading, queryHistory }) {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Ask Questions about {productName}</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your question"
        className="w-full p-2 mb-4 border rounded"
      />
      <button
        onClick={answerQuery}
        className="bg-blue-600 text-white p-2 rounded-lg shadow-md hover:bg-blue-700 transition"
        disabled={loading.query}
      >
        {loading.query ? 'Loading...' : 'Get Answer'}
      </button>
      {queryHistory.length > 0 && (
        <div className="mt-4">
          <h3 className="font-bold mb-2">Latest Answer:</h3>
          <div className="p-4 bg-gray-200 rounded">
            <strong>Q:</strong> {queryHistory[queryHistory.length - 1].question}
            <br />
            <strong>A:</strong> {queryHistory[queryHistory.length - 1].answer}
          </div>
        </div>
      )}
      {queryHistory.length > 1 && (
        <div className="mt-4">
          <h3 className="font-bold mb-2">Previous Questions:</h3>
          <ul className="list-disc pl-5">
            {queryHistory.slice(0, -1).map((item, index) => (
              <li key={index} className="mb-2">
                <strong>Q:</strong> {item.question}
                <br />
                <strong>A:</strong> {item.answer}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}