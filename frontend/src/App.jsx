import React from 'react';
import { Button, Typography, Card, CardContent } from '@mui/material';

function App() {
  return (
    <div className="min-h-screen bg-slate-100 flex flex-col items-center justify-center p-4">
      <Card className="max-w-lg w-full shadow-lg rounded-xl p-6">
        <CardContent className="flex flex-col items-center text-center">
          <Typography variant="h4" component="h1" className="font-bold text-indigo-600 mb-4">
            React 19 + Vite + Tailwind + MUI
          </Typography>
          <p className="text-gray-600 mb-6">
            Frontend structure successfully initialized. Tailwind utility classes and Material UI components are operating harmoniously.
          </p>
          <Button variant="contained" color="primary" className="normal-case">
            MUI Button
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default App;
