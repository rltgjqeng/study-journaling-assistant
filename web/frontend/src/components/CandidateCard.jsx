import React from 'react';

function CandidateCard({ candidate }) {
  const handleConfirm = () => {
    fetch(`http://localhost:5001/api/question_candidates/confirm/${candidate.id}`, {
      method: 'POST'
    }).then(() => {
      alert('질문 확정 완료!');
      window.location.reload();
    });
  };

  const handleDeny = () => {
    fetch(`http://localhost:5001/api/question_candidates/deny/${candidate.id}`, {
      method: 'POST'
    }).then(() => {
      alert('질문 거절됨');
      window.location.reload();
    });
  };

  return (
    <div style={{
      borderBottom: '1px solid #eee',
      padding: '0.5rem 0',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <div>
        <div style={{ fontWeight: 500 }}>{candidate.question_text}</div>
        <div style={{ fontSize: '0.8rem', color: '#999' }}>
          {new Date(candidate.timestamp).toLocaleTimeString()}
        </div>
      </div>
      <div>
        <button onClick={handleConfirm} style={{ marginRight: '0.5rem' }}>✔</button>
        <button onClick={handleDeny}>✖</button>
      </div>
    </div>
  );
}

export default CandidateCard;
