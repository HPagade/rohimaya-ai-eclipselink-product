import api from './api'

// Types matching backend schemas
export interface SBARResponse {
  situation: string
  background: string
  assessment: string
  recommendation: string
}

export interface CriticalAlertResponse {
  alert_type: string
  severity: string
  confidence: number
  message: string
  recommended_actions: string
}

export interface HandoffResponse {
  id: number
  patient_id: number
  created_by_user_id: number
  is_baseline: boolean
  baseline_handoff_id?: number

  // Audio
  audio_duration_seconds?: number

  // Transcription
  transcript_text?: string
  transcript_confidence?: number

  // SBAR
  sbar?: SBARResponse

  // Critical alert
  critical_alert?: CriticalAlertResponse

  // Status
  status: string
  points_earned: number

  // Timestamps
  created_at: string
  ai_processed_at?: string
}

export interface CreateHandoffRequest {
  patient_id: number
  is_baseline: boolean
  user_id: number
  audio_file: Blob
}

/**
 * Upload a new handoff with voice recording
 * Returns the complete handoff with AI-generated SBAR
 */
export async function uploadHandoff(request: CreateHandoffRequest): Promise<HandoffResponse> {
  const formData = new FormData()
  formData.append('audio_file', request.audio_file, 'handoff.webm')
  formData.append('patient_id', request.patient_id.toString())
  formData.append('is_baseline', request.is_baseline.toString())
  formData.append('user_id', request.user_id.toString())

  const response = await api.post<HandoffResponse>('/handoffs/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 120000, // 2 minutes for AI processing
  })

  return response.data
}

/**
 * Get all handoffs for a patient
 */
export async function getHandoffsForPatient(patientId: number): Promise<HandoffResponse[]> {
  const response = await api.get<HandoffResponse[]>(`/handoffs?patient_id=${patientId}`)
  return response.data
}

/**
 * Get a specific handoff by ID
 */
export async function getHandoff(handoffId: number): Promise<HandoffResponse> {
  const response = await api.get<HandoffResponse>(`/handoffs/${handoffId}`)
  return response.data
}

/**
 * Get all handoffs (with optional filters)
 */
export async function getHandoffs(filters?: {
  patient_id?: number
  is_baseline?: boolean
  has_critical_alert?: boolean
  limit?: number
}): Promise<HandoffResponse[]> {
  const params = new URLSearchParams()
  if (filters?.patient_id) params.append('patient_id', filters.patient_id.toString())
  if (filters?.is_baseline !== undefined) params.append('is_baseline', filters.is_baseline.toString())
  if (filters?.has_critical_alert !== undefined) params.append('has_critical_alert', filters.has_critical_alert.toString())
  if (filters?.limit) params.append('limit', filters.limit.toString())

  const response = await api.get<HandoffResponse[]>(`/handoffs?${params.toString()}`)
  return response.data
}
