import request from 'supertest';
import { buildApp } from '../src/app.js';
import { s3, BUCKETS } from '../src/s3.js';
import { genAvatarKey, genCVKey } from '../src/validators.js';

describe('File Upload/Download Tests', () => {
  let app;
  const testUserId = 'test-user-123';
  const authHeaders = { 'x-user-id': testUserId };

  beforeAll(async () => {
    app = buildApp();
    
    // Ensure test buckets exist
    try {
      await s3.bucketExists(BUCKETS.PUBLIC);
    } catch {
      await s3.makeBucket(BUCKETS.PUBLIC);
    }
    
    try {
      await s3.bucketExists(BUCKETS.PRIVATE);
    } catch {
      await s3.makeBucket(BUCKETS.PRIVATE);
    }
  });

  afterAll(async () => {
    // Clean up test files
    try {
      const publicObjects = await s3.listObjectsV2(BUCKETS.PUBLIC, `users/${testUserId}/`, true);
      for await (const obj of publicObjects) {
        await s3.removeObject(BUCKETS.PUBLIC, obj.name);
      }
    } catch (error) {
      console.warn('Failed to clean up public test files:', error.message);
    }

    try {
      const privateObjects = await s3.listObjectsV2(BUCKETS.PRIVATE, `users/${testUserId}/`, true);
      for await (const obj of privateObjects) {
        await s3.removeObject(BUCKETS.PRIVATE, obj.name);
      }
    } catch (error) {
      console.warn('Failed to clean up private test files:', error.message);
    }
  });

  describe('Public Avatar Upload', () => {
    test('should generate presigned URL for valid avatar upload', async () => {
      const response = await request(app)
        .post('/files/avatar/presign')
        .set(authHeaders)
        .send({ contentType: 'image/png' })
        .expect(200);

      expect(response.body).toHaveProperty('uploadUrl');
      expect(response.body).toHaveProperty('publicUrl');
      expect(response.body).toHaveProperty('key');
      expect(response.body.uploadUrl).toContain('X-Amz-Algorithm');
      expect(response.body.publicUrl).toContain('public-avatars');
      expect(response.body.key).toMatch(/^users\/test-user-123\/avatar-\w+\.png$/);
    });

    test('should generate presigned URL for JPEG avatar', async () => {
      const response = await request(app)
        .post('/files/avatar/presign')
        .set(authHeaders)
        .send({ contentType: 'image/jpeg' })
        .expect(200);

      expect(response.body.key).toMatch(/^users\/test-user-123\/avatar-[\w-]+\.jpg$/);
    });

    test('should generate presigned URL for WebP avatar', async () => {
      const response = await request(app)
        .post('/files/avatar/presign')
        .set(authHeaders)
        .send({ contentType: 'image/webp' })
        .expect(200);

      expect(response.body.key).toMatch(/^users\/test-user-123\/avatar-[\w-]+\.webp$/);
    });

    test('should reject invalid content type', async () => {
      const response = await request(app)
        .post('/files/avatar/presign')
        .set(authHeaders)
        .send({ contentType: 'application/pdf' })
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('contentType');
    });

    test('should reject missing content type', async () => {
      const response = await request(app)
        .post('/files/avatar/presign')
        .set(authHeaders)
        .send({})
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });

    test('should enforce file size limits', async () => {
      const response = await request(app)
        .post('/files/avatar/presign')
        .set(authHeaders)
        .set('x-file-size', '10485760') // 10MB, exceeds 5MB limit
        .send({ contentType: 'image/png' })
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('too large');
    });

    test('should require authentication', async () => {
      await request(app)
        .post('/files/avatar/presign')
        .send({ contentType: 'image/png' })
        .expect(401);
    });
  });

  describe('Private CV Upload', () => {
    test('should generate presigned URL for valid CV upload', async () => {
      const response = await request(app)
        .post('/files/cv/presign')
        .set(authHeaders)
        .send({ contentType: 'application/pdf' })
        .expect(200);

      expect(response.body).toHaveProperty('uploadUrl');
      expect(response.body).toHaveProperty('key');
      expect(response.body.uploadUrl).toContain('X-Amz-Algorithm');
      expect(response.body.key).toMatch(/^users\/test-user-123\/cv-\w+$/);
    });

    test('should generate presigned URL for Word document', async () => {
      const response = await request(app)
        .post('/files/cv/presign')
        .set(authHeaders)
        .send({ contentType: 'application/msword' })
        .expect(200);

      expect(response.body).toHaveProperty('uploadUrl');
      expect(response.body).toHaveProperty('key');
    });

    test('should generate presigned URL for DOCX document', async () => {
      const response = await request(app)
        .post('/files/cv/presign')
        .set(authHeaders)
        .send({ contentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
        .expect(200);

      expect(response.body).toHaveProperty('uploadUrl');
      expect(response.body).toHaveProperty('key');
    });

    test('should reject invalid content type', async () => {
      const response = await request(app)
        .post('/files/cv/presign')
        .set(authHeaders)
        .send({ contentType: 'image/png' })
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('contentType');
    });

    test('should enforce file size limits', async () => {
      const response = await request(app)
        .post('/files/cv/presign')
        .set(authHeaders)
        .set('x-file-size', '20971520') // 20MB, exceeds 10MB limit
        .send({ contentType: 'application/pdf' })
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('too large');
    });

    test('should require authentication', async () => {
      await request(app)
        .post('/files/cv/presign')
        .send({ contentType: 'application/pdf' })
        .expect(401);
    });
  });

  describe('Private CV Download', () => {
    let testKey;

    beforeEach(async () => {
      // Upload a test file first
      testKey = genCVKey(testUserId);
      const testContent = Buffer.from('Test CV content');
      
      await s3.putObject(BUCKETS.PRIVATE, testKey, testContent, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment'
      });
    });

    afterEach(async () => {
      if (testKey) {
        try {
          await s3.removeObject(BUCKETS.PRIVATE, testKey);
        } catch (error) {
          console.warn('Failed to clean up test file:', error.message);
        }
      }
    });

    test('should generate presigned download URL for existing file', async () => {
      const filename = testKey.split('/').pop();
      const response = await request(app)
        .get(`/files/cv/${filename}/presign`)
        .set(authHeaders)
        .expect(200);

      expect(response.body).toHaveProperty('url');
      expect(response.body).toHaveProperty('expiresIn');
      expect(response.body.url).toContain('X-Amz-Algorithm');
      expect(response.body.expiresIn).toBe(120);
    });

    test('should return 404 for non-existent file', async () => {
      const response = await request(app)
        .get('/files/cv/non-existent-file/presign')
        .set(authHeaders)
        .expect(404);

      expect(response.body).toHaveProperty('error', 'NotFound');
    });

    test('should prevent access to other users files', async () => {
      // Create a file for another user
      const otherUserKey = genCVKey('other-user-456');
      const testContent = Buffer.from('Other user CV content');
      
      await s3.putObject(BUCKETS.PRIVATE, otherUserKey, testContent, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment'
      });

      // Try to access the other user's file by using their filename
      // This should fail because the key construction will be wrong
      const otherUserFilename = otherUserKey.split('/').pop();
      
      const response = await request(app)
        .get(`/files/cv/${otherUserFilename}/presign`)
        .set(authHeaders)
        .expect(404); // This will be 404 because the file doesn't exist in the current user's namespace

      expect(response.body).toHaveProperty('error', 'NotFound');

      // Clean up
      try {
        await s3.removeObject(BUCKETS.PRIVATE, otherUserKey);
      } catch (error) {
        console.warn('Failed to clean up other user file:', error.message);
      }
    });

    test('should stream file download directly', async () => {
      const filename = testKey.split('/').pop();
      const response = await request(app)
        .get(`/files/cv/${filename}/download`)
        .set(authHeaders)
        .expect(200);

      expect(response.headers['content-type']).toBe('application/octet-stream');
      expect(response.headers['cache-control']).toBe('private, max-age=0, no-store');
      expect(response.headers['content-disposition']).toContain('attachment');
      expect(response.body.toString()).toBe('Test CV content');
    });

    test('should return 404 for non-existent file download', async () => {
      const response = await request(app)
        .get('/files/cv/non-existent-file/download')
        .set(authHeaders)
        .expect(404);
    });

    test('should require authentication for presign', async () => {
      const filename = testKey.split('/').pop();
      await request(app)
        .get(`/files/cv/${filename}/presign`)
        .expect(401);
    });

    test('should require authentication for download', async () => {
      const filename = testKey.split('/').pop();
      await request(app)
        .get(`/files/cv/${filename}/download`)
        .expect(401);
    });
  });

  describe('Integration Tests', () => {
    test('should complete full avatar upload flow', async () => {
      // Step 1: Get presigned URL
      const presignResponse = await request(app)
        .post('/files/avatar/presign')
        .set(authHeaders)
        .send({ contentType: 'image/png' })
        .expect(200);

      const { uploadUrl, publicUrl, key } = presignResponse.body;

      // Step 2: Upload file using presigned URL
      const testImageContent = Buffer.from('fake-png-content');
      const uploadResponse = await request(uploadUrl)
        .put('')
        .set('Content-Type', 'image/png')
        .send(testImageContent)
        .expect(200);

      // Step 3: Verify file exists in bucket
      const exists = await s3.statObject(BUCKETS.PUBLIC, key);
      expect(exists).toBeDefined();
      expect(exists.size).toBe(testImageContent.length);

      // Step 4: Verify public URL is accessible via MinIO directly
      const minioUrl = `http://localhost:9000/${BUCKETS.PUBLIC}/${encodeURIComponent(key)}`;
      const publicResponse = await request(minioUrl)
        .get('')
        .expect(200);

      expect(publicResponse.body).toEqual(testImageContent);
    });

    test('should complete full CV upload and download flow', async () => {
      // Step 1: Get presigned URL for upload
      const presignResponse = await request(app)
        .post('/files/cv/presign')
        .set(authHeaders)
        .send({ contentType: 'application/pdf' })
        .expect(200);

      const { uploadUrl, key } = presignResponse.body;

      // Step 2: Upload file using presigned URL
      const testPdfContent = Buffer.from('fake-pdf-content');
      await request(uploadUrl)
        .put('')
        .set('Content-Type', 'application/pdf')
        .send(testPdfContent)
        .expect(200);

      // Step 3: Verify file exists in private bucket
      const exists = await s3.statObject(BUCKETS.PRIVATE, key);
      expect(exists).toBeDefined();
      expect(exists.size).toBe(testPdfContent.length);

      // Step 4: Get presigned download URL
      const filename = key.split('/').pop();
      const downloadPresignResponse = await request(app)
        .get(`/files/cv/${filename}/presign`)
        .set(authHeaders)
        .expect(200);

      const { url: downloadUrl } = downloadPresignResponse.body;

      // Step 5: Download file using presigned URL
      const downloadResponse = await request(downloadUrl)
        .get('')
        .expect(200);

      expect(downloadResponse.body).toEqual(testPdfContent);

      // Step 6: Test direct download endpoint
      const directDownloadResponse = await request(app)
        .get(`/files/cv/${filename}/download`)
        .set(authHeaders)
        .expect(200);

      expect(directDownloadResponse.body).toEqual(testPdfContent);
    });

    test('should handle multiple users with separate namespaces', async () => {
      const user1Id = 'user-1';
      const user2Id = 'user-2';
      const user1Headers = { 'x-user-id': user1Id };
      const user2Headers = { 'x-user-id': user2Id };

      // User 1 uploads avatar
      const user1Presign = await request(app)
        .post('/files/avatar/presign')
        .set(user1Headers)
        .send({ contentType: 'image/png' })
        .expect(200);

      const user1Key = user1Presign.body.key;
      expect(user1Key).toMatch(/^users\/user-1\//);

      // User 2 uploads avatar
      const user2Presign = await request(app)
        .post('/files/avatar/presign')
        .set(user2Headers)
        .send({ contentType: 'image/png' })
        .expect(200);

      const user2Key = user2Presign.body.key;
      expect(user2Key).toMatch(/^users\/user-2\//);

      // Verify keys are different
      expect(user1Key).not.toBe(user2Key);

      // Create a CV file for user 2
      const user2CVKey = genCVKey('user-2');
      const user2CVContent = Buffer.from('User 2 CV content');
      
      await s3.putObject(BUCKETS.PRIVATE, user2CVKey, user2CVContent, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment'
      });

      // User 1 should not be able to access user 2's files
      const user2Filename = user2CVKey.split('/').pop();
      await request(app)
        .get(`/files/cv/${user2Filename}/presign`)
        .set(user1Headers)
        .expect(404); // This will be 404 because the file doesn't exist in user 1's namespace

      // Clean up user 2's CV file
      try {
        await s3.removeObject(BUCKETS.PRIVATE, user2CVKey);
      } catch (error) {
        console.warn('Failed to clean up user 2 CV file:', error.message);
      }
    });
  });
});
