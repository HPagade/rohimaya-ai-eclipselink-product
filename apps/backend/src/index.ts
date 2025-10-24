import express, { Application, Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Import routes
import authRoutes from './routes/auth.routes';
import handoffRoutes from './routes/handoff.routes';
import voiceRoutes from './routes/voice.routes';
import patientRoutes from './routes/patient.routes';
import sbarRoutes from './routes/sbar.routes';

// Import middleware
import { errorHandler, notFoundHandler } from './middleware/error.middleware';
import { generalRateLimit } from './middleware/rate-limit.middleware';

// Import workers
import transcriptionWorker from './workers/transcription.worker';
import sbarGenerationWorker from './workers/sbar-generation.worker';

/**
 * EclipseLink AI Backend Server
 * Express.js + TypeScript
 * Based on Part 2 & Part 4 specifications
 */

const app: Application = express();
const PORT = process.env.PORT || 4000;

/**
 * Middleware Stack
 */

// Security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:']
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true
  }
}));

// CORS configuration
const corsOptions = {
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Authorization', 'Content-Type', 'X-Request-ID']
};
app.use(cors(corsOptions));

// Request logging
if (process.env.NODE_ENV !== 'production') {
  app.use(morgan('dev'));
} else {
  app.use(morgan('combined'));
}

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Request ID middleware
app.use((req: Request, res: Response, next) => {
  const requestId = req.headers['x-request-id'] as string ||
    `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  req.headers['x-request-id'] = requestId;
  res.setHeader('X-Request-ID', requestId);
  next();
});

// Response time middleware
app.use((req: Request, res: Response, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    res.setHeader('X-Response-Time', `${duration}ms`);
  });
  next();
});

// General rate limiting
app.use(generalRateLimit);

/**
 * Routes
 */

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    success: true,
    data: {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      environment: process.env.NODE_ENV || 'development',
      version: process.env.npm_package_version || '1.0.0'
    }
  });
});

// API version info
app.get('/v1', (req: Request, res: Response) => {
  res.status(200).json({
    success: true,
    data: {
      version: 'v1',
      name: 'EclipseLink AI API',
      description: 'Clinical Handoff System API',
      documentation: 'https://docs.eclipselink.ai/api',
      endpoints: {
        auth: '/v1/auth',
        handoffs: '/v1/handoffs (TODO)',
        patients: '/v1/patients (TODO)',
        voice: '/v1/voice (TODO)',
        sbar: '/v1/sbar (TODO)',
        ehr: '/v1/ehr (TODO)',
        analytics: '/v1/analytics (TODO)'
      }
    },
    meta: {
      requestId: req.headers['x-request-id'],
      timestamp: new Date().toISOString()
    }
  });
});

// Mount routes
app.use('/v1/auth', authRoutes);
app.use('/v1/handoffs', handoffRoutes);
app.use('/v1/voice', voiceRoutes);
app.use('/v1/patients', patientRoutes);
app.use('/v1/sbar', sbarRoutes);

// TODO: Add remaining route modules
// app.use('/v1/ehr', ehrRoutes);
// app.use('/v1/analytics', analyticsRoutes);

/**
 * Error Handling
 */

// 404 handler
app.use(notFoundHandler);

// Global error handler
app.use(errorHandler);

/**
 * Server Start
 */
function startServer() {
  app.listen(PORT, () => {
    console.log('╔═══════════════════════════════════════════════════════╗');
    console.log('║                                                       ║');
    console.log('║           EclipseLink AI Backend Server              ║');
    console.log('║                                                       ║');
    console.log('╚═══════════════════════════════════════════════════════╝');
    console.log('');
    console.log(`✓ Environment:  ${process.env.NODE_ENV || 'development'}`);
    console.log(`✓ Port:         ${PORT}`);
    console.log(`✓ API Version:  v1`);
    console.log(`✓ Health:       http://localhost:${PORT}/health`);
    console.log(`✓ API Docs:     http://localhost:${PORT}/v1`);
    console.log('');
    console.log('Available Endpoints:');
    console.log('');
    console.log('  Auth:');
    console.log(`    POST   /v1/auth/register`);
    console.log(`    POST   /v1/auth/login`);
    console.log(`    POST   /v1/auth/refresh`);
    console.log(`    POST   /v1/auth/logout`);
    console.log(`    GET    /v1/auth/me`);
    console.log('');
    console.log('  Handoffs:');
    console.log(`    POST   /v1/handoffs`);
    console.log(`    GET    /v1/handoffs`);
    console.log(`    GET    /v1/handoffs/:id`);
    console.log(`    PUT    /v1/handoffs/:id`);
    console.log(`    POST   /v1/handoffs/:id/assign`);
    console.log(`    POST   /v1/handoffs/:id/complete`);
    console.log(`    DELETE /v1/handoffs/:id`);
    console.log('');
    console.log('  Voice Recordings:');
    console.log(`    POST   /v1/voice/upload`);
    console.log(`    GET    /v1/voice/:id`);
    console.log(`    GET    /v1/voice/:id/download`);
    console.log(`    GET    /v1/voice/:id/status`);
    console.log(`    DELETE /v1/voice/:id`);
    console.log('');
    console.log('  Patients:');
    console.log(`    GET    /v1/patients`);
    console.log(`    GET    /v1/patients/:id`);
    console.log(`    GET    /v1/patients/:id/handoffs`);
    console.log('');
    console.log('  SBAR Reports:');
    console.log(`    GET    /v1/sbar/:handoffId`);
    console.log(`    GET    /v1/sbar/:handoffId/versions`);
    console.log(`    GET    /v1/sbar/:id/compare`);
    console.log(`    PUT    /v1/sbar/:id`);
    console.log(`    POST   /v1/sbar/:id/export`);
    console.log('');
    console.log('Background Workers:');
    console.log(`    ✓ Transcription Worker (concurrency: 5)`);
    console.log(`    ✓ SBAR Generation Worker (concurrency: 3)`);
    console.log('');
    console.log('TODO: Implement EHR and analytics endpoints');
    console.log('');
  });
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM signal received: closing HTTP server and workers');
  await transcriptionWorker.close();
  await sbarGenerationWorker.close();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('SIGINT signal received: closing HTTP server and workers');
  await transcriptionWorker.close();
  await sbarGenerationWorker.close();
  process.exit(0);
});

// Start server
if (require.main === module) {
  startServer();
}

export default app;
