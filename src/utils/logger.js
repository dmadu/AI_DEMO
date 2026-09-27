const SENSITIVE_KEYS = [
  'password',
  'token',
  'secret',
  'authorization',
  'credit_card',
  'card_number',
  'ssn',
  'api_key'
];

function sanitizeValue(key, value) {
  if (value === null || value === undefined) {
    return value;
  }
  
  const lowerKey = String(key).toLowerCase();
  if (SENSITIVE_KEYS.some(sk => lowerKey.includes(sk))) {
    return '[REDACTED]';
  }

  if (typeof value === 'string') {
    // Check if it looks like a bearer token or sensitive header value
    if (lowerKey === 'authorization' || value.startsWith('Bearer ')) {
      return '[REDACTED]';
    }
    return value;
  }

  if (Array.isArray(value)) {
    return value.map((item, idx) => sanitizeValue(idx, item));
  }

  if (typeof value === 'object') {
    return sanitizeObject(value);
  }

  return value;
}

function sanitizeObject(obj) {
  if (!obj || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => sanitizeObject(item));
  }

  const sanitized = {};
  for (const [key, value] of Object.entries(obj)) {
    sanitized[key] = sanitizeValue(key, value);
  }
  return sanitized;
}

function formatLog(level, message, meta = {}) {
  const sanitizedMeta = sanitizeObject(meta);
  const logEntry = {
    timestamp: new Date().toISOString(),
    level: level.toUpperCase(),
    message,
    ...sanitizedMeta
  };
  return JSON.stringify(logEntry);
}

const logger = {
  info(message, meta) {
    console.log(formatLog('info', message, meta));
  },
  error(message, meta) {
    console.error(formatLog('error', message, meta));
  },
  warn(message, meta) {
    console.warn(formatLog('warn', message, meta));
  },
  debug(message, meta) {
    console.debug(formatLog('debug', message, meta));
  },
  sanitize(data) {
    return sanitizeObject(data);
  }
};

module.exports = logger;
