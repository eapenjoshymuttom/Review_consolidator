import React, { useState } from 'react';

const API_URL = 'http://localhost:8000';

export default function App() {
  const [productName, setProductName] = useState('');
  const [summary, setSummary] = useState('');
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [reviewText, setReviewText] = useState('');
  const [feedback, setFeedback] = useState('');
  const [userPreferences, setUserPreferences] = useState({
    writing_style: '',
    preferred_length: '',
    focus_areas: [],
  });
  const [stylesuggestion, setStyleSuggestion] = useState('');
  const [template, setTemplate] = useState('');

  const fetchData = async (endpoint, data) => {
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
    }
  };

  const getProductSummary = async () => {
    const data = await fetchData('/product_summary', { product_name: productName });
    if (data) setSummary(data.summary);
  };

  const answerQuery = async () => {
    const data = await fetchData('/answer_query', { product_name: productName, query });
    if (data) setAnswer(data.answer);
  };

  const getReviewFeedback = async () => {
    const data = await fetchData('/real_time_feedback', { text: reviewText });
    if (data) setFeedback(data.feedback);
  };

  const personalizeReviewStyle = async () => {
    const data = await fetchData('/personalize_review_style', userPreferences);
    if (data) setStyleSuggestion(data.style_suggestion);
  };

  const generateReviewTemplate = async () => {
    const data = await fetchData('/generate_review_template', {
      product_name: productName,
      ...userPreferences,
    });
    if (data) setTemplate(data.template);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Product Review Assistant</h1>
      
      <div className="mb-4">
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="Enter product name"
          className="border p-2 mr-2"
        />
        <button onClick={getProductSummary} className="bg-blue-500 text-white p-2 rounded">
          Get Product Summary
        </button>
      </div>
      
      {summary && (
        <div className="mb-4">
          <h2 className="text-xl font-bold">Product Summary</h2>
          <p>{summary}</p>
        </div>
      )}
      
      <div className="mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
          className="border p-2 mr-2"
        />
        <button onClick={answerQuery} className="bg-green-500 text-white p-2 rounded">
          Ask Question
        </button>
      </div>
      
      {answer && (
        <div className="mb-4">
          <h2 className="text-xl font-bold">Answer</h2>
          <p>{answer}</p>
        </div>
      )}
      
      <div className="mb-4">
        <textarea
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          placeholder="Write your review here"
          className="border p-2 w-full h-32"
        />
        <button onClick={getReviewFeedback} className="bg-yellow-500 text-white p-2 rounded mt-2">
          Get Feedback
        </button>
      </div>
      
      {feedback && (
        <div className="mb-4">
          <h2 className="text-xl font-bold">Review Feedback</h2>
          <p>{feedback}</p>
        </div>
      )}
      
      <div className="mb-4">
        <h2 className="text-xl font-bold">User Preferences</h2>
        <input
          type="text"
          value={userPreferences.writing_style}
          onChange={(e) => setUserPreferences({...userPreferences, writing_style: e.target.value})}
          placeholder="Writing style"
          className="border p-2 mr-2"
        />
        <input
          type="text"
          value={userPreferences.preferred_length}
          onChange={(e) => setUserPreferences({...userPreferences, preferred_length: e.target.value})}
          placeholder="Preferred length"
          className="border p-2 mr-2"
        />
        <input
          type="text"
          value={userPreferences.focus_areas.join(', ')}
          onChange={(e) => setUserPreferences({...userPreferences, focus_areas: e.target.value.split(', ')})}
          placeholder="Focus areas (comma-separated)"
          className="border p-2 mr-2"
        />
        <button onClick={personalizeReviewStyle} className="bg-purple-500 text-white p-2 rounded">
          Personalize Review Style
        </button>
      </div>
      
      {stylesuggestion && (
        <div className="mb-4">
          <h2 className="text-xl font-bold">Personalized Style Suggestion</h2>
          <p>{stylesuggestion}</p>
        </div>
      )}
      
      <div className="mb-4">
        <button onClick={generateReviewTemplate} className="bg-indigo-500 text-white p-2 rounded">
          Generate Review Template
        </button>
      </div>
      
      {template && (
        <div className="mb-4">
          <h2 className="text-xl font-bold">Review Template</h2>
          <pre className="whitespace-pre-wrap">{template}</pre>
        </div>
      )}
    </div>
  );
}