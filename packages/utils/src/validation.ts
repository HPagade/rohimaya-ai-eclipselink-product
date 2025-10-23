/**
 * Validation utilities using Zod
 */

import { z } from 'zod';

// Email validation
export const emailSchema = z.string().email('Invalid email address');

// Password validation (min 8 chars, uppercase, lowercase, number)
export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number');

// Phone validation (US format)
export const phoneSchema = z
  .string()
  .regex(/^\+?1?\d{10,}$/, 'Invalid phone number');

// MRN validation
export const mrnSchema = z.string().min(1, 'MRN is required');

// UUID validation
export const uuidSchema = z.string().uuid('Invalid ID format');

// Date validation
export const dateSchema = z.string().datetime('Invalid date format');

// Pagination validation
export const paginationSchema = z.object({
  page: z.number().int().min(1).default(1),
  limit: z.number().int().min(1).max(100).default(20)
});
