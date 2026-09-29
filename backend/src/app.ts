import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { logger } from './utils/logger';
import { errorHandler, AppError } from './middleware/errorHandler';

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());

// Morgan HTTP request logging with winston stream
app.use(
  morgan(':method :url :status :res[content-length] - :response-time ms', {
    stream: {
      write: (message: string) => logger.info(message.trim()),
    },
  })
);

// Example auth attempt route showcasing structured logging & sanitization
app.post('/api/auth/login', (req, res, next) => {
  const { username, password, token } = req.body;
  logger.info('Authentication attempt', { username, password, token });

  if (!username || !password) {
    return next(new AppError('Username and password are required', 400));
  }

  if (username === 'admin' && password === 'secret123') {
    return res.json({ success: true, token: 'mock-jwt-token-xyz' });
  }

  return next(new AppError('Invalid credentials', 401));
});

// Example database failure simulation route
app.get('/api/db-test', (req, res, next) => {
  logger.error('Database connection failed', { dbHost: 'localhost', password: 'db_secret_password' });
  return next(new AppError('Database connection error', 500));
});

// Example unhandled exception test route
app.get('/api/error-test', (req, res, next) => {
  throw new Error('Unexpected server crash exception');
});

// 404 handler
app.use((req, res, next) => {
  next(new AppError('Resource not found', 404));
});

// Centralised Error Handler
app.use(errorHandler);

export default app;
