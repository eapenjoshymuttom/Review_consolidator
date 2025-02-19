import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function PersonalizeReview({ productName, fetchData, loading, setLoading }) {
  const [userPreferences, setUserPreferences] = useState({
    writing_style: '',
    preferred_length: '',
    focus_areas: [],
  });
  const [stylesuggestion, setStyleSuggestion] = useState('');
  const [template, setTemplate] = useState('');

  const personalizeReviewStyle = async () => {
    const data = await fetchData('/personalize_review_style', userPreferences, 'style', setLoading);
    if (data) setStyleSuggestion(data.style_suggestion);
  };

  const generateReviewTemplate = async () => {
    const data = await fetchData('/generate_review_template', {
      product_name: productName,
      ...userPreferences,
    }, 'template', setLoading);
    if (data) setTemplate(data.template);
  };

  return (
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
      <div className="flex space-x-4">
        <button
          onClick={personalizeReviewStyle}
          className="bg-purple-600 text-white p-3 rounded-lg shadow-md hover:bg-purple-700 transition mb-4"
          disabled={loading.style}
        >
          {loading.style ? 'Loading...' : 'Personalize Review Style'}
        </button>
        <button
          onClick={generateReviewTemplate}
          className="bg-indigo-600 text-white p-3 rounded-lg shadow-md hover:bg-indigo-700 transition mb-4"
          disabled={loading.template}
        >
          {loading.template ? 'Loading...' : 'Generate Review Template'}
        </button>
      </div>
      {stylesuggestion && (
        <div className="mt-4">
          <h3 className="text-lg font-bold mb-2">Personalized Style Suggestion</h3>
          <ReactMarkdown>{stylesuggestion}</ReactMarkdown>
        </div>
      )}
      {template && (
        <div className="mt-4">
          <h3 className="text-lg font-bold mb-2">Review Template</h3>
          <ReactMarkdown>{template}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}