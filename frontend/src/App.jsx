import React, { useState, useEffect } from 'react'

function App() {
  const [message, setMessage] = useState('Loading...')
  const [dbStatus, setDbStatus] = useState('Checking...')

  useEffect(() => {
    fetch('http://localhost:5000/api/health')
      .then(res => res.json())
      .then(data => {
        setMessage(data.status)
        setDbStatus(data.database)
      })
      .catch(err => {
        setMessage('Error connecting to backend')
        setDbStatus('disconnected')
      })
  }, [])

  return (
    <div style={{ fontFamily: 'sans-serif', textAlign: 'center', marginTop: '50px' }}>
      <h1>React 19 + Flask + PostgreSQL Monorepo</h1>
      <p>Backend Status: <strong>{message}</strong></p>
      <p>Database Status: <strong>{dbStatus}</strong></p>
    </div>
  )
}

export default App
