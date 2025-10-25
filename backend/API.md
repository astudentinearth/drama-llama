# API Documentation

This document provides documentation for the backend API of the Drama Llama application.

## Jobs API

### GET /api/jobs

Retrieves a list of all job listings.

**Response (200 OK)**

```json
{
  "jobs": [
    {
      "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "title": "Software Engineer",
      "content": "We are looking for a skilled software engineer to join our team.",
      "tags": ["Java", "Spring", "React"],
      "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
      "active": true
    }
  ]
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} JobListing
 * @property {string} id
 * @property {string} title
 * @property {string} content
 * @property {string[]} tags
 * @property {string} userId
 * @property {boolean} active
 */

/**
 * @typedef {object} JobListingsResponse
 * @property {JobListing[]} jobs
 */
```

### GET /api/jobs/{id}

Retrieves a specific job listing by its ID.

**Request**

*   **Path Parameters**
    *   `id` (string): The UUID of the job listing.

**Response (200 OK)**

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "title": "Software Engineer",
  "content": "We are looking for a skilled software engineer to join our team.",
  "tags": ["Java", "Spring", "React"],
  "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
  "active": true
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} JobListing
 * @property {string} id
 * @property {string} title
 * @property {string} content
 * @property {string[]} tags
 * @property {string} userId
 * @property {boolean} active
 */
```

### POST /api/jobs

Creates a new job listing.

**Request Body**

```json
{
  "title": "Senior Software Engineer",
  "content": "We are hiring a senior software engineer.",
  "tags": ["Java", "Spring Boot", "Microservices"],
  "active": true
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} CreateJobListing
 * @property {string} title
 * @property {string} content
 * @property {string[]} tags
 * @property {boolean} active
 */
```

**Response (200 OK)**

```json
{
  "id": "c3d4e5f6-a7b8-9012-3456-7890abcdef12",
  "title": "Senior Software Engineer",
  "content": "We are hiring a senior software engineer.",
  "tags": ["Java", "Spring Boot", "Microservices"],
  "userId": "d4e5f6a7-b8c9-0123-4567-890abcdef123",
  "active": true
}
```

### PATCH /api/jobs/{id}

Updates an existing job listing.

**Request**

*   **Path Parameters**
    *   `id` (string): The UUID of the job listing.

*   **Request Body**

    ```json
    {
      "title": "Principal Software Engineer",
      "content": "We are looking for a principal software engineer.",
      "tags": ["Java", "Spring", "AWS", "React"],
      "active": true
    }
    ```

**Response (200 OK)**

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "title": "Principal Software Engineer",
  "content": "We are looking for a principal software engineer.",
  "tags": ["Java", "Spring", "AWS", "React"],
  "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
  "active": true
}
```

### POST /api/jobs/{jobId}/applications

Creates or updates a job application for a specific job.

**Request**

*   **Path Parameters**
    *   `jobId` (string): The UUID of the job listing.

*   **Request Body**

    ```json
    {
      "message": "I am very interested in this position."
    }
    ```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} CreateJobApplication
 * @property {string} message
 */
```

**Response (200 OK)**

```json
{
  "id": "e5f6a7b8-c9d0-1234-5678-90abcdef1234",
  "jobListingId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
  "message": "I am very interested in this position."
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} JobApplication
 * @property {string} id
 * @property {string} jobListingId
 * @property {string} userId
 * @property {string} message
 */
```

### GET /api/jobs/{jobId}/applications

Lists all applications for a specific job.

**Request**

*   **Path Parameters**
    *   `jobId` (string): The UUID of the job listing.

**Response (200 OK)**

```json
{
  "applications": [
    {
      "id": "e5f6a7b8-c9d0-1234-5678-90abcdef1234",
      "jobListingId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
      "message": "I am very interested in this position."
    }
  ]
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} JobApplicationsResponse
 * @property {JobApplication[]} applications
 */
```

### GET /api/jobs/{jobId}/count

Counts the number of applications for a specific job.

**Request**

*   **Path Parameters**
    *   `jobId` (string): The UUID of the job listing.

**Response (200 OK)**

```json
{
  "count": 42
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} ApplicationsCount
 * @property {number} count
 */
```

## Company API

### POST /api/company

Creates a new company.

**Response (200 OK)**

The response is a string representing the newly created company's ID.

```
"f6a7b8c9-d0e1-2345-6789-0abcdef12345"
```

## User Profile API

### GET /api/profile/{userId}

Retrieves the user profile for a specific user.

**Request**

*   **Path Parameters**
    *   `userId` (string): The UUID of the user.

**Response (200 OK)**

```json
{
  "profile": {
    "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
    "fullName": "John Doe",
    "jobTitle": "Software Developer",
    "skills": ["JavaScript", "React", "Node.js"]
  }
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} UserProfile
 * @property {string} userId
 * @property {string} fullName
 * @property {string} jobTitle
 * @property {string[]} skills
 */

/**
 * @typedef {object} UserProfileResponse
 * @property {UserProfile} profile
 */
```

### POST /api/profile/{userId}

Creates or updates a user profile.

**Request**

*   **Path Parameters**
    *   `userId` (string): The UUID of the user.

*   **Request Body**

    ```json
    {
      "fullName": "John Doe",
      "jobTitle": "Senior Software Developer",
      "skills": ["JavaScript", "React", "Node.js", "TypeScript"]
    }
    ```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} UpdateProfile
 * @property {string} fullName
 * @property {string} jobTitle
 * @property {string[]} skills
 */
```

**Response (200 OK)**

```json
{
  "profile": {
    "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
    "fullName": "John Doe",
    "jobTitle": "Senior Software Developer",
    "skills": ["JavaScript", "React", "Node.js", "TypeScript"]
  }
}
```

### GET /api/profile/{userId}/cv

Retrieves a list of CVs for a specific user.

**Request**

*   **Path Parameters**
    *   `userId` (string): The UUID of the user.

**Response (200 OK)**

```json
{
  "cvs": [
    {
      "id": "d0e1f2a3-b4c5-6789-0123-456789abcdef",
      "userId": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
      "url": "https://example.com/cv.pdf",
      "createdAt": "2023-10-27T10:00:00Z"
    }
  ]
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} Cv
 * @property {string} id
 * @property {string} userId
 * @property {string} url
 * @property {string} createdAt
 */

/**
 * @typedef {object} GetCVsResponse
 * @property {Cv[]} cvs
 */
```

## Upload API

### POST /api/upload/cv

Uploads a CV file.

**Request**

*   **Form Data**
    *   `file` (File): The CV file to upload.

**Response (200 OK)**

```json
{
  "id": "d0e1f2a3-b4c5-6789-0123-456789abcdef",
  "url": "https://your-s3-bucket.s3.amazonaws.com/cvs/d0e1f2a3-b4c5-6789-0123-456789abcdef.pdf",
  "key": "cvs/d0e1f2a3-b4c5-6789-0123-456789abcdef.pdf"
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} UploadCvResponse
 * @property {string} id
 * @property {string} url
 * @property {string} key
 */
```
