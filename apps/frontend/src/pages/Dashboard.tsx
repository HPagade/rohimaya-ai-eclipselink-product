import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import { useAuthStore } from '@/store/authStore'
import handoffService from '@/services/handoffService'
import patientService from '@/services/patientService'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const user = useAuthStore(state => state.user)
  const [stats, setStats] = useState({ patients: 0, handoffs: 0, pending: 0 })
  const [recentHandoffs, setRecentHandoffs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [handoffsRes, patientsRes] = await Promise.all([
        handoffService.list({ page_size: 5 }),
        patientService.list({ page_size: 1 })
      ])
      setRecentHandoffs(handoffsRes.handoffs)
      setStats({
        patients: patientsRes.total,
        handoffs: handoffsRes.total,
        pending: handoffsRes.handoffs.filter(h => h.status === 'draft').length
      })
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back, {user?.first_name}!</h1>
        <p className="text-gray-600 mb-8">{user?.role} • {user?.facility_name}</p>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Total Patients</div>
            <div className="text-3xl font-bold text-peacock-teal-600">{stats.patients}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Total Handoffs</div>
            <div className="text-3xl font-bold text-lunar-blue-600">{stats.handoffs}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Pending Handoffs</div>
            <div className="text-3xl font-bold text-phoenix-orange-600">{stats.pending}</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Link to="/handoff/new" className="bg-peacock-teal-500 hover:bg-peacock-teal-600 text-white rounded-lg shadow p-6 transition">
            <div className="text-2xl mb-2">➕</div>
            <div className="font-semibold">Create New Handoff</div>
            <div className="text-sm opacity-90">Start a new patient handoff</div>
          </Link>
          <Link to="/patients" className="bg-lunar-blue-500 hover:bg-lunar-blue-600 text-white rounded-lg shadow p-6 transition">
            <div className="text-2xl mb-2">👥</div>
            <div className="font-semibold">View Patients</div>
            <div className="text-sm opacity-90">Browse all patients</div>
          </Link>
        </div>

        {/* Recent Handoffs */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold">Recent Handoffs</h2>
          </div>
          <div className="p-6">
            {loading ? (
              <div className="text-center py-8 text-gray-500">Loading...</div>
            ) : recentHandoffs.length === 0 ? (
              <div className="text-center py-8 text-gray-500">No handoffs yet. Create your first one!</div>
            ) : (
              <div className="space-y-4">
                {recentHandoffs.map(handoff => (
                  <Link key={handoff.id} to={`/handoff/${handoff.id}`} className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="font-medium">{handoff.patient_name || `Patient ${handoff.patient_id}`}</div>
                        <div className="text-sm text-gray-600">Created by {handoff.created_by_name}</div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        handoff.status === 'submitted' ? 'bg-green-100 text-green-800' :
                        handoff.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {handoff.status}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}
