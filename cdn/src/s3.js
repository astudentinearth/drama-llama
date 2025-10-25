import 'dotenv/config';
import { Client } from 'minio';

const {
  S3_ENDPOINT = 'localhost',
  S3_PORT = '9000',
  S3_USE_SSL = 'false',
  S3_ACCESS_KEY,
  S3_SECRET_KEY,
  S3_REGION = 'us-east-1',
  BUCKET_PUBLIC = 'public-avatars',
  BUCKET_PRIVATE = 'private-docs',
  PUT_URL_EXP_SECS = '300',
  GET_URL_EXP_SECS = '120'
} = process.env;

export const BUCKETS = {
  PUBLIC: BUCKET_PUBLIC,
  PRIVATE: BUCKET_PRIVATE
};

export const s3 = new Client({
  endPoint: S3_ENDPOINT,
  port: Number(S3_PORT),
  useSSL: String(S3_USE_SSL) === 'true',
  accessKey: S3_ACCESS_KEY,
  secretKey: S3_SECRET_KEY,
  region: S3_REGION
});

// Presign helpers
export function presignPut(bucket, objectName, seconds, headers = {}) {
  return s3.presignedPutObject(bucket, objectName, seconds, headers);
}

export function presignGet(bucket, objectName, seconds, respHeaders = {}) {
  // minio-js uses query params like response-content-disposition under S3 rules
  return s3.presignedGetObject(bucket, objectName, seconds, respHeaders);
}

// Simple existence check
export async function objectExists(bucket, objectName) {
  try {
    await s3.statObject(bucket, objectName);
    return true;
  } catch (e) {
    if (e?.code === 'NotFound') return false;
    throw e;
  }
}

export const EXPIRES = {
  PUT: Number(PUT_URL_EXP_SECS),
  GET: Number(GET_URL_EXP_SECS)
};
