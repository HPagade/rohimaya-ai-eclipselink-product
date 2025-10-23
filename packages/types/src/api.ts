/**
 * API request and response types
 */

import { Handoff, Patient, Staff, SBARReport, VoiceRecording } from './database';

// Authentication
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: Staff;
  token: string;
  refreshToken: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  facility_id: string;
  role: string;
  discipline: string;
  license_number: string;
  phone: string;
}

// Handoffs
export interface CreateHandoffRequest {
  patient_id: string;
  receiving_provider_id?: string;
  scheduled_time?: string;
}

export interface UpdateHandoffRequest {
  receiving_provider_id?: string;
  scheduled_time?: string;
  status?: string;
}

export interface HandoffResponse {
  handoff: Handoff;
  patient?: Patient;
  giving_provider?: Staff;
  receiving_provider?: Staff;
  voice_recording?: VoiceRecording;
  sbar_report?: SBARReport;
}

// Voice Processing
export interface UploadVoiceRequest {
  handoff_id: string;
}

export interface UploadVoiceResponse {
  recording_id: string;
  upload_url: string;
  job_id: string;
}

export interface VoiceStatusResponse {
  recording_id: string;
  status: string;
  transcription?: string;
  sbar?: SBARReport;
  progress: number;
  error?: string;
}

// Patients
export interface CreatePatientRequest {
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'male' | 'female' | 'other';
  room_number?: string;
  primary_diagnosis?: string;
  allergies?: string[];
}

export interface UpdatePatientRequest {
  room_number?: string;
  primary_diagnosis?: string;
  allergies?: string[];
}

// API Response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
