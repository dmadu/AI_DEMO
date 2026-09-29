import React, { useEffect, useState } from 'react';

function App() {
  const [backendStatus, setBackendStatus] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/health')
      .then(res => res.json())
      .then(data => setBackendStatus(data))
      .catch(err => setBackendStatus({ status: 'error', message: err.toString() }));
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Project Setup & Architecture</h1>
      <p>React Frontend is running successfully!</p>
      <h2>Backend & Database Status:</h2>
      <pre style={{ background: '#f4f4f4', padding: '10px' }}>
        {JSON.stringify(backendStatus, null, 2)}
      </pre>
    </div>
  );
}

export default App;
