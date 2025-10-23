/**
 * Database types and interfaces
 */

export interface Facility {
  id: string;
  name: string;
  type: 'hospital' | 'clinic' | 'nursing_home' | 'other';
  address: string;
  city: string;
  state: string;
  zip_code: string;
  phone: string;
  created_at: Date;
  updated_at: Date;
}

export interface Staff {
  id: string;
  facility_id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: StaffRole;
  discipline: StaffDiscipline;
  license_number: string;
  phone: string;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

export type StaffRole =
  | 'nurse'
  | 'doctor'
  | 'physician_assistant'
  | 'nurse_practitioner'
  | 'therapist'
  | 'technician'
  | 'admin'
  | 'super_admin';

export type StaffDiscipline =
  | 'RN'
  | 'LPN'
  | 'CNA'
  | 'MD'
  | 'DO'
  | 'PA'
  | 'NP'
  | 'RT'
  | 'PT'
  | 'OT'
  | 'EMT'
  | 'Radiologic Tech'
  | 'Surgical Tech'
  | 'Lab Tech'
  | 'Pharmacy Tech'
  | 'MA';

export interface Patient {
  id: string;
  facility_id: string;
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: Date;
  gender: 'male' | 'female' | 'other';
  room_number?: string;
  primary_diagnosis?: string;
  allergies?: string[];
  created_at: Date;
  updated_at: Date;
}

export interface Handoff {
  id: string;
  facility_id: string;
  patient_id: string;
  giving_provider_id: string;
  receiving_provider_id?: string;
  voice_recording_id?: string;
  sbar_report_id?: string;
  status: HandoffStatus;
  scheduled_time?: Date;
  completed_at?: Date;
  created_at: Date;
  updated_at: Date;
}

export type HandoffStatus =
  | 'draft'
  | 'recording'
  | 'processing'
  | 'ready'
  | 'assigned'
  | 'in_progress'
  | 'completed'
  | 'cancelled';

export interface VoiceRecording {
  id: string;
  handoff_id: string;
  storage_key: string;
  duration_seconds: number;
  file_size_bytes: number;
  format: string;
  transcription_status: TranscriptionStatus;
  transcription_text?: string;
  created_at: Date;
  updated_at: Date;
}

export type TranscriptionStatus =
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed';

export interface SBARReport {
  id: string;
  handoff_id: string;
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
  generation_status: GenerationStatus;
  version: number;
  created_at: Date;
  updated_at: Date;
}

export type GenerationStatus =
  | 'pending'
  | 'generating'
  | 'completed'
  | 'failed';
