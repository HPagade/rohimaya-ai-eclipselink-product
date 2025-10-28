import { Router } from 'express';
import {
  createPatient,
  listPatients,
  getPatient,
  updatePatient,
  getPatientHandoffs
} from '../controllers/patient.controller';
import { authenticateJWT } from '../middleware/auth.middleware';
import { requirePermission } from '../middleware/permissions.middleware';
import {
  listPatientsSchema,
  getPatientSchema,
  getPatientHandoffsSchema,
  validate
} from '../validators/patient.validator';
import { asyncHandler } from '../middleware/error.middleware';
import { generalRateLimit } from '../middleware/rate-limit.middleware';

/**
 * Patient Routes
 * Based on Part 4C specifications
 *
 * Endpoints:
 * - GET    /patients            - List patients
 * - GET    /patients/:id        - Get patient details
 * - GET    /patients/:id/handoffs - Get patient handoff history
 */

const router = Router();

// Apply authentication to all routes
router.use(authenticateJWT);

// Apply general rate limiting
router.use(generalRateLimit);

/**
 * POST /v1/patients
 * Create a new patient
 */
router.post(
  '/',
  requirePermission('patient:create'),
  asyncHandler(createPatient)
);

/**
 * GET /v1/patients
 * List patients with search, filtering, and pagination
 */
router.get(
  '/',
  requirePermission('patient:read'),
  validate(listPatientsSchema),
  asyncHandler(listPatients)
);

/**
 * GET /v1/patients/:id
 * Get detailed patient information
 */
router.get(
  '/:id',
  requirePermission('patient:read'),
  validate(getPatientSchema),
  asyncHandler(getPatient)
);

/**
 * PUT /v1/patients/:id
 * Update patient information
 */
router.put(
  '/:id',
  requirePermission('patient:update'),
  asyncHandler(updatePatient)
);

/**
 * GET /v1/patients/:id/handoffs
 * Get patient's complete handoff history with SBAR evolution
 */
router.get(
  '/:id/handoffs',
  requirePermission('patient:read'),
  validate(getPatientHandoffsSchema),
  asyncHandler(getPatientHandoffs)
);

export default router;
