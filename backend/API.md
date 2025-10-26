# API Documentation

This document provides documentation for the backend API of the Groowy application.

## Authentication API

### POST /api/auth/register

Registers a new user account.

**Request Body**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "recruiter": false
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} RegisterRequest
 * @property {string} username
 * @property {string} email
 * @property {string} password
 * @property {boolean} recruiter
 */
```

**Response (200 OK)**

```json
{
  "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
  "username": "johndoe",
  "email": "john@example.com",
  "roles": ["MEMBER"]
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} User
 * @property {string} id
 * @property {string} username
 * @property {string} email
 * @property {string[]} roles
 */
```

### POST /api/auth/login

Authenticates a user and creates a session.

**Request Body**

```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (200 OK)**

Returns HTTP 200 on successful authentication. The session is managed via cookies.

### POST /api/auth/logout

Logs out the current user and destroys the session.

**Response (200 OK)**

Returns HTTP 200 on successful logout.

### GET /api/auth/me

Retrieves information about the currently authenticated user.

**Response (200 OK)**

```json
{
  "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
  "username": "johndoe",
  "email": "john@example.com",
  "roles": ["MEMBER"]
}
```

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

### GET /api/company/{id}

Retrieves a specific company by its ID.

**Request**

*   **Path Parameters**
    *   `id` (string): The UUID of the company.

**Response (200 OK)**

```json
{
  "id": "f6a7b8c9-d0e1-2345-6789-0abcdef12345",
  "name": "Tech Corp",
  "description": "A leading technology company"
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

### GET /api/company/{id}/jobs

Retrieves all job listings for a specific company.

**Request**

*   **Path Parameters**
    *   `id` (string): The UUID of the company.

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

### GET /api/company/my

Retrieves the current user's company. Requires RECRUITER role.

**Response (200 OK)**

```json
{
  "id": "f6a7b8c9-d0e1-2345-6789-0abcdef12345",
  "name": "My Company",
  "description": "My company description"
}
```

### PATCH /api/company/{id}

Updates an existing company. Requires RECRUITER role.

**Request**

*   **Path Parameters**
    *   `id` (string): The UUID of the company.

*   **Request Body**

    ```json
    {
      "name": "Updated Company Name",
      "description": "Updated company description"
    }
    ```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} UpdateCompany
 * @property {string} name
 * @property {string} description
 */
```

**Response (200 OK)**

```json
{
  "id": "f6a7b8c9-d0e1-2345-6789-0abcdef12345",
  "name": "Updated Company Name",
  "description": "Updated company description"
}
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

### POST /api/profile/{userId}/ai/sessions/{sessionId}/summarize-cv

Summarizes a CV for a specific user and session.

**Request**

*   **Path Parameters**
    *   `userId` (string): The UUID of the user.
    *   `sessionId` (string): The session ID.

*   **Request Body**

    ```json
    {
      "cvUrl": "https://example.com/cv.pdf"
    }
    ```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} SummarizeCvRequest
 * @property {string} cvUrl
 */
```

**Response (200 OK)**

Returns a summary of the CV content.

## Roadmap API

The Roadmap API provides endpoints for managing learning sessions, AI interactions, quizzes, and graduation projects. All endpoints proxy requests to the AI service.

### Session Management

### GET /api/roadmap/sessions

Retrieves all sessions for the current authenticated user.

**Response (200 OK)**

Returns a list of user sessions.

### GET /api/roadmap/sessions/{sessionId}

Retrieves a specific session by its ID.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns session details.

### GET /api/roadmap/sessions/user/{userId}

Retrieves all sessions for a specific user.

**Request**

*   **Path Parameters**
    *   `userId` (string): The UUID of the user.

**Response (200 OK)**

Returns a list of sessions for the specified user.

### GET /api/roadmap/sessions/{sessionId}/full

Retrieves complete session information including all details.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns full session details.

