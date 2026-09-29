# API Documentation

This document outlines the API endpoints, request and response formats, authentication methods, and error handling structure implemented in the application.

## Base URL

When running locally via Docker Compose, the base URL for API requests is:

```text
http://localhost:<PORT>
```
*(Replace `<PORT>` with the port specified in your `.env` file or `docker-compose.yml`)*

---

## Authentication

Depending on the specific endpoint, authentication may be required via HTTP headers (e.g., Bearer tokens or API keys). Refer to endpoint-specific details below.

---

## Endpoints

### 1. Health Check / Status

- **Endpoint:** `GET /health` or `GET /`
- **Description:** Verifies that the service is running and responsive.
- **Authentication:** None
- **Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "timestamp": "202X-XX-XXTXX:XX:XXZ"
  }
  ```

---

## Error Handling

The application implements centralized error handling to ensure consistent error responses across all endpoints. When an error occurs, the API returns a standard JSON error response format.

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Detailed error description here.",
    "status": 400
  }
}
```

### Common HTTP Status Codes
- `200 OK`: Request succeeded.
- `201 Created`: Resource successfully created.
- `400 Bad Request`: Invalid request parameters or payload.
- `401 Unauthorized`: Authentication credentials missing or invalid.
- `404 Not Found`: Requested resource does not exist.
- `500 Internal Server Error`: An unexpected error occurred on the server.