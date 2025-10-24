import { z } from 'zod';

/**
 * Handoff Validation Schemas
 * Based on Part 4B specifications
 */

// UUID validation
const uuidSchema = z
  .string()
  .uuid('Invalid UUID format');

// Handoff type validation
const handoffTypeSchema = z.enum([
  'shift_change',
  'transfer',
  'admission',
  'discharge',
  'procedure',
  'status_update'
], {
  errorMap: () => ({ message: 'Invalid handoff type' })
});

// Priority validation
const prioritySchema = z.enum([
  'routine',
  'urgent',
  'emergent'
], {
  errorMap: () => ({ message: 'Invalid priority level' })
});

// Status validation
const statusSchema = z.enum([
  'draft',
  'recording',
  'transcribing',
  'generating',
  'ready',
  'assigned',
  'accepted',
  'completed',
  'cancelled',
  'failed'
], {
  errorMap: () => ({ message: 'Invalid handoff status' })
});

/**
 * POST /v1/handoffs
 * Create new handoff
 */
export const createHandoffSchema = z.object({
  body: z.object({
    patientId: uuidSchema,
    fromStaffId: uuidSchema,
    toStaffId: uuidSchema.optional(),
    handoffType: handoffTypeSchema,
    priority: prioritySchema.optional().default('routine'),
    scheduledTime: z.string().datetime().optional(),
    location: z.string().max(100).optional(),
    clinicalNotes: z.string().max(5000).optional(),
    isCritical: z.boolean().optional().default(false),
    requiresFollowup: z.boolean().optional().default(false),
    // Initial vs Update workflow (Part 4C)
    isInitialHandoff: z.boolean().optional().default(false),
    previousHandoffId: uuidSchema.optional()
  })
});

/**
 * GET /v1/handoffs
 * List handoffs with filters
 */
export const listHandoffsSchema = z.object({
  query: z.object({
    page: z.coerce.number().int().min(1).optional().default(1),
    limit: z.coerce.number().int().min(1).max(100).optional().default(20),
    status: z.string().optional(),
    priority: z.string().optional(),
    handoffType: z.string().optional(),
    fromStaffId: uuidSchema.optional(),
    toStaffId: uuidSchema.optional(),
    patientId: uuidSchema.optional(),
    startDate: z.string().datetime().optional(),
    endDate: z.string().datetime().optional(),
    search: z.string().optional(),
    sortBy: z.string().optional().default('createdAt'),
    sortOrder: z.enum(['asc', 'desc']).optional().default('desc'),
    includeSbar: z.coerce.boolean().optional().default(false)
  })
});

/**
 * GET /v1/handoffs/:id
 * Get handoff details
 */
export const getHandoffSchema = z.object({
  params: z.object({
    id: uuidSchema
  })
});

/**
 * PUT /v1/handoffs/:id
 * Update handoff
 */
export const updateHandoffSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  body: z.object({
    status: statusSchema.optional(),
    toStaffId: uuidSchema.optional(),
    priority: prioritySchema.optional(),
    scheduledTime: z.string().datetime().optional(),
    location: z.string().max(100).optional(),
    clinicalNotes: z.string().max(5000).optional(),
    isCritical: z.boolean().optional(),
    requiresFollowup: z.boolean().optional()
  })
});

/**
 * POST /v1/handoffs/:id/assign
 * Assign handoff to provider
 */
export const assignHandoffSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  body: z.object({
    toStaffId: uuidSchema,
    notifyProvider: z.boolean().optional().default(true),
    notificationMethod: z.enum(['push', 'email', 'sms']).optional().default('push'),
    message: z.string().max(500).optional()
  })
});

/**
 * POST /v1/handoffs/:id/complete
 * Mark handoff as completed
 */
export const completeHandoffSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  body: z.object({
    completionNotes: z.string().max(5000).optional(),
    actualTime: z.string().datetime().optional()
  })
});

/**
 * DELETE /v1/handoffs/:id
 * Cancel/delete handoff
 */
export const deleteHandoffSchema = z.object({
  params: z.object({
    id: uuidSchema
  }),
  body: z.object({
    cancellationReason: z.string().max(500).optional()
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
