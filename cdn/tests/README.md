# File Upload/Download Tests

This directory contains comprehensive tests for the file upload and download functionality, covering both public and private file operations.

## Test Structure

### `files.test.js`
Main test file containing:

- **Public Avatar Upload Tests**: Tests for presigned URL generation for avatar uploads (PNG, JPEG, WebP)
- **Private CV Upload Tests**: Tests for presigned URL generation for CV uploads (PDF, DOC, DOCX)
- **Private CV Download Tests**: Tests for both presigned download URLs and direct streaming
- **Integration Tests**: End-to-end tests covering complete upload/download flows
- **Security Tests**: Tests for user isolation and access control

## Test Features

### Public File Operations
- ✅ Avatar upload with presigned URLs
- ✅ Multiple image format support (PNG, JPEG, WebP)
- ✅ File size validation (5MB limit)
- ✅ Content type validation
- ✅ Public URL generation
- ✅ Authentication requirements

### Private File Operations
- ✅ CV upload with presigned URLs
- ✅ Multiple document format support (PDF, DOC, DOCX)
- ✅ File size validation (10MB limit)
- ✅ Presigned download URLs
- ✅ Direct file streaming
- ✅ User namespace isolation
- ✅ Access control validation

### Security Features
- ✅ User authentication requirements
- ✅ User namespace isolation
- ✅ File ownership validation
- ✅ Cross-user access prevention

## Running Tests

### Prerequisites
1. Install dependencies:
   ```bash
   npm install
   ```

2. Start MinIO server (using Docker Compose):
   ```bash
   docker-compose -f docker-compose.minio.yml up -d
   ```

3. Wait for MinIO to be ready (usually takes 10-15 seconds)

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Test Environment

The tests use the following configuration:
- **MinIO Endpoint**: localhost:9000
- **Access Key**: minioadmin
- **Secret Key**: minioadmin
- **Public Bucket**: public-avatars
- **Private Bucket**: private-docs
- **Max Avatar Size**: 5MB
- **Max CV Size**: 10MB

## Test Data Cleanup

Tests automatically clean up after themselves:
- Uploaded test files are removed after each test
- Buckets are cleaned up after test completion
- No persistent test data remains

## Test Coverage

The tests cover:
- ✅ All API endpoints
- ✅ Success and error scenarios
- ✅ Input validation
- ✅ File size limits
- ✅ Content type validation
- ✅ Authentication and authorization
- ✅ User isolation
- ✅ End-to-end workflows
- ✅ Error handling

## Troubleshooting

### MinIO Connection Issues
- Ensure MinIO is running: `docker-compose -f docker-compose.minio.yml ps`
- Check MinIO logs: `docker-compose -f docker-compose.minio.yml logs minio`
- Verify MinIO is accessible at http://localhost:9000

### Test Failures
- Check that all environment variables are set correctly
- Ensure MinIO buckets exist and are accessible
- Verify network connectivity to MinIO
- Check for any port conflicts

### Cleanup Issues
- If tests fail to clean up, manually remove test files from MinIO
- Restart MinIO if bucket operations fail
- Check MinIO logs for any error messages
