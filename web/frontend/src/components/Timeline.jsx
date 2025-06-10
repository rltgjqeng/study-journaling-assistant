// src/components/Timeline.jsx
function Timeline({ groupedData, selectedDate, selectedSource, onSelect }) {
  return (
    <div style={{ width: '100%', overflowY: 'auto' }}>
      {Object.entries(groupedData).map(([date, sources]) => (
        <div key={date} style={{ marginBottom: '1rem' }}>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem', color: '#2a7f62' }}>{date}</div>
          <ul style={{ marginLeft: '1rem' }}>
            {Object.keys(sources).map(source => (
              <li key={source}>
                <button
                  style={{
                    background: date === selectedDate && source === selectedSource ? '#d4f4e4' : 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    textAlign: 'left',
                    padding: '0.3rem 0',
                    color: '#333',
                  }}
                  onClick={() => onSelect(date, source)}
                >
                  {source}
                </button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default Timeline;
