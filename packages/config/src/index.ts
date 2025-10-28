/**
 * Shared configuration constants for EclipseLink AI
 * @packageDocumentation
 */

export const CONSTANTS = {
  // Voice recording limits
  MAX_RECORDING_DURATION_MS: 10 * 60 * 1000, // 10 minutes
  MAX_FILE_SIZE_BYTES: 50 * 1024 * 1024, // 50MB

  // SBAR sections
  SBAR_SECTIONS: ['situation', 'background', 'assessment', 'recommendation'] as const,

  // Handoff statuses
  HANDOFF_STATUSES: ['draft', 'recording', 'processing', 'review', 'completed', 'archived'] as const,

  // User roles
  USER_ROLES: ['admin', 'physician', 'nurse', 'pa', 'np', 'staff'] as const,

  // Pagination
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,

  // API versions
  API_VERSION: 'v1',

  // JWT expiration
  JWT_EXPIRES_IN: '1h',
  REFRESH_TOKEN_EXPIRES_IN: '30d',
} as const;

export const ERRORS = {
  AUTH: {
    UNAUTHORIZED: 'Unauthorized access',
    INVALID_TOKEN: 'Invalid or expired token',
    INVALID_CREDENTIALS: 'Invalid email or password',
  },
  VALIDATION: {
    REQUIRED_FIELD: 'Required field missing',
    INVALID_FORMAT: 'Invalid data format',
  },
  HANDOFF: {
    NOT_FOUND: 'Handoff not found',
    PERMISSION_DENIED: 'Permission denied for this handoff',
  },
  VOICE: {
    UPLOAD_FAILED: 'Voice recording upload failed',
    FILE_TOO_LARGE: 'File size exceeds maximum limit',
    INVALID_FORMAT: 'Invalid audio format',
  },
} as const;

export type SBARSection = typeof CONSTANTS.SBAR_SECTIONS[number];
export type HandoffStatus = typeof CONSTANTS.HANDOFF_STATUSES[number];
export type UserRole = typeof CONSTANTS.USER_ROLES[number];
