// src/components/QuestionCard.jsx
function QuestionCard({ question }) {
  return (
    <div style={{ border: '1px solid #ccc', margin: '0.5rem', padding: '0.5rem', borderRadius: '8px' }}>
      <div><strong>📌 하이라이트:</strong> {question.highlight}</div>
      <div><strong>📝 메모:</strong> {question.memo || '없음'}</div>
      <div style={{ fontSize: '0.85rem', color: '#666' }}>
        {question.source} - {new Date(question.timestamp).toLocaleString()}
      </div>
    </div>
  );
}

export default QuestionCard;
