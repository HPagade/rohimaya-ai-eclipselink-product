import api from './api'

export interface RegisterData {
  email: string
  password: string
  first_name: string
  last_name: string
  role: string
  department?: string
  phone?: string
  facility_name: string
}

export interface LoginData {
  username: string  // OAuth2 uses 'username' field
  password: string
}

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  role: string
  department?: string
  facility_id: number
  facility_name: string
  is_admin: boolean
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

const authService = {
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  async login(email: string, password: string): Promise<AuthResponse> {
    // FastAPI OAuth2 expects form data
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout')
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me')
    return response.data
  },
}

export default authService
