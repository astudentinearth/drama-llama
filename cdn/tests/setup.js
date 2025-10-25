import 'dotenv/config';

// Test environment setup
process.env.NODE_ENV = 'test';
process.env.S3_ENDPOINT = 'localhost';
process.env.S3_PORT = '9000';
process.env.S3_USE_SSL = 'false';
process.env.S3_ACCESS_KEY = 'miniodramallama';
process.env.S3_SECRET_KEY = 'miniodramallama59.';
process.env.S3_REGION = 'us-east-1';
process.env.BUCKET_PUBLIC = 'public-avatars';
process.env.BUCKET_PRIVATE = 'private-docs';
process.env.PUT_URL_EXP_SECS = '300';
process.env.GET_URL_EXP_SECS = '120';
process.env.MAX_AVATAR_BYTES = '5242880';
process.env.MAX_CV_BYTES = '10485760';
