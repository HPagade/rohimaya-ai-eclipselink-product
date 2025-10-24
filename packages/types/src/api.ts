/**
 * API request and response types
 */

import { UUID, ApiResponse, PaginatedResponse } from './common';
import { Staff, Patient, Handoff, SBARReport, VoiceRecording } from './database';

// Authentication
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: Staff;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  facility_id: UUID;
  role: string;
}

// Handoffs
export interface CreateHandoffRequest {
  patient_id: UUID;
  handoff_type: string;
  priority?: string;
  scheduled_time?: string;
}

export interface UpdateHandoffRequest {
  status?: string;
  priority?: string;
  to_staff_id?: UUID;
}

export type HandoffListResponse = ApiResponse<PaginatedResponse<Handoff>>;
export type HandoffDetailResponse = ApiResponse<Handoff>;

// Voice Recordings
export interface UploadVoiceRequest {
  handoff_id: UUID;
  audio_file: File | Buffer;
  duration: number;
  audio_format: string;
}

export interface VoiceStatusResponse {
  recording_id: UUID;
  status: string;
  transcription?: string;
  error?: string;
}

// SBAR
export interface GenerateSBARRequest {
  handoff_id: UUID;
  is_initial: boolean;
}

export interface UpdateSBARRequest {
  situation?: string;
  background?: string;
  assessment?: string;
  recommendation?: string;
  edit_summary?: string;
}

export type SBARDetailResponse = ApiResponse<SBARReport>;

// Patients
export interface CreatePatientRequest {
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
}

export type PatientListResponse = ApiResponse<PaginatedResponse<Patient>>;
export type PatientDetailResponse = ApiResponse<Patient>;
