import axios from 'axios'
import { useAuthStore } from '@/store/authStore'
import toast from 'react-hot-toast'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000, // 30 seconds (for AI processing)
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // Unauthorized - logout user
          useAuthStore.getState().logout()
          toast.error('Session expired. Please login again.')
          window.location.href = '/login'
          break

        case 403:
          toast.error('You do not have permission to perform this action.')
          break

        case 404:
          toast.error('Resource not found.')
          break

        case 422:
          // Validation error
          const validationErrors = data.detail
          if (Array.isArray(validationErrors)) {
            validationErrors.forEach((err: any) => {
              toast.error(`${err.loc[1]}: ${err.msg}`)
            })
          } else {
            toast.error('Validation error occurred.')
          }
          break

        case 500:
          toast.error('Server error. Please try again later.')
          break

        default:
          toast.error(data.detail || 'An error occurred.')
      }
    } else if (error.request) {
      // Network error
      toast.error('Network error. Please check your connection.')
    } else {
      toast.error('An unexpected error occurred.')
    }

    return Promise.reject(error)
  }
)

export default api
