import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import RegisterPage from './pages/RegisterPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={
          <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <h1 className="text-2xl font-bold text-gray-800">Login Page Placeholder</h1>
          </div>
        } />
        <Route path="*" element={<Navigate to="/register" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
