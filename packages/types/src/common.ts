/**
 * Common types shared across the application
 */

export type UUID = string;

export interface Timestamps {
  created_at: string;
  updated_at: string;
}

export interface PaginationParams {
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  meta?: {
    timestamp: string;
    request_id: string;
  };
}

export type HandoffStatus =
  | 'draft'
  | 'recording'
  | 'transcribing'
  | 'generating'
  | 'ready'
  | 'assigned'
  | 'accepted'
  | 'completed'
  | 'cancelled'
  | 'failed';

export type HandoffPriority = 'routine' | 'urgent' | 'emergent';

export type UserRole =
  | 'registered_nurse'
  | 'licensed_practical_nurse'
  | 'certified_nursing_assistant'
  | 'medical_assistant'
  | 'physician'
  | 'nurse_practitioner'
  | 'physician_assistant'
  | 'respiratory_therapist'
  | 'physical_therapist'
  | 'occupational_therapist'
  | 'emergency_medical_technician'
  | 'radiologic_technician'
  | 'surgical_technician'
  | 'lab_technician'
  | 'pharmacy_technician'
  | 'admin'
  | 'super_admin';
