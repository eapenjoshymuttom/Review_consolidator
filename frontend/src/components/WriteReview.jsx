import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function WriteReview({ productName, fetchData, loading }) {
  const [reviewText, setReviewText] = useState('');
  const [completionResult, setCompletionResult] = useState('');
  const [feedback, setFeedback] = useState('');

  const getTextCompletion = async () => {
    const data = await fetchData('/text_completion', { text: reviewText }, 'completion');
    if (data) {
      setCompletionResult(data.completion);
      setReviewText(data.completion); // Update reviewText with the completed text
    }
  };

  const getReviewFeedback = async () => {
    const data = await fetchData('/real_time_feedback', { text: reviewText }, 'feedback');
    if (data) setFeedback(data.feedback);
  };

  return (
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
          <ReactMarkdown>{feedback}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}