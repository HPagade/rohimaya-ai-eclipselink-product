import { Request, Response, NextFunction } from 'express';
import { RateLimitError } from './error.middleware';

/**
 * Simple In-Memory Rate Limiter
 * For production, replace with Redis-based rate limiter
 * Based on Part 4D specifications
 */

interface RateLimitStore {
  [key: string]: {
    count: number;
    resetAt: number;
  };
}

const store: RateLimitStore = {};

// Clean up expired entries every minute
setInterval(() => {
  const now = Date.now();
  Object.keys(store).forEach(key => {
    if (store[key].resetAt < now) {
      delete store[key];
    }
  });
}, 60000);

export interface RateLimitOptions {
  windowMs: number;   // Time window in milliseconds
  max: number;        // Max requests per window
  keyGenerator?: (req: Request) => string;  // Custom key generator
  skip?: (req: Request) => boolean;         // Skip rate limiting for certain requests
}

/**
 * Rate Limit Middleware
 */
export function rateLimit(options: RateLimitOptions) {
  const {
    windowMs = 60000,  // Default: 1 minute
    max = 100,         // Default: 100 requests
    keyGenerator = defaultKeyGenerator,
    skip
  } = options;

  return (req: Request, res: Response, next: NextFunction): void => {
    // Skip if skip function returns true
    if (skip && skip(req)) {
      next();
      return;
    }

    const key = keyGenerator(req);
    const now = Date.now();

    // Get or create rate limit entry
    if (!store[key] || store[key].resetAt < now) {
      store[key] = {
        count: 0,
        resetAt: now + windowMs
      };
    }

    const entry = store[key];
    entry.count++;

    // Calculate rate limit headers
    const remaining = Math.max(0, max - entry.count);
    const reset = Math.floor(entry.resetAt / 1000);
    const retryAfter = Math.ceil((entry.resetAt - now) / 1000);

    // Set rate limit headers
    res.setHeader('X-RateLimit-Limit', max);
    res.setHeader('X-RateLimit-Remaining', remaining);
    res.setHeader('X-RateLimit-Reset', reset);
    res.setHeader('X-RateLimit-Window', Math.floor(windowMs / 1000));

    // Check if limit exceeded
    if (entry.count > max) {
      res.setHeader('Retry-After', retryAfter);

      const error = new RateLimitError(
        max,
        remaining,
        reset,
        retryAfter
      );

      next(error);
      return;
    }

    next();
  };
}

/**
 * Default key generator
 * Uses user ID if authenticated, otherwise IP address
 */
function defaultKeyGenerator(req: Request): string {
  if (req.user) {
    return `user:${req.user.userId}`;
  }

  // Get IP from various headers
  const ip =
    (req.headers['x-forwarded-for'] as string)?.split(',')[0]?.trim() ||
    (req.headers['x-real-ip'] as string) ||
    req.socket.remoteAddress ||
    'unknown';

  return `ip:${ip}`;
}

/**
 * Facility-based key generator
 */
export function facilityKeyGenerator(req: Request): string {
  if (req.user?.facilityId) {
    return `facility:${req.user.facilityId}`;
  }
  return defaultKeyGenerator(req);
}

/**
 * Predefined rate limiters based on Part 4D specifications
 */

// General API rate limiter: 100 requests per minute per user
export const generalRateLimit = rateLimit({
  windowMs: 60000,      // 1 minute
  max: 100
});

// Voice upload rate limiter: 10 uploads per minute per user
export const voiceUploadRateLimit = rateLimit({
  windowMs: 60000,      // 1 minute
  max: 10
});

// EHR sync rate limiter: 1 sync per patient per minute
export const ehrSyncRateLimit = rateLimit({
  windowMs: 60000,      // 1 minute
  max: 60               // 60 total syncs per minute per user
});

// Auth rate limiter: 5 login attempts per 15 minutes per IP
export const authRateLimit = rateLimit({
  windowMs: 900000,     // 15 minutes
  max: 5,
  keyGenerator: (req) => {
    // Always use IP for auth endpoints
    const ip =
      (req.headers['x-forwarded-for'] as string)?.split(',')[0]?.trim() ||
      (req.headers['x-real-ip'] as string) ||
      req.socket.remoteAddress ||
      'unknown';
    return `auth:${ip}:${req.body?.email || 'unknown'}`;
  }
});
