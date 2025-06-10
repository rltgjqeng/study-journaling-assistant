// src/components/Tabs.jsx
function Tabs({ activeTab, setActiveTab }) {
  return (
    <div style={{ marginTop: '1rem', display: 'flex', borderBottom: '1px solid #ccc' }}>
      <button
        onClick={() => setActiveTab('questions')}
        style={{
          padding: '0.5rem 1rem',
          borderBottom: activeTab === 'questions' ? '2px solid green' : 'none'
        }}
      >
        Questions
      </button>
      <button
        onClick={() => setActiveTab('candidates')}
        style={{
          padding: '0.5rem 1rem',
          borderBottom: activeTab === 'candidates' ? '2px solid green' : 'none'
        }}
      >
        Candidates
      </button>
    </div>
  )
}

export default Tabs
