import api from './api'

export interface Patient {
  id: number
  facility_id: number
  mrn: string
  first_name: string
  last_name: string
  date_of_birth: string
  gender?: string
  phone?: string
  email?: string
  room_number?: string
  admission_date?: string
  discharge_date?: string
  primary_diagnosis?: string
  allergies?: string
  code_status?: string
  status: string
  created_at: string
  updated_at: string
}

export interface PatientCreate {
  mrn: string
  first_name: string
  last_name: string
  date_of_birth: string
  gender?: string
  phone?: string
  email?: string
  room_number?: string
  admission_date?: string
  primary_diagnosis?: string
  allergies?: string
  code_status?: string
}

export interface PatientList {
  patients: Patient[]
  total: number
  page: number
  page_size: number
}

const patientService = {
  async list(params?: {
    page?: number
    page_size?: number
    search?: string
    status_filter?: string
  }): Promise<PatientList> {
    const response = await api.get('/patients', { params })
    return response.data
  },

  async get(id: number): Promise<Patient> {
    const response = await api.get(`/patients/${id}`)
    return response.data
  },

  async create(data: PatientCreate): Promise<Patient> {
    const response = await api.post('/patients', data)
    return response.data
  },

  async update(id: number, data: Partial<PatientCreate>): Promise<Patient> {
    const response = await api.put(`/patients/${id}`, data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/patients/${id}`)
  },
}

export default patientService
