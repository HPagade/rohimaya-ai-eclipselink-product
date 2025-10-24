import { z } from 'zod';

/**
 * SBAR Validation Schemas
 * Based on Part 4C specifications
 */

// UUID validation
const uuidSchema = z
  .string()
  .uuid('Invalid UUID format');

/**
 * GET /v1/sbar/:handoffId
 * Get SBAR report for a handoff
 */
export const getSbarSchema = z.object({
  params: z.object({
    handoffId: uuidSchema
  })
});

/**
 * GET /v1/sbar/:handoffId/versions
 * Get all SBAR versions for a handoff chain
 */
export const getSbarVersionsSchema = z.object({
  params: z.object({
    handoffId: uuidSchema
  }),
  query: z.object({
    includeChanges: z.coerce.boolean().optional().default(true)
  })
});

/**
 * GET /v1/sbar/:id/compare
 * Compare two SBAR versions
 */
export const compareSbarSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  query: z.object({
    compareWith: uuidSchema
  })
});

/**
 * PUT /v1/sbar/:id
 * Edit SBAR report
 */
export const updateSbarSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  body: z.object({
    situation: z.string().max(5000).optional(),
    background: z.string().max(5000).optional(),
    assessment: z.string().max(5000).optional(),
    recommendation: z.string().max(5000).optional(),
    editSummary: z.string().max(500).optional(),
    section: z.enum(['situation', 'background', 'assessment', 'recommendation']).optional()
  })
});

/**
 * POST /v1/sbar/:id/export
 * Export SBAR to various formats
 */
export const exportSbarSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  body: z.object({
    format: z.enum(['pdf', 'docx', 'txt', 'json']),
    includePatientPhoto: z.boolean().optional().default(false),
    includeVitalSigns: z.boolean().optional().default(true),
    includeChangeHistory: z.boolean().optional().default(true),
    includeAllVersions: z.boolean().optional().default(false)
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
