import winston from 'winston';

const sensitiveKeys = ['password', 'token', 'secret', 'authorization', 'apikey', 'api_key', 'creditcard', 'cc'];

function sanitizeValue(key: string, value: any): any {
  if (value === null || value === undefined) {
    return value;
  }
  const lowerKey = key.toLowerCase();
  if (sensitiveKeys.some(sk => lowerKey.includes(sk))) {
    return '[REDACTED]';
  }
  if (typeof value === 'object') {
    return sanitizeObject(value);
  }
  return value;
}

function sanitizeObject(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(item => (typeof item === 'object' ? sanitizeObject(item) : item));
  }
  if (obj && typeof obj === 'object') {
    const sanitized: Record<string, any> = {};
    for (const [k, v] of Object.entries(obj)) {
      sanitized[k] = sanitizeValue(k, v);
    }
    return sanitized;
  }
  return obj;
}

export const sanitizeLogMeta = winston.format((info) => {
  if (info.meta && typeof info.meta === 'object') {
    info.meta = sanitizeObject(info.meta);
  }
  // Also sanitize any extra properties passed to log methods
  for (const key of Object.keys(info)) {
    if (!['level', 'message', 'timestamp', 'stack'].includes(key)) {
      info[key] = sanitizeValue(key, info[key]);
    }
  }
  return info;
});

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    sanitizeLogMeta(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ],
});

if (process.env.NODE_ENV === 'test') {
  logger.silent = true;
}
