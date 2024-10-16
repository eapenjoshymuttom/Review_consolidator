import React from 'react';

export default function Summary({ productName, summary }) {
  return (
    <div className="mb-6 p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-2">Review Summary of {productName}</h2>
      <p className="text-gray-700">{summary}</p>
    </div>
  );
}