# CDN Service - Backend Developer Guide

A Node.js-based CDN service for handling file uploads and downloads with MinIO/S3-compatible storage. This service provides presigned URLs for secure file operations and supports both public and private file access patterns.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   CDN Service   │    │   MinIO/S3      │
│   Application   │◄──►│   (This App)    │◄──►│   Storage       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Public Files  │
                       │   (Avatars)     │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Private Files  │
                       │   (CVs, Docs)   │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- Docker & Docker Compose
- MinIO (included in docker-compose)

### Installation

```bash
# Clone and install dependencies
git clone <repository-url>
cd cdn
npm install

# Start MinIO
docker-compose -f docker-compose.minio.yml up -d

# Create required buckets (one-time setup)
mc alias set local http://localhost:9000 $S3_ACCESS_KEY $S3_SECRET_KEY
mc mb local/public-avatars
mc mb local/private-docs
mc anonymous set download local/public-avatars

# Start the service
npm run dev
```

The service will be available at `http://localhost:4001`

## 📁 Project Structure

```
cdn/
├── src/
│   ├── app.js              # Express app configuration
│   ├── auth.js             # Authentication middleware
│   ├── routes/
│   │   └── files.js        # File upload/download routes
│   ├── s3.js               # MinIO/S3 client configuration
│   ├── server.js           # Server entry point
│   └── validators.js       # Input validation schemas
├── tests/
│   ├── files.test.js       # Comprehensive test suite
│   ├── setup.js            # Test environment setup
│   └── README.md           # Test documentation
├── docker-compose.minio.yml # MinIO container configuration
├── jest.config.cjs         # Jest test configuration
└── package.json
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Express Server
PORT=4001
NODE_ENV=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Authentication (for demo purposes)
DEV_AUTH_SECRET=dramallama

# MinIO/S3 Configuration
S3_ENDPOINT=localhost
S3_PORT=9000
S3_USE_SSL=false
S3_ACCESS_KEY=miniodramallama
S3_SECRET_KEY=miniodramallama59.
S3_REGION=us-east-1

# Bucket Names
BUCKET_PUBLIC=public-avatars
BUCKET_PRIVATE=private-docs

# File Size Limits
MAX_AVATAR_BYTES=5242880            # 5 MB
MAX_CV_BYTES=10485760               # 10 MB

# Presigned URL Expiration
PUT_URL_EXP_SECS=300                # 5 minutes
GET_URL_EXP_SECS=120                # 2 minutes
```

## 🔌 API Endpoints

### Authentication

All endpoints require authentication via the `x-user-id` header:

```http
x-user-id: your-user-id-here
```

### Public File Operations (Avatars)

#### Generate Upload URL
```http
POST /files/avatar/presign
Content-Type: application/json
x-user-id: user123

{
  "contentType": "image/png"
}
```

**Response:**
```json
{
  "uploadUrl": "https://localhost:9000/public-avatars/users/user123/avatar-abc123.png?...",
  "publicUrl": "http://localhost:4001/public-avatars/users/user123/avatar-abc123.png",
  "key": "users/user123/avatar-abc123.png"
}
```

**Supported Content Types:**
- `image/png`
- `image/jpeg` 
- `image/webp`

### Private File Operations (CVs/Documents)

#### Generate Upload URL
```http
POST /files/cv/presign
Content-Type: application/json
x-user-id: user123

{
  "contentType": "application/pdf"
}
```

**Response:**
```json
{
  "uploadUrl": "https://localhost:9000/private-docs/users/user123/cv-xyz789?...",
  "key": "users/user123/cv-xyz789"
}
```

**Supported Content Types:**
- `application/pdf`
- `application/msword`
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

#### Generate Download URL
```http
GET /files/cv/{filename}/presign
x-user-id: user123
```

**Response:**
```json
{
  "url": "https://localhost:9000/private-docs/users/user123/cv-xyz789?...",
  "expiresIn": 120
}
```

#### Direct Download
```http
GET /files/cv/{filename}/download
x-user-id: user123
```

**Response:** File stream with appropriate headers

## 🔒 Security Features

### User Namespace Isolation
- All files are stored under `users/{userId}/` paths
- Users can only access their own files
- Cross-user access attempts return 404

### File Size Validation
- Avatars: 5MB limit
- CVs: 10MB limit
- Validation via `x-file-size` header

### Content Type Validation
- Strict whitelist of allowed MIME types
- Rejects invalid content types with 400 status

### Rate Limiting
- 120 requests per minute per user
- Applied to all `/files/*` endpoints

## 🧪 Testing

### Run Tests
```bash
# Run all tests (starts MinIO automatically)
./run-tests.sh

# Or run manually
npm test

# With coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### Test Coverage
- **23 comprehensive tests** covering all functionality
- **Real MinIO integration** (not mocked)
- **Security testing** (user isolation, access control)
- **Error handling** (validation, file size limits)
- **End-to-end workflows** (upload → download flows)

## 🔄 File Upload Flow

### 1. Public Avatar Upload
```javascript
// 1. Get presigned URL
const response = await fetch('/files/avatar/presign', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-user-id': 'user123'
  },
  body: JSON.stringify({ contentType: 'image/png' })
});

