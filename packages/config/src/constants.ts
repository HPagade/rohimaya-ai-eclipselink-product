/**
 * Application constants
 */

// Brand colors (Rohimaya Health AI)
export const BRAND_COLORS = {
  peacockTeal: '#1a9b8e',
  phoenixGold: '#f4c430',
  lunarBlue: '#2c3e50',
  moonWhite: '#f8f9fa',
  eclipseNavy: '#1a2332',
  accentCopper: '#b87333'
} as const;

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    LOGOUT: '/api/auth/logout',
    ME: '/api/auth/me',
    REFRESH: '/api/auth/refresh'
  },
  HANDOFFS: {
    LIST: '/api/handoffs',
    CREATE: '/api/handoffs',
    GET: (id: string) => `/api/handoffs/${id}`,
    UPDATE: (id: string) => `/api/handoffs/${id}`,
    DELETE: (id: string) => `/api/handoffs/${id}`,
    COMPLETE: (id: string) => `/api/handoffs/${id}/complete`
  },
  VOICE: {
    UPLOAD: '/api/voice/upload',
    STATUS: (jobId: string) => `/api/voice/status/${jobId}`,
    GET: (id: string) => `/api/voice/${id}`
  },
  PATIENTS: {
    LIST: '/api/patients',
    CREATE: '/api/patients',
    GET: (id: string) => `/api/patients/${id}`,
    UPDATE: (id: string) => `/api/patients/${id}`,
    SYNC_EHR: (id: string) => `/api/patients/${id}/sync-ehr`
  }
} as const;

// File upload limits
export const FILE_LIMITS = {
  MAX_VOICE_SIZE: 10 * 1024 * 1024, // 10MB
  MAX_VOICE_DURATION: 300, // 5 minutes in seconds
  ALLOWED_AUDIO_FORMATS: ['audio/webm', 'audio/mp3', 'audio/wav']
} as const;

// Pagination defaults
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_LIMIT: 20,
  MAX_LIMIT: 100
} as const;

// Cache TTL (in seconds)
export const CACHE_TTL = {
  SESSION: 86400, // 24 hours
  PATIENT: 3600, // 1 hour
  API_RESPONSE: 300, // 5 minutes
  RATE_LIMIT: 60 // 1 minute
} as const;

// Rate limits
export const RATE_LIMITS = {
  VOICE_UPLOAD: {
    MAX_REQUESTS: 10,
    WINDOW_MS: 60000 // 1 minute
  },
  API_CALLS: {
    MAX_REQUESTS: 100,
    WINDOW_MS: 60000 // 1 minute
  }
} as const;
