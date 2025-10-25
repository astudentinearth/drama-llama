import 'dotenv/config';
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import pino from 'pino';
import pinoHttp from 'pino-http';
import rateLimit from 'express-rate-limit';
import { requireUser } from './auth.js';
import filesRouter from './routes/files.js';

const logger = pino({ level: process.env.NODE_ENV === 'production' ? 'info' : 'debug' });

export function buildApp() {
  const app = express();

  // Security headers
  app.use(helmet({
    crossOriginResourcePolicy: false // allow images from this host to be used cross-origin
  }));

  // Logging
  app.use(pinoHttp({ logger }));

  // CORS
  const allow = (process.env.CORS_ORIGINS || '').split(',').filter(Boolean);
  app.use(cors({
    origin: allow.length ? allow : true,
    credentials: false
  }));

  // JSON body (for control endpoints)
  app.use(express.json({ limit: '200kb' }));

  // Health
  app.get('/health', (_, res) => res.json({ ok: true }));

  // Rate-limit presign endpoints
  const limiter = rateLimit({
    windowMs: 60 * 1000,
    max: 120, // per minute
    standardHeaders: true,
    legacyHeaders: false
  });

  app.use('/files', requireUser, limiter, filesRouter);

  // Static **public** bucket passthrough (optional convenience)
  // e.g., http://localhost:4001/public-avatars/....  -> proxied from MinIO via your CDN later
  // For local dev, MinIO already serves these at http://localhost:9000/public-avatars/...
  // If you prefer to proxy, you can implement a tiny reverse proxy here.

  // Not found
  app.use((req, res) => res.status(404).json({ error: 'NotFound' }));

  // Error handler
  // (Keep minimal; upstream routes already try/catch and set status codes)
  return app;
}
