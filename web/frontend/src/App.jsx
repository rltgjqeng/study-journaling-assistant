import { useState, useEffect } from 'react';
import Questions from './pages/Questions';
import Candidates from './pages/Candidates';
import Tabs from './components/Tabs';
import Timeline from './components/Timeline';

function App() {
  const [activeTab, setActiveTab] = useState('questions');
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedSource, setSelectedSource] = useState(null);
  const [groupedQuestions, setGroupedQuestions] = useState({});
  const [groupedCandidates, setGroupedCandidates] = useState({});

  // 질문 데이터 그룹화
  useEffect(() => {
    fetch("http://localhost:5001/api/questions/grouped")
      .then(res => res.json())
      .then(data => setGroupedQuestions(data));
  }, []);

  // 후보 데이터 그룹화
  useEffect(() => {
    fetch("http://localhost:5001/api/question_candidates/grouped")
      .then(res => res.json())
      .then(data => setGroupedCandidates(data));
  }, []);

  // 질문과 후보를 합친 그룹핑 데이터 생성
  const mergedGroupedData = {};
  // 1) 질문 데이터 복사
  Object.entries(groupedQuestions).forEach(([date, sources]) => {
    mergedGroupedData[date] = { ...sources };
  });
  // 2) 후보 데이터 병합
  Object.entries(groupedCandidates).forEach(([date, sources]) => {
    if (!mergedGroupedData[date]) {
      mergedGroupedData[date] = {};
    }
    Object.entries(sources).forEach(([source, items]) => {
      if (!mergedGroupedData[date][source]) {
        mergedGroupedData[date][source] = [];
      }
      mergedGroupedData[date][source].push(...items);
    });
  });

  // 타임라인 보기 버튼 기능
  const handleViewTimeline = () => {
    if (selectedDate && selectedSource) {
      alert(`Selected Date: ${selectedDate}, Source: ${selectedSource}`);
    } else {
      alert("Please select both date and source from the timeline.");
    }
  };

  return (
    <div className="app-container" style={{ display: 'flex', height: '100vh' }}>
      <div style={{ width: '280px', borderRight: '1px solid #ccc', padding: '1rem' }}>
        <h2>Timeline</h2>
        <Timeline
          groupedData={mergedGroupedData}
          selectedDate={selectedDate}
          selectedSource={selectedSource}
          onSelect={(date, source) => {
            setSelectedDate(date);
            setSelectedSource(source);
          }}
        />
      </div>

      <div style={{ flex: 1, padding: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0 }}>
            {activeTab === 'questions' ? 'Questions' : 'Candidates'}
          </h2>
          <button onClick={handleViewTimeline}>View Timeline</button>
        </div>

        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

        {activeTab === 'questions' ? (
          <Questions selectedDate={selectedDate} selectedSource={selectedSource} />
        ) : (
          <Candidates selectedDate={selectedDate} selectedSource={selectedSource} />
        )}
      </div>
    </div>
  );
}

export default App;
