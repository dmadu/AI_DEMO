# API Documentation

This document details all REST endpoints exposed by the application, including request methods, URL paths, headers, expected request payloads, query parameters, path variables, and standard response structures.

## Base URL
`http://localhost:3000/api` (or relative to your configured server root)

---

## Standard Response Formats

### Success Response Structure
```json
{
  "success": true,
  "status": 200,
  "data": {}
}
```

### Error Response Structure
```json
{
  "success": false,
  "status": 400,
  "error": {
    "code": "BAD_REQUEST",
    "message": "Detailed error description"
  }
}
```

---

## Endpoints

### 1. Health Check
- **URL:** `/health` or `/`
- **Method:** `GET`
- **Description:** Verifies that the API server is up and running.
- **Success Response:**
  - **Status:** `200 OK`
  - **Payload:** `{"status": "ok", "uptime": 12345}`

### 2. User Management & Authentication
Depending on the implemented routes in `src/routes`, standard CRUD endpoints apply:

- **GET `/api/users`**
  - **Description:** Retrieve a list of users.
  - **Query Parameters:** `limit` (number), `page` (number)
  - **Success Response (`200 OK`):** List of user objects.

- **POST `/api/users`**
  - **Description:** Create a new user.
  - **Request Payload:**
    ```json
    {
      "username": "johndoe",
      "email": "john@example.com",
      "password": "securePassword123"
    }
    ```
  - **Success Response (`201 Created`):** Created user object.

- **GET `/api/users/:id`**
  - **Description:** Retrieve a specific user by ID.
  - **Path Variables:** `id` (string/number)
  - **Success Response (`200 OK`):** User object.

- **PUT `/api/users/:id`**
  - **Description:** Update an existing user.
  - **Path Variables:** `id` (string/number)
  - **Request Payload:** Partial or full user object.
  - **Success Response (`200 OK`):** Updated user object.

- **DELETE `/api/users/:id`**
  - **Description:** Delete a user.
  - **Path Variables:** `id` (string/number)
  - **Success Response (`204 No Content`):** Empty body.
