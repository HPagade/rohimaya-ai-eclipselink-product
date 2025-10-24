import { z } from 'zod';

/**
 * Voice Recording Validation Schemas
 * Based on Part 4B specifications
 */

// UUID validation
const uuidSchema = z
  .string()
  .uuid('Invalid UUID format');

/**
 * POST /v1/voice/upload
 * Upload voice recording
 * Note: File validation handled by multer middleware
 */
export const uploadVoiceSchema = z.object({
  body: z.object({
    handoffId: uuidSchema,
    duration: z.coerce.number().int().min(1).max(600) // 1 second to 10 minutes
  })
});

/**
 * GET /v1/voice/:id
 * Get voice recording details
 */
export const getVoiceSchema = z.object({
  params: z.object({
    id: uuidSchema
  })
});

/**
 * GET /v1/voice/:id/download
 * Get presigned URL for download
 */
export const downloadVoiceSchema = z.object({
  params: z.object({
    id: uuidSchema
  })
});

/**
 * GET /v1/voice/:id/status
 * Get transcription/processing status
 */
export const getVoiceStatusSchema = z.object({
  params: z.object({
    id: uuidSchema
  })
});

/**
 * DELETE /v1/voice/:id
 * Delete voice recording
 */
export const deleteVoiceSchema = z.object({
  params: z.object({
    id: uuidSchema
  })
});

/**
 * Validation middleware
 */
export function validate(schema: z.ZodSchema) {
  return async (req: any, res: any, next: any) => {
    try {
      await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params
      });
      next();
    } catch (error) {
      next(error);
    }
  };
}
