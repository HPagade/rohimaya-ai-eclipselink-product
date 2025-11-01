import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  role: string
  facility_id: number
  facility_name: string
  is_admin: boolean
  is_active: boolean
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (token: string, user: User) => void
  logout: () => void
  updateUser: (user: Partial<User>) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: (token, user) => {
        set({ token, user, isAuthenticated: true })
      },

      logout: () => {
        set({ token: null, user: null, isAuthenticated: false })
      },

      updateUser: (updatedUser) => {
        set((state) => ({
          user: state.user ? { ...state.user, ...updatedUser } : null,
        }))
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
