import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Container, Typography, Button, Box, AppBar, Toolbar } from '@mui/material';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './components/Dashboard';

const Home = () => (
  <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'grey.100' }}>
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          My App
        </Typography>
        <Button color="inherit" component={Link} to="/login">
          Login
        </Button>
        <Button color="inherit" component={Link} to="/dashboard">
          Dashboard
        </Button>
      </Toolbar>
    </AppBar>
    <Container maxWidth="sm" sx={{ mt: 8, textAlign: 'center' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome to Home Page
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Please login to access your protected user dashboard.
      </Typography>
      <Box sx={{ mt: 4 }}>
        <Button variant="contained" color="primary" component={Link} to="/login" sx={{ mr: 2 }}>
          Go to Login
        </Button>
        <Button variant="outlined" color="primary" component={Link} to="/dashboard">
          Go to Dashboard
        </Button>
      </Box>
    </Container>
  </Box>
);

const LoginPlaceholder = () => {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [error, setError] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [success, setSuccess] = React.useState(false);
  const navigate = React.useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (response.ok && data.token) {
        localStorage.setItem('token', data.token);
        setSuccess(true);
        setTimeout(() => {
          navigate('/dashboard');
        }, 500);
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      setError('Network error or server unavailable');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 8 }}>
      <Box sx={{ p: 4, boxShadow: 3, borderRadius: 2, bgcolor: 'background.paper' }}>
        <Typography variant="h5" gutterBottom align="center">
          Login
        </Typography>
        {error && <Typography color="error" variant="body2" sx={{ mb: 2 }}>{error}</Typography>}
        {success && <Typography color="success.main" variant="body2" sx={{ mb: 2 }}>Login successful! Redirecting...</Typography>}
        <form onSubmit={handleLogin}>
          <Box sx={{ mb: 2 }}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{ width: '100%', padding: '10px', fontSize: '1rem', boxSizing: 'border-box' }}
            />
          </Box>
          <Box sx={{ mb: 2 }}>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ width: '100%', padding: '10px', fontSize: '1rem', boxSizing: 'border-box' }}
            />
          </Box>
          <Button type="submit" variant="contained" color="primary" fullWidth disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </Button>
        </form>
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Button component={Link} to="/" size="small">
            Back to Home
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginPlaceholder />} />
        
        {/* Protected Dashboard Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
        </Route>
      </Routes>
    </Router>
  );
}

App.defaultProps = {};

export default App;
