# Company API

This document provides documentation for the Company API.

## GET /api/company/{id}

Retrieves a company by its ID.

**Request**

*   **Path Parameters**
    *   `id` (string): The UUID of the company.

**Response (200 OK)**

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "name": "Drama Llama Inc.",
  "description": "The best company for all your drama llama needs."
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} Company
 * @property {string} id
 * @property {string} name
 * @property {string} description
 */
```

## GET /api/company/my

Retrieves the company of the currently authenticated user.

**Authentication**

This endpoint requires the user to be authenticated and have the `RECRUITER` role.

**Response (200 OK)**

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "name": "Drama Llama Inc.",
  "description": "The best company for all your drama llama needs."
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} Company
 * @property {string} id
 * @property {string} name
 * @property {string} description
 */
```