### GET /api/roadmap/sessions/{sessionId}/progress

Retrieves the progress information for a specific session.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns session progress data.

### GET /api/roadmap/sessions/user/{userId}/stats

Retrieves statistics for a specific user.

**Request**

*   **Path Parameters**
    *   `userId` (string): The UUID of the user.

**Response (200 OK)**

Returns user statistics.

### POST /api/roadmap/sessions

Creates a new learning session.

**Request Body**

```json
{
  "status": "active",
  "user_id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1"
}
```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} CreateSession
 * @property {string} status
 * @property {string} user_id
 */
```

**Response (200 OK)**

Returns the created session.

### POST /api/roadmap/sessions/complete

Marks a session as completed.

**Request**

*   **Query Parameters**
    *   `sessionId` (number): The session ID.

**Response (200 OK)**

Returns completion confirmation.

### POST /api/roadmap/sessions/archive

Archives a session.

**Request**

*   **Query Parameters**
    *   `sessionId` (number): The session ID.

**Response (200 OK)**

Returns archive confirmation.

### Message Management

### GET /api/roadmap/sessions/{sessionId}/messages

Retrieves all messages for a specific session.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns session messages.

### GET /api/roadmap/sessions/{sessionId}/messages/recent

Retrieves recent messages for a specific session.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns recent session messages.

### GET /api/roadmap/sessions/{sessionId}/messages/count

Retrieves the count of messages for a specific session.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns message count.

### AI Chat

### POST /api/roadmap/ai/sessions/{sessionId}/chat

Sends a chat message to the AI and receives a streaming response.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

*   **Request Body**

    ```json
    {
      "message": "Hello, I need help with learning JavaScript"
    }
    ```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} ChatMessage
 * @property {string} message
 */
```

**Response (200 OK)**

Returns a Server-Sent Events (SSE) stream with AI responses.

### Roadmap Management

### GET /api/roadmap/ai/sessions/{sessionId}/roadmap

Retrieves the roadmap for a specific session.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns session roadmap data.

### Quiz Management

### POST /api/roadmap/ai/sessions/{sessionId}/quizzes

Creates a new quiz for a session.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

*   **Request Body**

    ```json
    {
      "topic": "JavaScript Basics",
      "difficulty": "beginner"
    }
    ```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} CreateQuiz
 * @property {string} topic
 * @property {string} difficulty
 */
```

**Response (200 OK)**

Returns the created quiz.

### POST /api/roadmap/ai/sessions/{sessionId}/quizzes/{quizId}/attempts

Creates a quiz attempt for a specific quiz.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.
    *   `quizId` (number): The quiz ID.

*   **Request Body**

    ```json
    {
      "user_id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
      "quiz_id": 123
    }
    ```

**JavaScript Type Definitions**

```javascript
/**
 * @typedef {object} CreateQuizAttempt
 * @property {string} user_id
 * @property {number} quiz_id
 */
```

**Response (200 OK)**

Returns the quiz attempt.

### POST /api/roadmap/ai/sessions/{sessionId}/quiz-attempts/{attemptId}/submit

Submits a quiz attempt for grading.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.
    *   `attemptId` (number): The attempt ID.

**Response (200 OK)**

Returns quiz results.

### Graduation Project Management

### POST /api/roadmap/ai/graduation-project/{sessionId}/generate-questions

Generates questions for a graduation project.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns generated questions.

### GET /api/roadmap/ai/graduation-project/{sessionId}/questions

Retrieves questions for a graduation project.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns graduation project questions.

### GET /api/roadmap/ai/graduation-project/{sessionId}/submissions

Retrieves submissions for a graduation project.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns graduation project submissions.

### POST /api/roadmap/ai/graduation-project/{sessionId}/submit

Submits a graduation project.

**Request**

*   **Path Parameters**
    *   `sessionId` (string): The session ID.

**Response (200 OK)**

Returns submission confirmation.

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
