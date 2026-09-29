import React, { useState } from 'react';
import {
  Container,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Link as MuiLink,
} from '@mui/material';
import { registerUser } from '../services/authService';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    // Basic validation
    if (!username.trim() || !email.trim() || !password) {
      setError('All fields are required.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    setLoading(true);

    try {
      const response = await registerUser({ username, email, password });
      setSuccessMessage(response.message || 'Registration successful! You can now log in.');
      setUsername('');
      setEmail('');
      setPassword('');
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during registration.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4 py-12 sm:px-6 lg:px-8">
      <Container maxWidth="xs">
        <Box className="flex flex-col items-center">
          <Typography variant="h4" component="h1" className="font-bold text-slate-800 mb-6">
            Create an Account
          </Typography>
          
          <Card className="w-full shadow-lg rounded-xl border border-slate-200">
            <CardContent className="p-6 sm:p-8">
              {error && (
                <Alert severity="error" className="mb-4">
                  {error}
                </Alert>
              )}
              
              {successMessage && (
                <Alert severity="success" className="mb-4">
                  {successMessage}
                </Alert>
              )}

              <form onSubmit={handleSubmit} noValidate className="space-y-4">
                <div>
                  <TextField
                    label="Username"
                    variant="outlined"
                    fullWidth
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    disabled={loading}
                    size="medium"
                  />
                </div>

                <div>
                  <TextField
                    label="Email Address"
                    type="email"
                    variant="outlined"
                    fullWidth
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    disabled={loading}
                    size="medium"
                  />
                </div>

                <div>
                  <TextField
                    label="Password"
                    type="password"
                    variant="outlined"
                    fullWidth
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={loading}
                    size="medium"
                    helperText="Must be at least 6 characters"
                  />
                </div>

                <Button
                  type="submit"
                  variant="contained"
                  fullWidth
                  size="large"
                  disabled={loading}
                  className="mt-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg shadow-md normal-case"
                >
                  {loading ? <CircularProgress size={24} color="inherit" /> : 'Sign Up'}
                </Button>
              </form>

              <Box className="mt-6 text-center">
                <Typography variant="body2" className="text-slate-600">
                  Already have an account?{' '}
                  <MuiLink href="/login" className="text-blue-600 hover:underline font-medium">
                    Log in
                  </MuiLink>
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Container>
    </div>
  );
}
