const request = require('supertest');
const app = require('../src/app');
const logger = require('../src/utils/logger');

describe('Structured Logging and Sanitization Tests', () => {
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  test('API requests correctly emit structured logs containing metadata', async () => {
    const response = await request(app)
      .get('/api/health')
      .set('X-Request-ID', 'test-req-123');

    expect(response.status).toBe(200);
    
    const logs = consoleLogSpy.mock.calls.map(call => JSON.parse(call[0]));
    
    const incomingLog = logs.find(l => l.message === 'Incoming API Request');
    expect(incomingLog).toBeDefined();
    expect(incomingLog.requestId).toBe('test-req-123');
    expect(incomingLog.method).toBe('GET');
    expect(incomingLog.path).toBe('/api/health');
    expect(incomingLog.timestamp).toBeDefined();
    expect(incomingLog.level).toBe('INFO');

    const outgoingLog = logs.find(l => l.message === 'Outgoing API Response');
    expect(outgoingLog).toBeDefined();
    expect(outgoingLog.requestId).toBe('test-req-123');
    expect(outgoingLog.statusCode).toBe(200);
    expect(outgoingLog.durationMs).toBeDefined();
  });

  test('Authentication attempts and sensitive payloads are successfully redacted', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .set('Authorization', 'Bearer super-secret-token-xyz')
      .send({
        username: 'admin',
        password: 'mySuperSecretPassword',
        token: 'some-token-value',
        secret: 'top-secret',
        credit_card: '1234-5678-9012-3456'
      });

    expect(response.status).toBe(200);

    const logs = consoleLogSpy.mock.calls.map(call => JSON.parse(call[0]));
    const incomingLog = logs.find(l => l.message === 'Incoming API Request');
    
    expect(incomingLog).toBeDefined();
    expect(incomingLog.body.password).toBe('[REDACTED]');
    expect(incomingLog.body.token).toBe('[REDACTED]');
    expect(incomingLog.body.secret).toBe('[REDACTED]');
    expect(incomingLog.body.credit_card).toBe('[REDACTED]');
    expect(incomingLog.headers.authorization).toBe('[REDACTED]');

    const authSuccessLog = logs.find(l => l.message === 'Authentication success');
    expect(authSuccessLog).toBeDefined();
    expect(authSuccessLog.event).toBe('auth_success');
    expect(authSuccessLog.username).toBe('admin');
    // Verify no password or secret leaked in auth success log
    expect(JSON.stringify(authSuccessLog)).not.toContain('mySuperSecretPassword');
  });

  test('Error logs capture contextual stack traces and details', async () => {
    const response = await request(app).get('/api/error-test');
    expect(response.status).toBe(500);

    const errorLogs = consoleErrorSpy.mock.calls.map(call => JSON.parse(call[0]));
    const errorLog = errorLogs.find(l => l.message === 'Unhandled runtime error');

    expect(errorLog).toBeDefined();
    expect(errorLog.level).toBe('ERROR');
    expect(errorLog.error).toBe('Database connection failed');
    expect(errorLog.stack).toBeDefined();
  });

  test('Logger sanitize handles nested objects and arrays correctly', () => {
    const payload = {
      user: {
        name: 'John Doe',
        password: 'plainpassword',
        address: {
          street: '123 Main St',
          secret_code: '9999'
        }
      },
      tokens: ['token1', 'token2']
    };

    const sanitized = logger.sanitize(payload);
    expect(sanitized.user.name).toBe('John Doe');
    expect(sanitized.user.password).toBe('[REDACTED]');
    expect(sanitized.user.address.street).toBe('123 Main St');
    expect(sanitized.user.address.secret_code).toBe('[REDACTED]');
  });
});
