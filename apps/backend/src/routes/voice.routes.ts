import { Router } from 'express';
import {
  uploadVoiceRecording,
  getVoiceRecording,
  getVoiceDownloadUrl,
  getVoiceStatus,
  deleteVoiceRecording
} from '../controllers/voice.controller';
import { authenticateJWT } from '../middleware/auth.middleware';
import { requirePermission } from '../middleware/permissions.middleware';
import {
  uploadVoiceSchema,
  getVoiceSchema,
  downloadVoiceSchema,
  getVoiceStatusSchema,
  deleteVoiceSchema,
  validate
} from '../validators/voice.validator';
import { asyncHandler } from '../middleware/error.middleware';
import { voiceUpload, handleMulterError } from '../middleware/upload.middleware';
import { voiceUploadRateLimit } from '../middleware/rate-limit.middleware';

/**
 * Voice Recording Routes
 * Based on Part 4B specifications
 *
 * Endpoints:
 * - POST   /voice/upload        - Upload audio
 * - GET    /voice/:id           - Get recording details
 * - GET    /voice/:id/download  - Get presigned URL
 * - GET    /voice/:id/status    - Poll processing status
 * - DELETE /voice/:id           - Delete recording
 */

const router = Router();

// Apply authentication to all routes
router.use(authenticateJWT);

/**
 * POST /v1/voice/upload
 * Upload voice recording for transcription
 */
router.post(
  '/upload',
  requirePermission('voice:upload'),
  voiceUploadRateLimit,
  voiceUpload.single('audio'), // Multer middleware
  handleMulterError, // Multer error handler
  validate(uploadVoiceSchema),
  asyncHandler(uploadVoiceRecording)
);

/**
 * GET /v1/voice/:id
 * Get voice recording details
 */
router.get(
  '/:id',
  requirePermission('voice:read'),
  validate(getVoiceSchema),
  asyncHandler(getVoiceRecording)
);

/**
 * GET /v1/voice/:id/download
 * Get presigned URL for audio download
 */
router.get(
  '/:id/download',
  requirePermission('voice:read'),
  validate(downloadVoiceSchema),
  asyncHandler(getVoiceDownloadUrl)
);

/**
 * GET /v1/voice/:id/status
 * Get transcription/processing status
 */
router.get(
  '/:id/status',
  requirePermission('voice:read'),
  validate(getVoiceStatusSchema),
  asyncHandler(getVoiceStatus)
);

/**
 * DELETE /v1/voice/:id
 * Delete voice recording
 */
router.delete(
  '/:id',
  requirePermission('voice:delete'),
  validate(deleteVoiceSchema),
  asyncHandler(deleteVoiceRecording)
);

export default router;
