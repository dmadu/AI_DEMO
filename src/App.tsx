import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container, Box, Paper } from '@mui/material';

const Home: React.FC = () => (
  <Box className="py-8">
    <Paper elevation={3} className="p-6 rounded-xl bg-white">
      <Typography variant="h4" component="h1" className="text-blue-600 font-bold mb-4">
        Welcome to React 19 + MUI + Tailwind CSS
      </Typography>
      <Typography variant="body1" className="text-gray-700 mb-6">
        This application is fully configured with TypeScript, Material UI, Tailwind CSS, and React Router DOM.
      </Typography>
      <div className="flex gap-4">
        <Button variant="contained" color="primary" component={Link} to="/about">
          Go to About
        </Button>
      </div>
    </Paper>
  </Box>
);

const About: React.FC = () => (
  <Box className="py-8">
    <Paper elevation={3} className="p-6 rounded-xl bg-white">
      <Typography variant="h4" component="h1" className="text-indigo-600 font-bold mb-4">
        About Page
      </Typography>
      <Typography variant="body1" className="text-gray-700 mb-6">
        Demonstrating public routing using React Router DOM.
      </Typography>
      <Button variant="outlined" color="primary" component={Link} to="/">
        Back to Home
      </Button>
    </Paper>
  </Box>
);

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" className="flex-grow">
            App Frontend
          </Typography>
          <Button color="inherit" component={Link} to="/">
            Home
          </Button>
          <Button color="inherit" component={Link} to="/about">
            About
          </Button>
        </Toolbar>
      </AppBar>
      <Container component="main" className="flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Container>
      <Box component="footer" className="py-4 text-center text-gray-500 bg-white border-t">
        <Typography variant="body2">
          &copy; {new Date().getFullYear()} React 19 Application. All rights reserved.
        </Typography>
      </Box>
    </div>
  );
}
