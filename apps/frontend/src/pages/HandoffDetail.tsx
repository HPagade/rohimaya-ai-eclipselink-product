import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Layout from '@/components/Layout'
import handoffService, { Handoff } from '@/services/handoffService'
import toast from 'react-hot-toast'

export default function HandoffDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [handoff, setHandoff] = useState<Handoff | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadHandoff()
  }, [id])

  const loadHandoff = async () => {
    try {
      const data = await handoffService.get(Number(id))
      setHandoff(data)
    } catch (error) {
      console.error('Error loading handoff:', error)
      toast.error('Failed to load handoff')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    try {
      await handoffService.submit(Number(id))
      toast.success('Handoff submitted!')
      loadHandoff()
    } catch (error) {
      toast.error('Failed to submit handoff')
    }
  }

  if (loading) return <Layout><div className="text-center py-12">Loading...</div></Layout>
  if (!handoff) return <Layout><div className="text-center py-12">Handoff not found</div></Layout>

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Handoff Details</h1>
            <p className="text-gray-600 mt-1">Patient: {handoff.patient_name || `ID ${handoff.patient_id}`}</p>
          </div>
          <span className={`px-4 py-2 rounded-full text-sm font-medium ${
            handoff.status === 'submitted' ? 'bg-green-100 text-green-800' :
            handoff.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
            'bg-gray-100 text-gray-800'
          }`}>
            {handoff.status.toUpperCase()}
          </span>
        </div>

        {/* Metadata */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div><span className="text-gray-600">Created by:</span> <span className="font-medium">{handoff.created_by_name}</span></div>
            <div><span className="text-gray-600">Priority:</span> <span className="font-medium capitalize">{handoff.priority}</span></div>
            <div><span className="text-gray-600">Shift:</span> <span className="font-medium capitalize">{handoff.shift || 'Not specified'}</span></div>
            <div><span className="text-gray-600">Created:</span> <span className="font-medium">{new Date(handoff.created_at).toLocaleString()}</span></div>
          </div>
        </div>

        {/* SBAR Report */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">SBAR Report</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium text-peacock-teal-700 mb-2">S - Situation</h3>
              <p className="text-gray-700">{handoff.sbar_situation || 'Not provided'}</p>
            </div>
            <div>
              <h3 className="font-medium text-peacock-teal-700 mb-2">B - Background</h3>
              <p className="text-gray-700">{handoff.sbar_background || 'Not provided'}</p>
            </div>
            <div>
              <h3 className="font-medium text-peacock-teal-700 mb-2">A - Assessment</h3>
              <p className="text-gray-700">{handoff.sbar_assessment || 'Not provided'}</p>
            </div>
            <div>
              <h3 className="font-medium text-peacock-teal-700 mb-2">R - Recommendation</h3>
              <p className="text-gray-700">{handoff.sbar_recommendation || 'Not provided'}</p>
            </div>
          </div>
        </div>

        {/* Actions */}
        {handoff.status === 'draft' && (
          <div className="flex gap-4">
            <button onClick={handleSubmit} className="flex-1 px-6 py-3 bg-peacock-teal-500 text-white rounded-lg hover:bg-peacock-teal-600 transition">
              Submit Handoff
            </button>
            <button onClick={() => navigate('/dashboard')} className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition">
              Back to Dashboard
            </button>
          </div>
        )}
      </div>
    </Layout>
  )
}
