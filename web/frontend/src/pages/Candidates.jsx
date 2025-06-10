import { useEffect, useState } from 'react';
import CandidateCard from '../components/CandidateCard';

function Candidates({ selectedDate, selectedSource }) {
  const [groupedCandidates, setGroupedCandidates] = useState({});

  useEffect(() => {
    fetch('http://localhost:5001/api/question_candidates/grouped')
      .then(res => res.json())
      .then(data => setGroupedCandidates(data));
  }, []);

  // 선택된 날짜와 출처가 없을 경우 안내 메시지 표시
  if (!selectedDate || !selectedSource) {
    return <div style={{ color: '#888' }}>좌측 타임라인에서 날짜와 출처를 선택해주세요.</div>;
  }

  // 선택된 날짜와 출처에 해당하는 후보 목록
  const candidatesToShow = groupedCandidates?.[selectedDate]?.[selectedSource] || [];

  // candidate_index로 후보를 정렬, 선택된 후보를 별도로 표시
  const sortedCandidates = [...candidatesToShow]
    .sort((a, b) => a.candidate_index - b.candidate_index)  // 후보 순서대로 정렬
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp)); // 타임스탬프 순으로 정렬

  return (
    <div>
      {sortedCandidates.map((c) => (
        <CandidateCard key={c.id} candidate={c} />
      ))}
    </div>
  );
}

export default Candidates;
