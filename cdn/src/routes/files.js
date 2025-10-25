import { Router } from 'express';
import { EXPIRES, BUCKETS, presignPut, presignGet, s3, objectExists } from '../s3.js';
import { schemaAvatar, schemaCV, genAvatarKey, genCVKey, enforceSizeLimits, ensureOwnerPathOrThrow } from '../validators.js';

const {
  MAX_AVATAR_BYTES = '5242880',
  MAX_CV_BYTES = '10485760'
} = process.env;

const r = Router();

/**
 * POST /files/avatar/presign
 * Body: { contentType }
 * Auth: user required
 * Returns: { uploadUrl, publicUrl, key }
 */
r.post('/avatar/presign', async (req, res) => {
  const { value, error } = schemaAvatar.validate(req.body || {});
  if (error) return res.status(400).json({ error: error.message });

  try {
    // Optional: enforce planned size via client header `x-file-size`
    const claimedSize = Number(req.header('x-file-size') || '0');
    try {
      enforceSizeLimits(claimedSize, Number(MAX_AVATAR_BYTES));
    } catch (sizeError) {
      return res.status(400).json({ error: sizeError.message });
    }

    const key = genAvatarKey(req.user.id, value.contentType);

    const uploadUrl = await presignPut(BUCKETS.PUBLIC, key, EXPIRES.PUT, {
      'Content-Type': value.contentType,
      'Cache-Control': 'public, max-age=31536000, immutable'
    });

    // Direct public read URL (MinIO path-style)
    const publicUrl = `${req.protocol}://${req.get('host')}/${BUCKETS.PUBLIC}/${encodeURIComponent(key)}`;

    res.json({ uploadUrl, publicUrl, key });
  } catch (e) {
    res.status(500).json({ error: 'PresignFailed', detail: e.message });
  }
});

/**
 * POST /files/cv/presign
 * Body: { contentType }
 * Returns: { uploadUrl, key }
 */
r.post('/cv/presign', async (req, res) => {
  const { value, error } = schemaCV.validate(req.body || {});
  if (error) return res.status(400).json({ error: error.message });

  try {
    const claimedSize = Number(req.header('x-file-size') || '0');
    try {
      enforceSizeLimits(claimedSize, Number(MAX_CV_BYTES));
    } catch (sizeError) {
      return res.status(400).json({ error: sizeError.message });
    }

    const key = genCVKey(req.user.id);

    const uploadUrl = await presignPut(BUCKETS.PRIVATE, key, EXPIRES.PUT, {
      'Content-Type': value.contentType,
      'Cache-Control': 'private, max-age=0, no-store',
      'Content-Disposition': 'attachment'
    });

    res.json({ uploadUrl, key });
  } catch (e) {
    res.status(500).json({ error: 'PresignFailed', detail: e.message });
  }
});

/**
 * GET /files/cv/:key/presign
 * Returns short-lived GET url for the owner
 */
r.get('/cv/:key/presign', async (req, res) => {
  try {
    const key = `users/${req.user.id}/${req.params.key}`;
    ensureOwnerPathOrThrow(req.user.id, key);

    const exists = await objectExists(BUCKETS.PRIVATE, key);
    if (!exists) return res.status(404).json({ error: 'NotFound' });

    const url = await presignGet(BUCKETS.PRIVATE, key, EXPIRES.GET, {
      'response-content-disposition': 'attachment'
    });

    res.json({ url, expiresIn: EXPIRES.GET });
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message || 'PresignFailed' });
  }
});

/**
 * GET /files/cv/:key/download
 * Server-side streaming (alternative to presign)
 */
r.get('/cv/:key/download', async (req, res) => {
  try {
    const key = `users/${req.user.id}/${req.params.key}`;
    ensureOwnerPathOrThrow(req.user.id, key);

    // Check if object exists first
    const exists = await objectExists(BUCKETS.PRIVATE, key);
    if (!exists) return res.status(404).json({ error: 'NotFound' });

    // Stream via MinIO
    const stream = await s3.getObject(BUCKETS.PRIVATE, key);

    // (Optional) set headers from metadata if you stored them elsewhere
    res.setHeader('Content-Type', 'application/octet-stream');
    res.setHeader('Cache-Control', 'private, max-age=0, no-store');
    res.setHeader('Content-Disposition', `attachment; filename="cv-${req.user.id}"`);

    stream.on('error', (err) => {
      if (err?.code === 'NoSuchKey') return res.status(404).end();
      res.status(500).end();
    });

    stream.pipe(res);
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message || 'DownloadFailed' });
  }
});

export default r;
