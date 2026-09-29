import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { Button, Container, Typography, Box, Paper } from '@mui/material';

function Home() {
  return (
    <Container maxWidth="md" className="mt-10">
      <Paper elevation={3} className="p-8 rounded-xl bg-white">
        <Typography variant="h4" component="h1" className="text-indigo-600 font-bold mb-4">
          Welcome to React 19 + MUI + Tailwind CSS
        </Typography>
        <Typography variant="body1" className="text-gray-600 mb-6">
          This is the foundational project structure initialized with React Router DOM, Material UI, and Tailwind CSS.
        </Typography>
        <div className="flex gap-4">
          <Button variant="contained" color="primary">
            MUI Primary Button
          </Button>
          <Link to="/about">
            <Button variant="outlined" color="secondary">
              Go to About
            </Button>
          </Link>
        </div>
      </Paper>
    </Container>
  );
}

function About() {
  return (
    <Container maxWidth="md" className="mt-10">
      <Paper elevation={3} className="p-8 rounded-xl bg-white">
        <Typography variant="h4" component="h1" className="text-purple-600 font-bold mb-4">
          About Page
        </Typography>
        <Typography variant="body1" className="text-gray-600 mb-6">
          React Router is successfully integrated and working seamlessly with our component layout.
        </Typography>
        <Link to="/">
          <Button variant="contained" color="secondary">
            Back to Home
          </Button>
        </Link>
      </Paper>
    </Container>
  );
}

export default function App() {
  return (
    <Box className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm py-4 px-6 flex justify-between items-center">
        <Typography variant="h6" className="font-bold text-gray-800">
          App Architecture
        </Typography>
        <nav className="flex gap-4">
          <Link to="/" className="text-blue-600 hover:underline">Home</Link>
          <Link to="/about" className="text-blue-600 hover:underline">About</Link>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Box>
  );
}
