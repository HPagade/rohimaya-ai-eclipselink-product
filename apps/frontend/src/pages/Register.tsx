import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import authService, { RegisterData } from '@/services/authService'
import toast from 'react-hot-toast'

const ROLES = [
  { value: 'RN', label: 'Registered Nurse (RN)' },
  { value: 'LPN', label: 'Licensed Practical Nurse (LPN)' },
  { value: 'CNA', label: 'Certified Nursing Assistant (CNA)' },
  { value: 'MD', label: 'Physician (MD/DO)' },
  { value: 'NP', label: 'Nurse Practitioner (NP)' },
  { value: 'PA', label: 'Physician Assistant (PA)' },
  { value: 'RT', label: 'Respiratory Therapist (RT)' },
  { value: 'PT', label: 'Physical Therapist (PT)' },
  { value: 'OT', label: 'Occupational Therapist (OT)' },
  { value: 'PharmD', label: 'Pharmacist (PharmD)' },
  { value: 'SW', label: 'Social Worker' },
  { value: 'CM', label: 'Case Manager' },
  { value: 'MA', label: 'Medical Assistant (MA)' },
  { value: 'EMT', label: 'Emergency Medical Technician (EMT)' },
  { value: 'Admin', label: 'Administrator' },
]

export default function Register() {
  const [formData, setFormData] = useState<RegisterData>({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: '',
    department: '',
    phone: '',
    facility_name: '',
  })
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (formData.password !== confirmPassword) {
      toast.error('Passwords do not match')
      return
    }
    if (formData.password.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }
    setLoading(true)
    try {
      const response = await authService.register(formData)
      login(response.access_token, response.user)
      toast.success('Account created successfully!')
      navigate('/dashboard')
    } catch (error: any) {
      console.error('Registration error:', error)
      toast.error(error.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-peacock-teal-50 to-lunar-blue-50 px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-peacock-teal-500 rounded-full flex items-center justify-center">
              <span className="text-white text-2xl font-bold">E</span>
            </div>
          </div>
          <h1 className="text-3xl font-display font-bold text-lunar-blue-500">Create Your Account</h1>
          <p className="text-gray-600 mt-2">Join EclipseLink AI and transform clinical handoffs</p>
        </div>

        <div className="bg-white rounded-2xl shadow-large p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Hospital/Facility Name *</label>
              <input type="text" name="facility_name" required value={formData.facility_name} onChange={handleChange} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition" placeholder="Memorial Hospital" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
                <input type="text" name="first_name" required value={formData.first_name} onChange={handleChange} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition" placeholder="Jane" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
                <input type="text" name="last_name" required value={formData.last_name} onChange={handleChange} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition" placeholder="Smith" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email Address *</label>
              <input type="email" name="email" required value={formData.email} onChange={handleChange} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition" placeholder="you@hospital.com" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Role *</label>
                <select name="role" required value={formData.role} onChange={handleChange} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition">
                  <option value="">Select your role</option>
                  {ROLES.map((role) => (
                    <option key={role.value} value={role.value}>{role.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Department</label>
                <input type="text" name="department" value={formData.department} onChange={handleChange} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition" placeholder="Emergency, ICU, etc." />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Password *</label>
                <input type="password" name="password" required value={formData.password} onChange={handleChange} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition" placeholder="Min. 8 characters" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Confirm Password *</label>
                <input type="password" required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition" placeholder="Confirm password" />
              </div>
            </div>

            <button type="submit" disabled={loading} className="w-full bg-peacock-teal-500 text-white py-3 rounded-lg font-medium hover:bg-peacock-teal-600 focus:ring-4 focus:ring-peacock-teal-200 transition disabled:opacity-50 disabled:cursor-not-allowed">
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <p className="text-center text-sm text-gray-600 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-peacock-teal-600 hover:text-peacock-teal-700 font-medium">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
