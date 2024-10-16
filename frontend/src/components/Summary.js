import React from 'react';

export default function Summary({ productName, summary, error }) {
  return (
    <div className="mb-6 p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-2">Review Summary of {productName}</h2>
      {error ? (
        <p className="text-red-600">{error}</p>
      ) : (
        <p className="text-gray-700">{summary}</p>
      )}
    </div>
  );
}