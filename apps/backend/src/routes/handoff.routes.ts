import { Router } from 'express';
import {
  createHandoff,
  listHandoffs,
  getHandoff,
  updateHandoff,
  assignHandoff,
  completeHandoff,
  deleteHandoff
} from '../controllers/handoff.controller';
import { authenticateJWT } from '../middleware/auth.middleware';
import { requirePermission } from '../middleware/permissions.middleware';
import {
  createHandoffSchema,
  listHandoffsSchema,
  getHandoffSchema,
  updateHandoffSchema,
  assignHandoffSchema,
  completeHandoffSchema,
  deleteHandoffSchema,
  validate
} from '../validators/handoff.validator';
import { asyncHandler } from '../middleware/error.middleware';
import { generalRateLimit } from '../middleware/rate-limit.middleware';

/**
 * Handoff Routes
 * Based on Part 4B specifications
 *
 * Endpoints:
 * - POST   /handoffs           - Create handoff
 * - GET    /handoffs           - List with filters
 * - GET    /handoffs/:id       - Get details
 * - PUT    /handoffs/:id       - Update
 * - POST   /handoffs/:id/assign - Assign to provider
 * - POST   /handoffs/:id/complete - Complete handoff
 * - DELETE /handoffs/:id       - Cancel/delete
 */

const router = Router();

// Apply authentication to all routes
router.use(authenticateJWT);

// Apply general rate limiting
router.use(generalRateLimit);

/**
 * POST /v1/handoffs
 * Create a new handoff
 */
router.post(
  '/',
  requirePermission('handoff:create'),
  validate(createHandoffSchema),
  asyncHandler(createHandoff)
);

/**
 * GET /v1/handoffs
 * List handoffs with filtering, sorting, and pagination
 */
router.get(
  '/',
  requirePermission('handoff:read'),
  validate(listHandoffsSchema),
  asyncHandler(listHandoffs)
);

/**
 * GET /v1/handoffs/:id
 * Get detailed handoff information by ID
 */
router.get(
  '/:id',
  requirePermission('handoff:read'),
  validate(getHandoffSchema),
  asyncHandler(getHandoff)
);

/**
 * PUT /v1/handoffs/:id
 * Update handoff information
 */
router.put(
  '/:id',
  requirePermission('handoff:update'),
  validate(updateHandoffSchema),
  asyncHandler(updateHandoff)
);

/**
 * POST /v1/handoffs/:id/assign
 * Assign handoff to a provider
 */
router.post(
  '/:id/assign',
  requirePermission('handoff:update'),
  validate(assignHandoffSchema),
  asyncHandler(assignHandoff)
);

/**
 * POST /v1/handoffs/:id/complete
 * Mark handoff as completed
 */
router.post(
  '/:id/complete',
  requirePermission('handoff:update'),
  validate(completeHandoffSchema),
  asyncHandler(completeHandoff)
);

/**
 * DELETE /v1/handoffs/:id
 * Cancel or delete a handoff
 */
router.delete(
  '/:id',
  requirePermission('handoff:delete'),
  validate(deleteHandoffSchema),
  asyncHandler(deleteHandoff)
);

export default router;
