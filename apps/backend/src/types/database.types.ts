/**
 * Database Types
 * TypeScript types matching PostgreSQL schema
 */

import { UUID } from '@eclipselink/types';

// =============================================================================
// ENUMS (matching PostgreSQL ENUM types)
// =============================================================================

export type FacilityType =
  | 'hospital'
  | 'clinic'
  | 'nursing_home'
  | 'assisted_living'
  | 'home_health'
  | 'ambulatory_care'
  | 'rehabilitation'
  | 'mental_health';

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

export type EmploymentStatus =
  | 'full_time'
  | 'part_time'
  | 'per_diem'
  | 'contract'
  | 'inactive';

export type Gender = 'male' | 'female' | 'other' | 'unknown';

export type BloodType =
  | 'A+'
  | 'A-'
  | 'B+'
  | 'B-'
  | 'AB+'
  | 'AB-'
  | 'O+'
  | 'O-'
  | 'unknown';

export type PatientStatus =
  | 'active'
  | 'discharged'
  | 'deceased'
  | 'transferred';

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

export type RecordingStatus =
  | 'uploading'
  | 'uploaded'
  | 'processing'
  | 'transcribed'
  | 'failed'
  | 'deleted';

export type AudioFormat = 'webm' | 'mp3' | 'wav' | 'ogg' | 'm4a';

export type GenerationStage = 'transcription' | 'sbar_generation';

export type GenerationStatus =
  | 'queued'
  | 'processing'
  | 'completed'
  | 'failed';

export type AssignmentRole =
  | 'giving'
  | 'receiving'
  | 'supervising'
  | 'cc'
  | 'reviewing';

export type AssignmentStatus =
  | 'pending'
  | 'notified'
  | 'accepted'
  | 'declined'
  | 'completed';

// =============================================================================
// TABLE TYPES (matching database schema)
// =============================================================================

export interface DBFacility {
  id: UUID;
  name: string;
  facility_type: FacilityType;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  country: string;
  phone: string;
  email: string;
  website: string | null;
  timezone: string;
  is_active: boolean;
  settings: any; // JSONB
  created_at: Date;
  updated_at: Date;
}

export interface DBStaff {
  id: UUID;
  facility_id: UUID;
  email: string;
  password_hash: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  employment_status: EmploymentStatus;
  phone: string | null;
  department: string | null;
  employee_id: string | null;
  license_number: string | null;
  license_state: string | null;
  license_expiration: Date | null;
  is_active: boolean;
  last_login_at: Date | null;
  email_verified: boolean;
  email_verified_at: Date | null;
  two_factor_enabled: boolean;
  preferences: any; // JSONB
  created_at: Date;
  updated_at: Date;
}

