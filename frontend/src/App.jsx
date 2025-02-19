import React, { useState } from 'react';
import 'tailwindcss/tailwind.css';
import ProductInput from './components/ProductInput';
import Summary from './components/Summary';
import AskQuestions from './components/AskQuestions';
import WriteReview from './components/WriteReview';
import PersonalizeReview from './components/PersonalizeReview';
import ProductRatingsChart from './components/ProductRatingsChart';

const API_URL = 'http://localhost:8000';

const fetchData = async (endpoint, data, loadingKey, setLoading) => {
  try {
    setLoading((prev) => ({ ...prev, [loadingKey]: true }));
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const result = await response.json();
    setLoading((prev) => ({ ...prev, [loadingKey]: false }));
    return result;
  } catch (error) {
    console.error('Error fetching data:', error);
    setLoading((prev) => ({ ...prev, [loadingKey]: false }));
    return null;
  }
};

export default function App() {
  const [productInput, setProductInput] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [summary, setSummary] = useState('');
  const [price, setPrice] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [query, setQuery] = useState('');
  const [queryHistory, setQueryHistory] = useState([]);
  const [componentRatings, setComponentRatings] = useState({
    component_ratings: [],
    overall_rating: 0
  });
  const [loading, setLoading] = useState({
    summary: false,
    query: false,
    feedback: false,
    style: false,
    template: false,
    completion: false,
    ratings: false,
  });
  const [activeTab, setActiveTab] = useState('ask');
  const [error, setError] = useState('');

  const getProductSummary = async () => {
    const summaryData = await fetchData('/product_summary', { product_input: productInput }, 'summary', setLoading);
    if (summaryData) {
      if (summaryData.summary) {
        setSummary(summaryData.summary);
        setPrice(summaryData.price);
        setImageUrl(summaryData.image_url);
        setDisplayName(summaryData.display_name || productInput);
        setError('');
        
        // Fetch component ratings
        const ratingsData = await fetchData('/component_ratings', { product_input: productInput }, 'ratings', setLoading);
        if (ratingsData) {
          console.log('Component Ratings:', ratingsData.ratings);  // Add logging
          setComponentRatings(ratingsData.ratings || { component_ratings: [], overall_rating: 0 });
        }
      } else {
        setSummary('');
        setPrice('');
        setImageUrl('');
        setDisplayName('');
        setError('No product or review found.');
      }
    }
  };

  const answerQuery = async () => {
    if (!query.trim()) {
      setError('Please enter a question.');
      return;
    }
    
    const data = await fetchData('/answer_query', { product_name: productInput, query }, 'query', setLoading);
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
    setProductInput('');
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
          productInput={productInput}
          setProductInput={setProductInput}
          getProductSummary={getProductSummary}
          loading={loading}
        />
      ) : (
        <div>
        <Summary productName={displayName || productInput} summary={summary} error={error} />
        <div className="mt-4">
            {!error && componentRatings.component_ratings.length > 0 && (
              <div className="mt-4">
                <ProductRatingsChart 
                  componentRatings={componentRatings.component_ratings}
                  overallRating={{
                    name: 'Overall Rating',
                    value: componentRatings.overall_rating,
                    fill: '#8884d8'
                  }}
                />
              </div>
            )}
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
                  productName={displayName || productInput}
                  query={query}
                  setQuery={setQuery}
                  answerQuery={answerQuery}
                  loading={loading}
                  queryHistory={queryHistory}
                />
              )}

              {activeTab === 'review' && (
                <WriteReview productName={displayName || productInput} fetchData={(endpoint, data, loadingKey) => fetchData(endpoint, data, loadingKey, setLoading)} loading={loading} />
              )}

              {activeTab === 'personalize' && (
                <PersonalizeReview productName={displayName || productInput} fetchData={(endpoint, data, loadingKey) => fetchData(endpoint, data, loadingKey, setLoading)} loading={loading} />
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
        </div>
      )}
    </div>
  );
}