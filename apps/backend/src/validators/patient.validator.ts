import { z } from 'zod';

/**
 * Patient Validation Schemas
 * Based on Part 4C specifications
 */

// UUID validation
const uuidSchema = z
  .string()
  .uuid('Invalid UUID format');

/**
 * GET /v1/patients
 * List patients with search and filters
 */
export const listPatientsSchema = z.object({
  query: z.object({
    page: z.coerce.number().int().min(1).optional().default(1),
    limit: z.coerce.number().int().min(1).max(100).optional().default(20),
    search: z.string().optional(),
    status: z.enum(['active', 'discharged', 'transferred']).optional(),
    admissionDateStart: z.string().datetime().optional(),
    admissionDateEnd: z.string().datetime().optional(),
    department: z.string().optional(),
    hasInitialHandoff: z.coerce.boolean().optional(),
    sortBy: z.string().optional().default('lastName'),
    sortOrder: z.enum(['asc', 'desc']).optional().default('asc')
  })
});

/**
 * GET /v1/patients/:id
 * Get patient details
 */
export const getPatientSchema = z.object({
  params: z.object({
    id: uuidSchema
  })
});

/**
 * GET /v1/patients/:id/handoffs
 * Get patient's handoff history
 */
export const getPatientHandoffsSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  query: z.object({
    includeInitial: z.coerce.boolean().optional().default(true),
    includeUpdates: z.coerce.boolean().optional().default(true),
    includeSbar: z.coerce.boolean().optional().default(false),
    limit: z.coerce.number().int().min(1).max(100).optional().default(10)
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