const { uploadUrl, publicUrl } = await response.json();

// 2. Upload file directly to MinIO
const uploadResponse = await fetch(uploadUrl, {
  method: 'PUT',
  body: fileBlob,
  headers: { 'Content-Type': 'image/png' }
});

// 3. Use publicUrl for display
console.log('Avatar URL:', publicUrl);
```

### 2. Private CV Upload
```javascript
// 1. Get presigned URL
const response = await fetch('/files/cv/presign', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-user-id': 'user123'
  },
  body: JSON.stringify({ contentType: 'application/pdf' })
});

const { uploadUrl, key } = await response.json();

// 2. Upload file directly to MinIO
await fetch(uploadUrl, {
  method: 'PUT',
  body: fileBlob,
  headers: { 'Content-Type': 'application/pdf' }
});

// 3. Store key for later download
localStorage.setItem('cvKey', key);
```

### 3. Private CV Download
```javascript
// Option 1: Get presigned download URL
const response = await fetch(`/files/cv/${filename}/presign`, {
  headers: { 'x-user-id': 'user123' }
});

const { url } = await response.json();
window.open(url); // Opens download

// Option 2: Direct download
const response = await fetch(`/files/cv/${filename}/download`, {
  headers: { 'x-user-id': 'user123' }
});

const blob = await response.blob();
const downloadUrl = URL.createObjectURL(blob);
// Trigger download...
```

## 🛠️ Development

### Adding New File Types

1. **Update validators.js:**
```javascript
const NEW_FILE_TYPES = ['application/zip', 'text/plain'];

export const schemaNewFile = Joi.object({
  contentType: Joi.string().valid(...NEW_FILE_TYPES).required()
});
```

2. **Add route in files.js:**
```javascript
r.post('/newfile/presign', async (req, res) => {
  const { value, error } = schemaNewFile.validate(req.body || {});
  if (error) return res.status(400).json({ error: error.message });
  
  // Implementation...
});
```

3. **Add tests in files.test.js:**
```javascript
describe('New File Type', () => {
  test('should handle new file type', async () => {
    // Test implementation...
  });
});
```

### Error Handling

The service uses consistent error responses:

```json
{
  "error": "Error message",
  "detail": "Additional details (optional)"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (missing x-user-id)
- `403` - Forbidden (access denied)
- `404` - Not Found (file doesn't exist)
- `500` - Internal Server Error

### Logging

The service uses structured logging with Pino:

```javascript
// Request/response logging is automatic
// Custom logging:
logger.info({ userId, action: 'file_upload' }, 'File uploaded successfully');
logger.error({ error, userId }, 'Upload failed');
```

## 🚀 Production Deployment

### Environment Setup
1. Set `NODE_ENV=production`
2. Configure proper CORS origins
3. Use production MinIO/S3 credentials
4. Set up proper authentication (replace header-based auth)

### MinIO Configuration
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${S3_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${S3_SECRET_KEY}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    restart: unless-stopped

volumes:
  minio_data:
```

### Health Checks
```http
GET /health
```

**Response:**
```json
{
  "ok": true
}
```

## 📊 Monitoring

### Key Metrics to Monitor
- Upload/download success rates
- File size distributions
- Error rates by endpoint
- Storage usage per user
- Rate limiting hits

### Log Analysis
```bash
# Count uploads by user
grep "file_upload" logs/app.log | jq '.userId' | sort | uniq -c

# Error rate analysis
grep "ERROR" logs/app.log | jq '.req.url' | sort | uniq -c
```

## 🔧 Troubleshooting

### Common Issues

**1. MinIO Connection Failed**
```bash
# Check MinIO status
docker-compose -f docker-compose.minio.yml ps

# Check MinIO logs
docker-compose -f docker-compose.minio.yml logs minio
```

**2. Authentication Errors**
- Ensure `x-user-id` header is present
- Check CORS configuration for preflight requests

**3. File Upload Failures**
- Verify file size limits
- Check content type validation
- Ensure presigned URL hasn't expired

**4. Download Issues**
- Verify file exists in correct user namespace
- Check MinIO bucket permissions
- Ensure presigned URL is valid

### Debug Mode
```bash
# Enable debug logging
NODE_ENV=development npm run dev

# Check MinIO console
open http://localhost:9001
```

## 📚 Additional Resources

- [MinIO Documentation](https://docs.min.io/)
- [Express.js Guide](https://expressjs.com/)
- [Jest Testing Framework](https://jestjs.io/)
- [Pino Logger](https://getpino.io/)

## 🤝 Contributing

1. Write tests for new features
2. Follow existing code style
3. Update documentation
4. Run full test suite before submitting

```bash
# Pre-commit checks
npm test
npm run lint  # if configured
```

---

**Need Help?** Check the test files for usage examples or create an issue in the repository.