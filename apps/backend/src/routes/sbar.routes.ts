import { Router } from 'express';
import {
  getSbar,
  getSbarVersions,
  compareSbar,
  updateSbar,
  exportSbar
} from '../controllers/sbar.controller';
import { authenticateJWT } from '../middleware/auth.middleware';
import { requirePermission } from '../middleware/permissions.middleware';
import {
  getSbarSchema,
  getSbarVersionsSchema,
  compareSbarSchema,
  updateSbarSchema,
  exportSbarSchema,
  validate
} from '../validators/sbar.validator';
import { asyncHandler } from '../middleware/error.middleware';
import { generalRateLimit } from '../middleware/rate-limit.middleware';

/**
 * SBAR Routes
 * Based on Part 4C specifications
 *
 * Endpoints:
 * - GET    /sbar/:handoffId           - Get SBAR
 * - GET    /sbar/:handoffId/versions  - Version history
 * - GET    /sbar/:id/compare          - Compare versions
 * - PUT    /sbar/:id                  - Edit SBAR
 * - POST   /sbar/:id/export           - Export to PDF/DOCX
 */

const router = Router();

// Apply authentication to all routes
router.use(authenticateJWT);

// Apply general rate limiting
router.use(generalRateLimit);

/**
 * GET /v1/sbar/:handoffId
 * Get SBAR report for a specific handoff
 */
router.get(
  '/:handoffId',
  requirePermission('sbar:read'),
  validate(getSbarSchema),
  asyncHandler(getSbar)
);

/**
 * GET /v1/sbar/:handoffId/versions
 * Get all SBAR versions for a patient's handoff chain
 */
router.get(
  '/:handoffId/versions',
  requirePermission('sbar:read'),
  validate(getSbarVersionsSchema),
  asyncHandler(getSbarVersions)
);

/**
 * GET /v1/sbar/:id/compare
 * Compare two SBAR versions to see what changed
 */
router.get(
  '/:id/compare',
  requirePermission('sbar:read'),
  validate(compareSbarSchema),
  asyncHandler(compareSbar)
);

/**
 * PUT /v1/sbar/:id
 * Edit SBAR report
 */
router.put(
  '/:id',
  requirePermission('sbar:update'),
  validate(updateSbarSchema),
  asyncHandler(updateSbar)
);

/**
 * POST /v1/sbar/:id/export
 * Export SBAR report to various formats
 */
router.post(
  '/:id/export',
  requirePermission('sbar:read'),
  validate(exportSbarSchema),
  asyncHandler(exportSbar)
);

export default router;
