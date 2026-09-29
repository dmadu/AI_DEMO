import request from 'supertest';
import app from '../app';
import { logger } from '../utils/logger';

describe('Centralised Error Handling & Structured Logging', () => {
  beforeAll(() => {
    // Ensure logger is silent or mock info/error if needed
  });

  it('should return 400 and standardised JSON for validation failures / bad requests', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ username: 'admin' }); // missing password

    expect(response.status).toBe(400);
    expect(response.body).toEqual({
      success: false,
      error: {
        code: 400,
        message: 'Username and password are required',
      },
    });
  });

  it('should return 401 for authentication failure', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ username: 'admin', password: 'wrongpassword' });

    expect(response.status).toBe(401);
    expect(response.body).toEqual({
      success: false,
      error: {
        code: 401,
        message: 'Invalid credentials',
      },
    });
  });

  it('should return 500 and standardised JSON for unhandled exceptions', async () => {
    const response = await request(app).get('/api/error-test');

    expect(response.status).toBe(500);
    expect(response.body).toEqual({
      success: false,
      error: {
        code: 500,
        message: 'Unexpected server crash exception',
      },
    });
  });

  it('should return 404 for non-existent routes', async () => {
    const response = await request(app).get('/api/non-existent-route');

    expect(response.status).toBe(404);
    expect(response.body).toEqual({
      success: false,
      error: {
        code: 404,
        message: 'Resource not found',
      },
    });
  });

  it('should redact sensitive information from logs during auth and db errors', (done) => {
    const spy = jest.spyOn(logger, 'info');
    const spyError = jest.spyOn(logger, 'error');

    request(app)
      .post('/api/auth/login')
      .send({ username: 'admin', password: 'mypassword123', token: 'secret-token-abc' })
      .end(() => {
        // Verify that calls to logger contain redacted password/token in meta or arguments
        const allCalls = [...spy.mock.calls, ...spyError.mock.calls];
        for (const call of allCalls) {
          const callString = JSON.stringify(call);
          if (callString.includes('mypassword123') || callString.includes('secret-token-abc')) {
            throw new Error('Sensitive data leaked in logs!');
          }
        }
        spy.mockRestore();
        spyError.mockRestore();
        done();
      });
  });
});
