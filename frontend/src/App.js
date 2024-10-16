import React, { useState } from 'react';
import 'tailwindcss/tailwind.css';

const API_URL = 'http://localhost:8000';

export default function App() {
  const [productName, setProductName] = useState('');
  const [summary, setSummary] = useState('');
  const [query, setQuery] = useState('');
  const [questions, setQuestions] = useState([]);
  const [reviewText, setReviewText] = useState('');
  const [feedback, setFeedback] = useState('');
  const [userPreferences, setUserPreferences] = useState({
    writing_style: '',
    preferred_length: '',
    focus_areas: [],
  });
  const [stylesuggestion, setStyleSuggestion] = useState('');
  const [template, setTemplate] = useState('');
  const [loading, setLoading] = useState({
    summary: false,
    query: false,
    feedback: false,
    style: false,
    template: false,
    completion: false,
  });
  const [activeTab, setActiveTab] = useState('ask');
  const [completionResult, setCompletionResult] = useState('');

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
    } finally {
      setLoading((prev) => ({ ...prev, [loadingKey]: false }));
    }
  };

  const getProductSummary = async () => {
    const data = await fetchData('/product_summary', { product_name: productName }, 'summary');
    if (data) setSummary(data.summary);
  };

  const answerQuery = async () => {
    const data = await fetchData('/answer_query', { product_name: productName, query }, 'query');
    if (data) {
      setQuestions((prev) => [...prev, { query, answer: data.answer }]);
      setQuery('');
    }
  };

  const getReviewFeedback = async () => {
    const data = await fetchData('/real_time_feedback', { text: reviewText }, 'feedback');
    if (data) setFeedback(data.feedback);
  };

  const personalizeReviewStyle = async () => {
    const data = await fetchData('/personalize_review_style', userPreferences, 'style');
    if (data) setStyleSuggestion(data.style_suggestion);
  };

  const generateReviewTemplate = async () => {
    const data = await fetchData('/generate_review_template', {
      product_name: productName,
      ...userPreferences,
    }, 'template');
    if (data) setTemplate(data.template);
  };

  const getTextCompletion = async () => {
    const data = await fetchData('/text_completion', { text: reviewText }, 'completion');
    if (data) {
      setCompletionResult(data.completion);
      setReviewText(data.completion); // Update reviewText with the completed text
    }
  };

  const resetState = () => {
    setProductName('');
    setSummary('');
    setQuery('');
    setQuestions([]);
    setReviewText('');
    setFeedback('');
    setUserPreferences({
      writing_style: '',
      preferred_length: '',
      focus_areas: [],
    });
    setStyleSuggestion('');
    setTemplate('');
    setCompletionResult('');
    setActiveTab('ask');
  };

  return (
    <div className="container mx-auto p-6 bg-gray-100 min-h-screen">
      {!summary ? (
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
      ) : (
        <div>
          <div className="mb-6 p-4 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-2">Review Summary of {productName}</h2>
            <p className="text-gray-700">{summary}</p>
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
            )}

            {activeTab === 'review' && (
              <div>
                <h2 className="text-xl font-bold mb-4">Write a Review</h2>
                <textarea
                  value={reviewText}
                  onChange={(e) => setReviewText(e.target.value)}
                  placeholder="Write your review here"
                  className="border p-3 rounded-lg shadow-sm w-full h-32 mb-4"
                />
                <button
                  onClick={getTextCompletion}
                  className="bg-teal-600 mr-10 text-white p-3 rounded-lg shadow-md hover:bg-teal-700 transition mb-4"
                  disabled={loading.completion}
                >
                  {loading.completion ? 'Loading...' : 'Complete Text'}
                </button>
                {completionResult && (
                  <div className="mt-4">
                    <h3 className="text-lg font-bold mb-2">Completion Result</h3>
                    <pre className="whitespace-pre-wrap text-gray-700">{completionResult}</pre>
                  </div>
                )}
                <button
                  onClick={getReviewFeedback}
                  className="bg-blue-600 text-white p-3 rounded-lg shadow-md hover:bg-blue-700 transition"
                  disabled={loading.feedback}
                >
                  {loading.feedback ? 'Loading...' : 'Get Feedback'}
                </button>
                {feedback && (
                  <div className="mt-4">
                    <h3 className="text-lg font-bold mb-2">Review Feedback</h3>
                    <p className="text-gray-700">{feedback}</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'personalize' && (
              <div>
                <h2 className="text-xl font-bold mb-4">User Preferences</h2>
                <input
                  type="text"
                  value={userPreferences.writing_style}
                  onChange={(e) => setUserPreferences({...userPreferences, writing_style: e.target.value})}
                  placeholder="Writing style"
                  className="border p-3 rounded-lg shadow-sm w-full mb-4"
                />
                <input
                  type="text"
                  value={userPreferences.preferred_length}
                  onChange={(e) => setUserPreferences({...userPreferences, preferred_length: e.target.value})}
                  placeholder="Preferred length"
                  className="border p-3 rounded-lg shadow-sm w-full mb-4"
                />
                <input
                  type="text"
                  value={userPreferences.focus_areas.join(', ')}
                  onChange={(e) => setUserPreferences({...userPreferences, focus_areas: e.target.value.split(', ')})}
                  placeholder="Focus areas (comma-separated)"
                  className="border p-3 rounded-lg shadow-sm w-full mb-4"
                />
                <button
                  onClick={personalizeReviewStyle}
                  className="bg-purple-600 mr-10 text-white p-3 rounded-lg shadow-md hover:bg-purple-700 transition mb-4"
                  disabled={loading.style}
                >
                  {loading.style ? 'Loading...' : 'Personalize Review Style'}
                </button>
                {stylesuggestion && (
                  <div className="mt-4">
                    <h3 className="text-lg font-bold mb-2">Personalized Style Suggestion</h3>
                    <p className="text-gray-700">{stylesuggestion}</p>
                  </div>
                )}
                <button
                  onClick={generateReviewTemplate}
                  className="bg-indigo-600 text-white p-3 rounded-lg shadow-md hover:bg-indigo-700 transition mt-4"
                  disabled={loading.template}
                >
                  {loading.template ? 'Loading...' : 'Generate Review Template'}
                </button>
                {template && (
                  <div className="mt-4">
                    <h3 className="text-lg font-bold mb-2">Review Template</h3>
                    <pre className="whitespace-pre-wrap text-gray-700">{template}</pre>
                  </div>
                )}
              </div>
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