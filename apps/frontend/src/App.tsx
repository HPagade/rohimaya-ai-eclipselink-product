import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

// Pages (to be created)
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Dashboard from '@/pages/Dashboard'
import VoiceRecorder from '@/pages/VoiceRecorder'
import HandoffDetail from '@/pages/HandoffDetail'
import Patients from '@/pages/Patients'
import Rewards from '@/pages/Rewards'
import AdminPanel from '@/pages/AdminPanel'

// Store
import { useAuthStore } from '@/store/authStore'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/handoff/new"
          element={
            <PrivateRoute>
              <VoiceRecorder />
            </PrivateRoute>
          }
        />
        <Route
          path="/handoff/:id"
          element={
            <PrivateRoute>
              <HandoffDetail />
            </PrivateRoute>
          }
        />
        <Route
          path="/patients"
          element={
            <PrivateRoute>
              <Patients />
            </PrivateRoute>
          }
        />
        <Route
          path="/rewards"
          element={
            <PrivateRoute>
              <Rewards />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              <AdminPanel />
            </PrivateRoute>
          }
        />

        {/* Default redirect */}
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
