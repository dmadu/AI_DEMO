const logger = require('../utils/logger');

function requestLogger(req, res, next) {
  const startTime = Date.now();
  const requestId = req.headers['x-request-id'] || `req-${Math.random().toString(36).substr(2, 9)}`;
  req.requestId = requestId;
  res.setHeader('X-Request-ID', requestId);

  // Sanitize query params and body for logging
  const sanitizedQuery = logger.sanitize(req.query);
  const sanitizedBody = logger.sanitize(req.body);
  const sanitizedHeaders = logger.sanitize({
    'user-agent': req.headers['user-agent'],
    'content-type': req.headers['content-type'],
    'authorization': req.headers['authorization']
  });

  logger.info('Incoming API Request', {
    requestId,
    method: req.method,
    path: req.path,
    query: sanitizedQuery,
    body: sanitizedBody,
    headers: sanitizedHeaders
  });

  const originalSend = res.send;
  let responseBody;
  res.send = function(body) {
    responseBody = body;
    return originalSend.apply(this, arguments);
  };

  res.on('finish', () => {
    const durationMs = Date.now() - startTime;
    logger.info('Outgoing API Response', {
      requestId,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      durationMs
    });
  });

  next();
}

module.exports = requestLogger;
