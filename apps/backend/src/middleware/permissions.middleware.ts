import { Request, Response, NextFunction } from 'express';

/**
 * Permission Check Middleware
 * Verifies user has required permission
 * Based on Part 4A RBAC specifications
 */
export function requirePermission(permission: string) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const user = req.user;

    if (!user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_REQUIRED',
          message: 'Authentication required'
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
      return;
    }

    // Super admin has all permissions
    if (user.role === 'super_admin') {
      next();
      return;
    }

    // Check if user has wildcard permission
    if (user.permissions.includes('*:*')) {
      next();
      return;
    }

    // Check if user has specific permission
    const hasPermission = user.permissions.includes(permission);

    if (!hasPermission) {
      res.status(403).json({
        success: false,
        error: {
          code: 'FORBIDDEN',
          message: 'You do not have permission to perform this action',
          details: {
            requiredPermission: permission,
            userPermissions: user.permissions
          }
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
      return;
    }

    next();
  };
}

/**
 * Require Multiple Permissions (all must match)
 */
export function requirePermissions(permissions: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const user = req.user;

    if (!user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_REQUIRED',
          message: 'Authentication required'
        }
      });
      return;
    }

    // Super admin has all permissions
    if (user.role === 'super_admin' || user.permissions.includes('*:*')) {
      next();
      return;
    }

    // Check all permissions
    const missingPermissions = permissions.filter(
      perm => !user.permissions.includes(perm)
    );

    if (missingPermissions.length > 0) {
      res.status(403).json({
        success: false,
        error: {
          code: 'INSUFFICIENT_PERMISSIONS',
          message: 'Insufficient permissions to perform this action',
          details: {
            requiredPermissions: permissions,
            missingPermissions,
            userPermissions: user.permissions
          }
        }
      });
      return;
    }

    next();
  };
}

/**
 * Require Any Permission (at least one must match)
 */
export function requireAnyPermission(permissions: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const user = req.user;

    if (!user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_REQUIRED',
          message: 'Authentication required'
        }
      });
      return;
    }

    // Super admin has all permissions
    if (user.role === 'super_admin' || user.permissions.includes('*:*')) {
      next();
      return;
    }

    // Check if user has any of the required permissions
    const hasAnyPermission = permissions.some(
      perm => user.permissions.includes(perm)
    );

    if (!hasAnyPermission) {
      res.status(403).json({
        success: false,
        error: {
          code: 'FORBIDDEN',
          message: 'You do not have permission to perform this action',
          details: {
            requiredPermissions: permissions,
            userPermissions: user.permissions
          }
        }
      });
      return;
    }

    next();
  };
}

/**
 * Require Role
 */
export function requireRole(role: string | string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const user = req.user;

    if (!user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'AUTH_REQUIRED',
          message: 'Authentication required'
        }
      });
      return;
    }

    const allowedRoles = Array.isArray(role) ? role : [role];
    const hasRole = allowedRoles.includes(user.role);

    if (!hasRole) {
      res.status(403).json({
        success: false,
        error: {
          code: 'INSUFFICIENT_PERMISSIONS',
          message: 'Insufficient permissions to perform this action',
          details: {
            requiredRole: allowedRoles,
            currentRole: user.role
          }
        }
      });
      return;
    }

    next();
  };
}

/**
 * Generate request ID for tracking
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
