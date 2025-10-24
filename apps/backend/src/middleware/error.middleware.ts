import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';

/**
 * Custom Error Classes
 * Based on Part 4D error specifications
 */
export class APIError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number = 500,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends APIError {
  constructor(message: string, details?: any) {
    super('VALIDATION_ERROR', message, 400, details);
    this.name = 'ValidationError';
  }
}

export class AuthenticationError extends APIError {
  constructor(code: string, message: string, details?: any) {
    super(code, message, 401, details);
    this.name = 'AuthenticationError';
  }
}

export class AuthorizationError extends APIError {
  constructor(message: string, details?: any) {
    super('FORBIDDEN', message, 403, details);
    this.name = 'AuthorizationError';
  }
}

export class NotFoundError extends APIError {
  constructor(resource: string, id?: string) {
    super(
      'NOT_FOUND',
      'Resource not found',
      404,
      { resource, id }
    );
    this.name = 'NotFoundError';
  }
}

export class ConflictError extends APIError {
  constructor(message: string, details?: any) {
    super('CONFLICT', message, 409, details);
    this.name = 'ConflictError';
  }
}

export class RateLimitError extends APIError {
  constructor(limit: number, remaining: number, reset: number, retryAfter: number) {
    super(
      'RATE_LIMIT_EXCEEDED',
      'Rate limit exceeded. Please try again later.',
      429,
      { limit, remaining, reset, retryAfter }
    );
    this.name = 'RateLimitError';
  }
}

/**
 * Error Handler Middleware
 * Converts errors to standardized API error responses
 * Based on Part 4D specifications
 */
export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Log error for debugging
  console.error('Error occurred:', {
    name: err.name,
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method
  });

  const requestId = (req.headers['x-request-id'] as string) || generateRequestId();
  const timestamp = new Date().toISOString();

  // Handle Zod validation errors
  if (err instanceof ZodError) {
    const validationDetails = err.errors.map(error => ({
      field: error.path.join('.'),
      message: error.message,
      code: 'INVALID_INPUT',
      value: error.path.length > 0 ? undefined : error.message
    }));

    res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Request validation failed',
        details: validationDetails
      },
      meta: {
        requestId,
        timestamp
      }
    });
    return;
  }

  // Handle custom API errors
  if (err instanceof APIError) {
    const statusCode = err.statusCode;

    // Add Retry-After header for rate limit errors
    if (err instanceof RateLimitError && err.details?.retryAfter) {
      res.setHeader('Retry-After', err.details.retryAfter);
    }

    res.status(statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
        ...(err.details && { details: err.details })
      },
      meta: {
        requestId,
        timestamp
      }
    });
    return;
  }

  // Handle known error types
  if (err.message === 'AUTH_INVALID_TOKEN') {
    res.status(401).json({
      success: false,
      error: {
        code: 'AUTH_INVALID_TOKEN',
        message: 'Invalid or expired authentication token'
      },
      meta: {
        requestId,
        timestamp
      }
    });
    return;
  }

  // Handle database errors
  if (err.name === 'SequelizeUniqueConstraintError' ||
      (err as any).code === '23505') {
    res.status(409).json({
      success: false,
      error: {
        code: 'ALREADY_EXISTS',
        message: 'A resource with this identifier already exists',
        details: {
          constraint: (err as any).constraint || 'unknown'
        }
      },
      meta: {
        requestId,
        timestamp
      }
    });
    return;
  }

  // Handle database foreign key errors
  if (err.name === 'SequelizeForeignKeyConstraintError' ||
      (err as any).code === '23503') {
    res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Referenced resource does not exist'
      },
      meta: {
        requestId,
        timestamp
      }
    });
    return;
  }

  // Handle multer file upload errors
  if (err.name === 'MulterError') {
    const multerErr = err as any;

    if (multerErr.code === 'LIMIT_FILE_SIZE') {
      res.status(400).json({
        success: false,
        error: {
          code: 'FILE_TOO_LARGE',
          message: 'Uploaded file exceeds maximum allowed size',
          details: {
            maxSize: 10485760,
            maxSizeFormatted: '10 MB'
          }
        },
        meta: {
          requestId,
          timestamp
        }
      });
      return;
    }
  }

  // Default to internal server error
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An internal server error occurred. Please try again later.',
      details: {
        requestId,
        timestamp,
        supportContact: 'support@eclipselink.ai'
      }
    },
    meta: {
      requestId,
      timestamp
    }
  });
}

/**
 * 404 Not Found Handler
 */
export function notFoundHandler(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  res.status(404).json({
    success: false,
    error: {
      code: 'NOT_FOUND',
      message: `Route ${req.method} ${req.path} not found`,
      details: {
        method: req.method,
        path: req.path
      }
    },
    meta: {
      requestId: (req.headers['x-request-id'] as string) || generateRequestId(),
      timestamp: new Date().toISOString()
    }
  });
}

/**
 * Async Error Handler Wrapper
 * Wraps async route handlers to catch errors
 */
export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

/**
 * Generate request ID for tracking
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
