import api from './api'

export interface Handoff {
  id: number
  facility_id: number
  patient_id: number
  created_by_id: number
  assigned_to_id?: number
  handoff_type: string
  baseline_handoff_id?: number
  voice_recording_url?: string
  voice_recording_duration?: number
  transcription_text?: string
  sbar_situation?: string
  sbar_background?: string
  sbar_assessment?: string
  sbar_recommendation?: string
  status: string
  priority: string
  shift?: string
  has_critical_alerts: boolean
  critical_alerts?: any
  ai_confidence_score?: number
  ai_processing_time?: number
  submitted_at?: string
  received_at?: string
  created_at: string
  updated_at: string
  patient_name?: string
  created_by_name?: string
  assigned_to_name?: string
}

export interface HandoffCreate {
  patient_id: number
  assigned_to_id?: number
  handoff_type?: string
  baseline_handoff_id?: number
  transcription_text?: string
  sbar_situation?: string
  sbar_background?: string
  sbar_assessment?: string
  sbar_recommendation?: string
  priority?: string
  shift?: string
}

export interface HandoffList {
  handoffs: Handoff[]
  total: number
  page: number
  page_size: number
}

const handoffService = {
  async list(params?: {
    page?: number
    page_size?: number
    patient_id?: number
    status_filter?: string
    priority?: string
  }): Promise<HandoffList> {
    const response = await api.get('/handoffs', { params })
    return response.data
  },

  async get(id: number): Promise<Handoff> {
    const response = await api.get(`/handoffs/${id}`)
    return response.data
  },

  async create(data: HandoffCreate): Promise<Handoff> {
    const response = await api.post('/handoffs', data)
    return response.data
  },

  async update(id: number, data: Partial<HandoffCreate>): Promise<Handoff> {
    const response = await api.put(`/handoffs/${id}`, data)
    return response.data
  },

  async submit(id: number): Promise<Handoff> {
    const response = await api.post(`/handoffs/${id}/submit`)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/handoffs/${id}`)
  },
}

export default handoffService
