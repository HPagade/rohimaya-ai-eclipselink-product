import { useState } from 'react'
import { Link } from 'react-router-dom'
// import { useNavigate } from 'react-router-dom'  // Will be used in Day 2
// import { useAuthStore } from '@/store/authStore'  // Will be used in Day 2
import toast from 'react-hot-toast'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  // const navigate = useNavigate()  // Will be used in Day 2
  // const login = useAuthStore((state) => state.login)  // Will be used in Day 2

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // TODO: Replace with actual API call
      // const response = await authService.login(email, password)
      // login(response.token, response.user)

      // Placeholder for development
      toast.success('Login functionality coming soon!')
      console.log('Login attempted:', { email, password })
    } catch (error) {
      toast.error('Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-peacock-teal-50 to-lunar-blue-50 px-4">
      <div className="max-w-md w-full">
        {/* Logo and Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-peacock-teal-500 rounded-full flex items-center justify-center">
              <span className="text-white text-2xl font-bold">E</span>
            </div>
          </div>
          <h1 className="text-3xl font-display font-bold text-lunar-blue-500">
            EclipseLink AI
          </h1>
          <p className="text-gray-600 mt-2">
            Voice-Enabled Clinical Handoff Platform
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-2xl shadow-large p-8">
          <h2 className="text-2xl font-semibold text-lunar-blue-500 mb-6">
            Sign In
          </h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email */}
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition"
                placeholder="you@hospital.com"
              />
            </div>

            {/* Password */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500 focus:border-transparent transition"
                placeholder="Enter your password"
              />
            </div>

            {/* Forgot Password */}
            <div className="flex items-center justify-between">
              <Link
                to="/forgot-password"
                className="text-sm text-peacock-teal-600 hover:text-peacock-teal-700"
              >
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-peacock-teal-500 text-white py-3 rounded-lg font-medium hover:bg-peacock-teal-600 focus:ring-4 focus:ring-peacock-teal-200 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          {/* Register Link */}
          <p className="text-center text-sm text-gray-600 mt-6">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="text-peacock-teal-600 hover:text-peacock-teal-700 font-medium"
            >
              Sign up
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-gray-500 mt-8">
          Part of the Rohimaya Health AI Ecosystem
        </p>
      </div>
    </div>
  )
}
