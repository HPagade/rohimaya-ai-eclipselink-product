import { Request, Response, NextFunction } from 'express';
import { verifyAccessToken } from '../utils/jwt.util';

/**
 * Authentication Middleware
 * Verifies JWT token and attaches user to request
 * Based on Part 4A specifications
 */
export function authenticateJWT(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  try {
    // Get token from Authorization header
    const authHeader = req.headers.authorization;

    if (!authHeader) {
      res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_REQUIRED',
          message: 'Authentication is required to access this resource'
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
      return;
    }

    // Extract token from "Bearer <token>" format
    const parts = authHeader.split(' ');
    if (parts.length !== 2 || parts[0] !== 'Bearer') {
      res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_INVALID_TOKEN',
          message: 'Invalid authorization header format. Expected: Bearer <token>'
        }
      });
      return;
    }

    const token = parts[1];

    // Verify token
    const decoded = verifyAccessToken(token);

    // Attach user to request
    req.user = {
      userId: decoded.userId,
      facilityId: decoded.facilityId,
      role: decoded.role,
      permissions: decoded.permissions
    };

    next();
  } catch (error) {
    if (error instanceof Error && error.message === 'AUTH_INVALID_TOKEN') {
      res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_INVALID_TOKEN',
          message: 'Invalid or expired authentication token',
          details: {
            reason: 'Token verification failed'
          }
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
      return;
    }

    // Unexpected error
    res.status(500).json({
      success: false,
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An internal server error occurred'
      }
    });
  }
}

/**
 * Optional Authentication Middleware
 * Attaches user if token present, but doesn't require it
 */
export function optionalAuth(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader) {
      next();
      return;
    }

    const parts = authHeader.split(' ');
    if (parts.length === 2 && parts[0] === 'Bearer') {
      const token = parts[1];
      const decoded = verifyAccessToken(token);

      req.user = {
        userId: decoded.userId,
        facilityId: decoded.facilityId,
        role: decoded.role,
        permissions: decoded.permissions
      };
    }

    next();
  } catch {
    // Silently fail - token invalid but not required
    next();
  }
}

/**
 * Generate request ID for tracking
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
