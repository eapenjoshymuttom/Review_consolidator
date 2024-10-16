import React, { useState } from 'react';
import 'tailwindcss/tailwind.css';
import ProductInput from './components/ProductInput';
import Summary from './components/Summary';
import AskQuestions from './components/AskQuestions';
import WriteReview from './components/WriteReview';
import PersonalizeReview from './components/PersonalizeReview';

const API_URL = 'http://localhost:8000';

export default function App() {
  const [productName, setProductName] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState({
    summary: false,
    query: false,
    feedback: false,
    style: false,
    template: false,
    completion: false,
  });
  const [activeTab, setActiveTab] = useState('ask');
  const [error, setError] = useState('');

  const fetchData = async (endpoint, data, loadingKey) => {
    setLoading((prev) => ({ ...prev, [loadingKey]: true }));
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error fetching data from ${endpoint}:`, error);
      setError('An error occurred while fetching data.');
    } finally {
      setLoading((prev) => ({ ...prev, [loadingKey]: false }));
    }
  };

  const getProductSummary = async () => {
    const data = await fetchData('/product_summary', { product_name: productName }, 'summary');
    if (data) {
      if (data.summary) {
        setSummary(data.summary);
        setError('');
      } else {
        setSummary('');
        setError('No product or review found.');
      }
    }
  };

  const resetState = () => {
    setProductName('');
    setSummary('');
    setActiveTab('ask');
    setError('');
  };

  return (
    <div className="container mx-auto p-6 bg-gray-100 min-h-screen">
      {!summary && !error ? (
        <ProductInput
          productName={productName}
          setProductName={setProductName}
          getProductSummary={getProductSummary}
          loading={loading}
        />
      ) : (
        <div>
          <Summary productName={productName} summary={summary} error={error} />
          <div className="p-4 bg-white rounded-lg shadow-md">
            <div className="flex justify-around mb-4">
              <button
                className={`p-2 ${activeTab === 'ask' ? 'bg-violet-600 text-white' : 'bg-gray-200 text-gray-800'} rounded-lg`}
                onClick={() => setActiveTab('ask')}
              >
                Ask Questions
              </button>
              <button
                className={`p-2 ${activeTab === 'review' ? 'bg-violet-600 text-white' : 'bg-gray-200 text-gray-800'} rounded-lg`}
                onClick={() => setActiveTab('review')}
              >
                Write a Review
              </button>
              <button
                className={`p-2 ${activeTab === 'personalize' ? 'bg-violet-600 text-white' : 'bg-gray-200 text-gray-800'} rounded-lg`}
                onClick={() => setActiveTab('personalize')}
              >
                Personalize Review
              </button>
            </div>

            {activeTab === 'ask' && (
              <AskQuestions productName={productName} fetchData={fetchData} loading={loading} />
            )}

            {activeTab === 'review' && (
              <WriteReview productName={productName} fetchData={fetchData} loading={loading} />
            )}

            {activeTab === 'personalize' && (
              <PersonalizeReview productName={productName} fetchData={fetchData} loading={loading} />
            )}
          </div>
          <div className="flex justify-center mt-6">
            <button
              onClick={resetState}
              className="bg-red-600 text-white p-3 rounded-lg shadow-md hover:bg-red-700 transition"
            >
              Enter New Product
            </button>
          </div>
        </div>
      )}
    </div>
  );
}