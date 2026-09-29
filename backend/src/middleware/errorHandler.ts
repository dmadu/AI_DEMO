import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';

export class AppError extends Error {
  statusCode: number;
  errors?: any;

  constructor(message: string, statusCode: number = 500, errors?: any) {
    super(message);
    this.statusCode = statusCode;
    this.errors = errors;
    Error.captureStackTrace(this, this.constructor);
  }
}

export const errorHandler = (
  err: any,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  let statusCode = err.statusCode || 500;
  let message = err.message || 'Internal Server Error';
  let errors = err.errors || undefined;

  // Handle specific library errors if any (e.g. ValidationError from express-validator or mongoose)
  if (err.name === 'ValidationError') {
    statusCode = 400;
    message = 'Validation Error';
    errors = err.errors;
  } else if (err.name === 'UnauthorizedError' || err.name === 'JsonWebTokenError') {
    statusCode = 401;
    message = 'Authentication Failed';
  } else if (err.name === 'ForbiddenError') {
    statusCode = 403;
    message = 'Forbidden';
  }

  if (statusCode >= 500) {
    logger.error('Unhandled runtime error', {
      error: {
        message: err.message,
        stack: err.stack,
        name: err.name,
      },
      path: req.path,
      method: req.method,
      ip: req.ip,
    });
  } else {
    logger.warn('Client error response', {
      statusCode,
      message,
      path: req.path,
      method: req.method,
    });
  }

  res.status(statusCode).json({
    success: false,
    error: {
      code: statusCode,
      message,
      ...(errors && { details: errors }),
    },
  });
};
