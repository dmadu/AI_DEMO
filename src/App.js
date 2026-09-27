const express = require('express');
const requestLogger = require('./middleware/requestLogger');
const logger = require('./utils/logger');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use(requestLogger);

// Startup lifecycle event log
logger.info('Application initializing', { event: 'startup' });

// Sample routes for testing & auth events
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  
  if (username === 'admin' && password === 'secret123') {
    logger.info('Authentication success', { event: 'auth_success', username });
    return res.status(200).json({ status: 'success', token: 'jwt-token-abc123xyz' });
  }
  
  logger.warn('Authentication failure', { event: 'auth_failure', username });
  return res.status(401).json({ status: 'error', message: 'Invalid credentials' });
});

app.get('/api/health', (req, res) => {
  logger.info('Health check requested', { event: 'health_check' });
  res.status(200).json({ status: 'UP' });
});

app.get('/api/error-test', (req, res) => {
  const err = new Error('Database connection failed');
  logger.error('Unhandled runtime error', {
    error: err.message,
    stack: err.stack,
    event: 'error'
  });
  res.status(500).json({ status: 'error', message: 'Internal Server Error' });
});

// Global error handler
app.use((err, req, res, next) => {
  logger.error('Unhandled exception caught', {
    requestId: req.requestId,
    error: err.message,
    stack: err.stack,
    event: 'exception'
  });
  res.status(500).json({ status: 'error', message: 'Internal Server Error' });
});

module.exports = app;
