import Joi from 'joi';
import { nanoid } from 'nanoid';

const AVATAR_TYPES = ['image/png', 'image/jpeg', 'image/webp'];
const CV_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
];

export const schemaAvatar = Joi.object({
  contentType: Joi.string().valid(...AVATAR_TYPES).required()
});

export const schemaCV = Joi.object({
  contentType: Joi.string().valid(...CV_TYPES).required()
});

export function genAvatarKey(userId, contentType) {
  const ext = contentType === 'image/png'
    ? 'png'
    : contentType.includes('jpeg') ? 'jpg'
    : 'webp';
  return `users/${userId}/avatar-${nanoid(10)}.${ext}`;
}

export function genCVKey(userId) {
  return `users/${userId}/cv-${nanoid(12)}`;
}

export function enforceSizeLimits(contentLength, maxBytes) {
  if (typeof contentLength === 'number' && contentLength > 0 && contentLength > maxBytes) {
    const mb = (maxBytes / (1024 * 1024)).toFixed(1);
    throw new Error(`File too large. Max ${mb} MB`);
  }
}

export function ensureOwnerPathOrThrow(userId, key) {
  const prefix = `users/${userId}/`;
  if (!key || !key.startsWith(prefix)) {
    const err = new Error('Forbidden: key outside user namespace');
    err.status = 403;
    throw err;
  }
}
