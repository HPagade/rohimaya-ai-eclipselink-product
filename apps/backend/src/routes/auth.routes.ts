import { Router } from 'express';
import {
  register,
  login,
  refresh,
  logout,
  getCurrentUser
} from '../controllers/auth.controller';
import { authenticateJWT } from '../middleware/auth.middleware';
import {
  registerSchema,
  loginSchema,
  refreshSchema,
  logoutSchema,
  validate
} from '../validators/auth.validator';
import { asyncHandler } from '../middleware/error.middleware';
import { authRateLimit } from '../middleware/rate-limit.middleware';

/**
 * Auth Routes
 * Based on Part 4A specifications
 *
 * Endpoints:
 * - POST   /auth/register       - Register new user
 * - POST   /auth/login          - Login
 * - POST   /auth/refresh        - Refresh access token
 * - POST   /auth/logout         - Logout
 * - GET    /auth/me             - Get current user
 * - PUT    /auth/me             - Update current user (TODO)
 * - POST   /auth/change-password - Change password (TODO)
 * - POST   /auth/forgot-password - Request password reset (TODO)
 * - POST   /auth/reset-password  - Reset password (TODO)
 * - POST   /auth/verify-email    - Verify email (TODO)
 */

const router = Router();

/**
 * POST /v1/auth/register
 * Register a new user account
 */
router.post(
  '/register',
  authRateLimit,
  validate(registerSchema),
  asyncHandler(register)
);

/**
 * POST /v1/auth/login
 * Authenticate user and receive JWT tokens
 */
router.post(
  '/login',
  authRateLimit,
  validate(loginSchema),
  asyncHandler(login)
);

/**
 * POST /v1/auth/refresh
 * Refresh access token using refresh token
 */
router.post(
  '/refresh',
  validate(refreshSchema),
  asyncHandler(refresh)
);

/**
 * POST /v1/auth/logout
 * Invalidate current session and tokens
 */
router.post(
  '/logout',
  authenticateJWT,
  validate(logoutSchema),
  asyncHandler(logout)
);

/**
 * GET /v1/auth/me
 * Get current authenticated user information
 */
router.get(
  '/me',
  authenticateJWT,
  asyncHandler(getCurrentUser)
);

/**
 * TODO: Implement remaining auth endpoints
 * - PUT /auth/me
 * - POST /auth/change-password
 * - POST /auth/forgot-password
 * - POST /auth/reset-password
 * - POST /auth/verify-email
 */

export default router;
