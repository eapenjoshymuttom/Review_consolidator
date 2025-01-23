import React from 'react';

export default function ProductInput({ productName, setProductName, getProductSummary, loading }) {
  return (
    <div className="flex flex-col items-center">
      <h1 className="text-4xl font-extrabold mb-6 text-center text-gray-800">Enter Product Name</h1>
      <input
        type="text"
        value={productName}
        onChange={(e) => setProductName(e.target.value)}
        placeholder="Enter product name"
        className="border p-3 rounded-lg shadow-sm w-full max-w-md mb-4"
      />
      <button
        onClick={getProductSummary}
        className="bg-blue-600 text-white p-3 rounded-lg shadow-md hover:bg-blue-700 transition"
        disabled={loading.summary}
      >
        {loading.summary ? 'Loading...' : 'Get Product Summary'}
      </button>
    </div>
  );
}