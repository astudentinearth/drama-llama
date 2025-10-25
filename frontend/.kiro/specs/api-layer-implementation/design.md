# API Layer Implementation Design

## Overview

This design implements a comprehensive API layer for the Drama Llama application, providing TypeScript interfaces and functions for Jobs, Company, User Profile, and Upload endpoints. The implementation follows the established patterns from the existing auth API, ensuring consistency and maintainability across the codebase.

## Architecture

The API layer follows a feature-based modular architecture:

```
src/features/
├── jobs/
│   ├── jobs.api.ts          # Jobs and applications API functions
│   └── jobs.types.ts        # Job-related TypeScript interfaces
├── company/
│   └── company.api.ts       # Company API functions
├── profile/
│   ├── profile.api.ts       # User profile API functions
│   └── profile.types.ts     # Profile-related TypeScript interfaces
└── upload/
    ├── upload.api.ts        # File upload API functions
    └── upload.types.ts      # Upload-related TypeScript interfaces
```

Each module follows the same pattern:
- **API functions**: Handle HTTP requests using axios
- **Type definitions**: Define request/response interfaces
- **Error handling**: Use consistent error patterns with descriptive messages
- **Response validation**: Use the existing `success()` utility function

## Components and Interfaces

### Jobs API Module

**Core Types:**
```typescript
interface JobListing {
  id: string;
  title: string;
  content: string;
  tags: string[];
  userId: string;
  active: boolean;
}

interface CreateJobListing {
  title: string;
  content: string;
  tags: string[];
  active: boolean;
}

interface JobApplication {
  id: string;
  jobListingId: string;
  userId: string;
  message: string;
}
```

**API Functions:**
- `getJobs()`: Fetch all job listings
- `getJobById(id: string)`: Fetch specific job
- `createJob(data: CreateJobListing)`: Create new job
- `updateJob(id: string, data: Partial<CreateJobListing>)`: Update existing job
- `createJobApplication(jobId: string, data: CreateJobApplication)`: Apply to job
- `getJobApplications(jobId: string)`: Get job applications
- `getApplicationsCount(jobId: string)`: Get application count

### Profile API Module

**Core Types:**
```typescript
interface UserProfile {
  userId: string;
  fullName: string;
  jobTitle: string;
  skills: string[];
}

interface UpdateProfile {
  fullName: string;
  jobTitle: string;
  skills: string[];
}

interface Cv {
  id: string;
  userId: string;
  url: string;
  createdAt: string;
}
```

**API Functions:**
- `getUserProfile(userId: string)`: Get user profile
- `updateUserProfile(userId: string, data: UpdateProfile)`: Update profile
- `getUserCVs(userId: string)`: Get user CVs

### Company API Module

**API Functions:**
- `createCompany()`: Create new company (returns string ID)

### Upload API Module

**Core Types:**
```typescript
interface UploadCvResponse {
  id: string;
  url: string;
  key: string;
}
```

**API Functions:**
- `uploadCV(file: File)`: Upload CV file using FormData

## Data Models

All data models are derived from the provided API documentation and follow TypeScript best practices:

1. **Immutable Interfaces**: All interfaces are readonly where appropriate
2. **Optional Properties**: Use optional properties for partial updates
3. **Union Types**: Use union types for status fields where applicable
4. **Generic Types**: Use generics for response wrappers where beneficial

## Error Handling

The error handling strategy follows the existing auth API pattern:

1. **Response Validation**: Use `success(response)` to validate HTTP status codes
2. **Descriptive Errors**: Throw errors with meaningful messages that indicate the operation that failed
3. **Consistent Pattern**: All API functions follow the same error handling approach:
   ```typescript
   if (success(response)) {
     return response.data as ExpectedType;
   } else {
     throw new Error("Operation description failed");
   }
   ```

## Testing Strategy

The testing approach focuses on:

1. **Type Safety**: Ensure all interfaces match API documentation
2. **Function Signatures**: Verify all functions have correct parameter types
3. **Error Handling**: Test error scenarios and message consistency
4. **Integration**: Test with existing auth patterns and utilities
5. **Mock Responses**: Use mock data that matches API documentation examples

### Test Categories:

1. **Unit Tests**: Test individual API functions with mocked axios responses
2. **Type Tests**: Verify TypeScript interfaces compile correctly
3. **Integration Tests**: Test API functions work with existing utilities
4. **Error Tests**: Verify error handling and message consistency

The testing implementation will be minimal and focused on core functionality, following the project's testing patterns established in the auth module.