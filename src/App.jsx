import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Button, Card, CardContent, Typography, Box } from '@mui/material';

function Home() {
  return (
    <div className="min-h-screen bg-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-xl w-full bg-white rounded-xl shadow-lg p-8 space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-indigo-600">Frontend Initialized</h1>
          <p className="text-gray-600">
            React 19, Vite, React Router DOM, Material UI, and Tailwind CSS are successfully integrated.
          </p>
        </div>

        <div className="border-t border-gray-200 pt-6 flex flex-col items-center space-y-4">
          <h2 className="text-lg font-semibold text-gray-700">Material UI & Tailwind Integration Test</h2>
          
          <Box className="flex gap-4 items-center flex-wrap justify-center">
            <Button variant="contained" color="primary">
              MUI Contained Button
            </Button>
            <button className="px-4 py-2 bg-indigo-600 text-white font-medium rounded-lg shadow hover:bg-indigo-700 transition">
              Tailwind Button
            </button>
          </Box>

          <Card className="w-full mt-4">
            <CardContent>
              <Typography variant="h6" component="div" className="font-bold">
                MUI Card Component
              </Typography>
              <Typography variant="body2" color="text.secondary">
                This card is rendered using Material UI while surrounding layout uses Tailwind CSS classes.
              </Typography>
            </CardContent>
          </Card>
        </div>

        <div className="text-center pt-4">
          <Link to="/about" className="text-indigo-600 hover:underline font-medium">
            Go to About Page &rarr;
          </Link>
        </div>
      </div>
    </div>
  );
}

function About() {
  return (
    <div className="min-h-screen bg-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-xl w-full bg-white rounded-xl shadow-lg p-8 space-y-6 text-center">
        <h1 className="text-3xl font-bold text-indigo-600">About Page</h1>
        <p className="text-gray-600">
          Demonstrating React Router DOM navigation within the configured frontend setup.
        </p>
        <div>
          <Link to="/" className="text-indigo-600 hover:underline font-medium">
            &larr; Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}