export interface DBPatient {
  id: UUID;
  facility_id: UUID;
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: Date;
  gender: Gender;
  blood_type: BloodType;
  status: PatientStatus;
  admission_date: Date | null;
  discharge_date: Date | null;
  room_number: string | null;
  bed_number: string | null;
  department: string | null;
  attending_physician_id: UUID | null;
  primary_nurse_id: UUID | null;
  acuity_level: number | null;
  weight_kg: number | null;
  height_cm: number | null;
  phone: string | null;
  email: string | null;
  emergency_contact_name: string | null;
  emergency_contact_relationship: string | null;
  emergency_contact_phone: string | null;
  address: string | null;
  city: string | null;
  state: string | null;
  zip_code: string | null;
  insurance_provider: string | null;
  insurance_policy_number: string | null;
  primary_diagnosis: string | null;
  secondary_diagnoses: string[] | null; // TEXT[]
  allergies: any; // JSONB[]
  medications: any; // JSONB[]
  vital_signs: any; // JSONB
  clinical_notes: string | null;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface DBHandoff {
  id: UUID;
  patient_id: UUID;
  facility_id: UUID;
  from_staff_id: UUID;
  to_staff_id: UUID | null;
  status: HandoffStatus;
  priority: HandoffPriority;
  handoff_type: string;
  location: string | null;
  scheduled_time: Date | null;
  actual_time: Date | null;
  voice_recording_started_at: Date | null;
  voice_recording_completed_at: Date | null;
  transcription_started_at: Date | null;
  transcription_completed_at: Date | null;
  sbar_generation_started_at: Date | null;
  sbar_generation_completed_at: Date | null;
  recording_duration: number | null;
  transcription_duration: number | null;
  sbar_generation_duration: number | null;
  total_processing_time: number | null; // GENERATED COLUMN
  clinical_notes: string | null;
  internal_notes: string | null;
  quality_score: number | null;
  reviewed_by: UUID | null;
  reviewed_at: Date | null;
  review_comments: string | null;
  is_critical: boolean;
  requires_followup: boolean;
  flagged_for_review: boolean;
  exported_to_ehr: boolean;
  export_attempted_at: Date | null;
  export_completed_at: Date | null;
  export_error: string | null;
  version: number;
  created_at: Date;
  updated_at: Date;
  completed_at: Date | null;
  cancelled_at: Date | null;
  cancelled_by: UUID | null;
  cancellation_reason: string | null;
}

export interface DBVoiceRecording {
  id: UUID;
  handoff_id: UUID;
  uploaded_by: UUID;
  file_path: string;
  file_size: number;
  audio_format: AudioFormat;
  duration: number;
  status: RecordingStatus;
  transcription_text: string | null;
  transcription_confidence: number | null;
  transcription_word_count: number | null;
  transcription_language: string | null;
  transcription_model: string | null;
  processing_error: string | null;
  azure_job_id: string | null;
  started_processing_at: Date | null;
  completed_processing_at: Date | null;
  deleted_at: Date | null;
  deleted_by: UUID | null;
  created_at: Date;
  updated_at: Date;
}

export interface DBSBARReport {
  id: UUID;
  handoff_id: UUID;
  patient_id: UUID;
  facility_id: UUID;
  version: number;
  previous_version_id: UUID | null;
  is_latest: boolean;
  is_initial: boolean;
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
  changes_since_last_version: any; // JSONB[]
  completeness_score: number;
  readability_score: number;
  adherence_to_ipass: boolean;
  critical_info_present: boolean;
  ai_model_used: string;
  ai_generation_type: 'initial' | 'update';
  ai_confidence_score: number;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  generation_duration: number;
  manually_edited: boolean;
  edited_by: UUID | null;
  edited_at: Date | null;
  edit_notes: string | null;
  approved_by: UUID | null;
  approved_at: Date | null;
  status: 'draft' | 'final' | 'archived';
  created_at: Date;
  updated_at: Date;
}

export interface DBAuditLog {
  id: UUID;
  facility_id: UUID;
  user_id: UUID | null;
  action: string;
  resource_type: string;
  resource_id: UUID | null;
  old_values: any; // JSONB
  new_values: any; // JSONB
  ip_address: string | null;
  user_agent: string | null;
  session_id: string | null;
  success: boolean;
  error_message: string | null;
  created_at: Date;
}

export interface DBAuthSession {
  id: UUID;
  user_id: UUID;
  refresh_token: string;
  token_id: string;
  device_info: any; // JSONB
  ip_address: string | null;
  user_agent: string | null;
  is_active: boolean;
  last_activity_at: Date;
  expires_at: Date;
  created_at: Date;
}

// =============================================================================
// QUERY RESULT TYPES (with JOINs)
// =============================================================================

export interface HandoffWithRelations extends DBHandoff {
  patient: DBPatient;
  from_staff: Pick<DBStaff, 'id' | 'first_name' | 'last_name' | 'role'>;
  to_staff: Pick<DBStaff, 'id' | 'first_name' | 'last_name' | 'role'> | null;
  voice_recording?: DBVoiceRecording;
  sbar_report?: DBSBARReport;
}

export interface StaffWithFacility extends DBStaff {
  facility: DBFacility;
}

// =============================================================================
// INPUT TYPES (for INSERT/UPDATE operations)
// =============================================================================

export type InsertHandoff = Omit<
  DBHandoff,
  'id' | 'created_at' | 'updated_at' | 'total_processing_time'
>;

export type UpdateHandoff = Partial<
  Omit<DBHandoff, 'id' | 'created_at' | 'total_processing_time'>
>;

export type InsertVoiceRecording = Omit<
  DBVoiceRecording,
  'id' | 'created_at' | 'updated_at'
>;

export type UpdateVoiceRecording = Partial<
  Omit<DBVoiceRecording, 'id' | 'created_at'>
>;

export type InsertSBARReport = Omit<
  DBSBARReport,
  'id' | 'created_at' | 'updated_at'
>;

export type UpdateSBARReport = Partial<
  Omit<DBSBARReport, 'id' | 'created_at'>
>;
