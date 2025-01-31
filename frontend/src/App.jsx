import React, { useState } from 'react';
import 'tailwindcss/tailwind.css';
import ProductInput from './components/ProductInput';
import Summary from './components/Summary';
import AskQuestions from './components/AskQuestions';
import WriteReview from './components/WriteReview';
import PersonalizeReview from './components/PersonalizeReview';
import { ReviewChart } from './components/ReviewChart';

const API_URL = 'http://localhost:8000';

const chartData = [
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
]

export default function App() {
  const [productName, setProductName] = useState('');
  const [summary, setSummary] = useState('');
  const [price, setPrice] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [query, setQuery] = useState('');
  const [queryHistory, setQueryHistory] = useState([]);
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
    setError('');  // Clear any previous errors
    
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      
      const responseData = await response.json();
      
      if (!response.ok) {
        throw new Error(responseData.detail || `HTTP error! status: ${response.status}`);
      }
      
      return responseData;
    } catch (error) {
      console.error(`Error fetching data from ${endpoint}:`, error);
      setError(error.message || 'An error occurred while fetching data.');
      return null;
    } finally {
      setLoading((prev) => ({ ...prev, [loadingKey]: false }));
    }
  };

  const getProductSummary = async () => {
    const data = await fetchData('/product_summary', { product_name: productName }, 'summary');
    if (data) {
      if (data.summary) {
        setSummary(data.summary);
        setPrice(data.price);
        setImageUrl(data.image_url);
        setError('');
      } else {
        setSummary('');
        setPrice('');
        setImageUrl('');
        setError('No product or review found.');
      }
    }
  };

  const answerQuery = async () => {
    if (!query.trim()) {
      setError('Please enter a question.');
      return;
    }
    
    const data = await fetchData('/answer_query', { product_name: productName, query }, 'query');
    if (data) {
      if (data.answer) {
        setQueryHistory((prev) => [...prev, { question: query, answer: data.answer }]);
        setQuery('');
        setError('');
      } else {
        setError('No answer found. Please try rephrasing your question.');
      }
    } else {
      setError('Failed to get answer. Please try again later.');
    }
  };

  const resetState = () => {
    setProductName('');
    setSummary('');
    setQuery('');
    setQueryHistory([]);
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
          {/* <ReviewChart data={chartData} /> */}
          {/* New Section for Price and Image */}
          <div className="p-4 bg-white rounded-lg shadow-md mt-4">
            <h3 className="text-xl font-semibold">Product Details</h3>
            <p className="text-lg text-gray-700">Price: {price || "N/A"}</p>
            {imageUrl && (
              <img src={imageUrl} alt="Product" className="mt-2 w-40 h-auto rounded-lg shadow-md" />
            )}
          </div>
           
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
              <AskQuestions
                productName={productName}
                query={query}
                setQuery={setQuery}
                answerQuery={answerQuery}
                loading={loading}
                queryHistory={queryHistory}
              />
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