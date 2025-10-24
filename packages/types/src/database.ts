/**
 * Database table types
 * Generated from database schema
 */

import { UUID, Timestamps, HandoffStatus, HandoffPriority, UserRole } from './common';

export interface Facility extends Timestamps {
  id: UUID;
  name: string;
  facility_type: string;
  license_number?: string;
  email?: string;
  phone?: string;
  address_line1: string;
  city: string;
  state: string;
  zip_code: string;
  is_active: boolean;
}

export interface Staff extends Timestamps {
  id: UUID;
  facility_id: UUID;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
}

export interface Patient extends Timestamps {
  id: UUID;
  facility_id: UUID;
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  status: string;
}

export interface Handoff extends Timestamps {
  id: UUID;
  patient_id: UUID;
  facility_id: UUID;
  from_staff_id: UUID;
  to_staff_id?: UUID;
  status: HandoffStatus;
  priority: HandoffPriority;
  handoff_type: string;
}

export interface SBARReport extends Timestamps {
  id: UUID;
  handoff_id: UUID;
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
  version: number;
  is_latest: boolean;
}

export interface VoiceRecording extends Timestamps {
  id: UUID;
  handoff_id: UUID;
  uploaded_by: UUID;
  status: string;
  duration: number;
  file_size: number;
  audio_format: string;
  file_path: string;
}
