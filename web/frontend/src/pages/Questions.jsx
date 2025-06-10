// src/pages/Questions.jsx
import { useEffect, useState } from 'react';
import QuestionCard from '../components/QuestionCard';

function Questions({ selectedDate, selectedSource }) {
  const [groupedQuestions, setGroupedQuestions] = useState({});

  useEffect(() => {
    fetch("http://localhost:5001/api/questions/grouped")
      .then(res => res.json())
      .then(data => setGroupedQuestions(data));
  }, []);

  // 🛡️ selectedDate 또는 selectedSource가 아직 선택되지 않은 경우
  if (!selectedDate || !selectedSource) {
    return <div style={{ color: '#888' }}>좌측 타임라인에서 날짜와 출처를 선택해주세요.</div>;
  }

  const questionsToShow = groupedQuestions?.[selectedDate]?.[selectedSource] || [];

  const sorted = [...questionsToShow].sort(
    (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
  );

  return (
    <div>
      {sorted.map((q) => (
        <QuestionCard key={q.id} question={q} />
      ))}
    </div>
  );
}

export default Questions;
