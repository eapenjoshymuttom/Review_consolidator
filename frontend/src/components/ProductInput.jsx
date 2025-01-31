import React from 'react';

export default function ProductInput({ productName, setProductName, getProductSummary, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    getProductSummary();
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4">Enter Product Name</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          className="p-2 border border-gray-300 rounded-lg w-full mb-4"
          placeholder="e.g., iPhone 12"
        />
        <button
          type="submit"
          className={`p-2 bg-blue-600 text-white rounded-lg ${loading.summary ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={loading.summary}
        >
          {loading.summary ? 'Loading...' : 'Get Product Summary'}
        </button>
      </form>
    </div>
  );
}