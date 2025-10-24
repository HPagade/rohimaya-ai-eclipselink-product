import { z } from 'zod';

/**
 * Auth Validation Schemas
 * Based on Part 4A specifications
 */

// Email validation
const emailSchema = z
  .string()
  .email('Invalid email format')
  .min(1, 'Email is required');

// Password validation: min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character');

// UUID validation
const uuidSchema = z
  .string()
  .uuid('Invalid UUID format');

// User role validation
const roleSchema = z.enum([
  'registered_nurse',
  'licensed_practical_nurse',
  'certified_nursing_assistant',
  'physician',
  'nurse_practitioner',
  'physician_assistant',
  'respiratory_therapist',
  'physical_therapist',
  'occupational_therapist',
  'speech_therapist',
  'social_worker',
  'case_manager',
  'pharmacist',
  'radiologist',
  'lab_technician',
  'admin',
  'super_admin'
], {
  errorMap: () => ({ message: 'Invalid role' })
});

// State code validation
const stateSchema = z
  .string()
  .length(2, 'State code must be 2 characters')
  .regex(/^[A-Z]{2}$/, 'State code must be uppercase letters');

/**
 * POST /auth/register
 */
export const registerSchema = z.object({
  body: z.object({
    email: emailSchema,
    password: passwordSchema,
    firstName: z
      .string()
      .min(2, 'First name must be at least 2 characters')
      .max(100, 'First name must be less than 100 characters'),
    lastName: z
      .string()
      .min(2, 'Last name must be at least 2 characters')
      .max(100, 'Last name must be less than 100 characters'),
    role: roleSchema,
    facilityId: uuidSchema,
    licenseNumber: z
      .string()
      .min(1, 'License number is required for clinical roles')
      .optional(),
    licenseState: stateSchema.optional()
  })
});

/**
 * POST /auth/login
 */
export const loginSchema = z.object({
  body: z.object({
    email: emailSchema,
    password: z.string().min(1, 'Password is required')
  })
});

/**
 * POST /auth/refresh
 */
export const refreshSchema = z.object({
  body: z.object({
    refreshToken: z.string().min(1, 'Refresh token is required')
  })
});

/**
 * POST /auth/logout
 */
export const logoutSchema = z.object({
  body: z.object({
    refreshToken: z.string().min(1, 'Refresh token is required')
  })
});

/**
 * POST /auth/forgot-password
 */
export const forgotPasswordSchema = z.object({
  body: z.object({
    email: emailSchema
  })
});

/**
 * POST /auth/reset-password
 */
export const resetPasswordSchema = z.object({
  body: z.object({
    token: z.string().min(1, 'Reset token is required'),
    password: passwordSchema
  })
});

/**
 * POST /auth/verify-email
 */
export const verifyEmailSchema = z.object({
  body: z.object({
    token: z.string().min(1, 'Verification token is required')
  })
});

/**
 * PUT /auth/me
 */
export const updateProfileSchema = z.object({
  body: z.object({
    preferredName: z.string().max(100).optional(),
    phone: z.string().regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number').optional(),
    preferences: z.object({
      language: z.string().optional(),
      timezone: z.string().optional(),
      notifications: z.object({
        email: z.boolean().optional(),
        push: z.boolean().optional(),
        sms: z.boolean().optional()
      }).optional()
    }).optional()
  })
});

/**
 * POST /auth/change-password
 */
export const changePasswordSchema = z.object({
  body: z.object({
    currentPassword: z.string().min(1, 'Current password is required'),
    newPassword: passwordSchema
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
