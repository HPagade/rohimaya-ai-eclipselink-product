import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import patientService, { Patient } from '@/services/patientService'
import handoffService from '@/services/handoffService'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

export default function VoiceRecorder() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatient, setSelectedPatient] = useState<number | ''>('')
  const [formData, setFormData] = useState({
    sbar_situation: '',
    sbar_background: '',
    sbar_assessment: '',
    sbar_recommendation: '',
    priority: 'normal',
    shift: ''
  })
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    loadPatients()
  }, [])

  const loadPatients = async () => {
    try {
      const result = await patientService.list({ page_size: 100 })
      setPatients(result.patients)
    } catch (error) {
      console.error('Error loading patients:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedPatient) {
      toast.error('Please select a patient')
      return
    }
    setLoading(true)
    try {
      const handoff = await handoffService.create({
        patient_id: Number(selectedPatient),
        ...formData
      })
      toast.success('Handoff created successfully!')
      navigate(`/handoff/${handoff.id}`)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create handoff')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Create New Handoff</h1>

        <div className="bg-white rounded-lg shadow p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Patient Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Select Patient *</label>
              <select required value={selectedPatient} onChange={e => setSelectedPatient(Number(e.target.value))} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-peacock-teal-500">
                <option value="">Choose a patient...</option>
                {patients.map(p => (
                  <option key={p.id} value={p.id}>{p.first_name} {p.last_name} - MRN: {p.mrn} - Room: {p.room_number || 'N/A'}</option>
                ))}
              </select>
            </div>

            {/* Priority and Shift */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select value={formData.priority} onChange={e => setFormData({...formData, priority: e.target.value})} className="w-full px-4 py-3 border border-gray-300 rounded-lg">
                  <option value="normal">Normal</option>
                  <option value="urgent">Urgent</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Shift</label>
                <select value={formData.shift} onChange={e => setFormData({...formData, shift: e.target.value})} className="w-full px-4 py-3 border border-gray-300 rounded-lg">
                  <option value="">Select shift...</option>
                  <option value="day">Day</option>
                  <option value="evening">Evening</option>
                  <option value="night">Night</option>
                </select>
              </div>
            </div>

            {/* SBAR Sections */}
            <div className="bg-peacock-teal-50 p-4 rounded-lg">
              <h3 className="font-semibold text-lg mb-4">SBAR Report</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">S - Situation</label>
                  <textarea placeholder="What is happening with the patient?" value={formData.sbar_situation} onChange={e => setFormData({...formData, sbar_situation: e.target.value})} rows={3} className="w-full px-4 py-3 border border-gray-300 rounded-lg" />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">B - Background</label>
                  <textarea placeholder="What is the clinical background?" value={formData.sbar_background} onChange={e => setFormData({...formData, sbar_background: e.target.value})} rows={3} className="w-full px-4 py-3 border border-gray-300 rounded-lg" />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">A - Assessment</label>
                  <textarea placeholder="What do you think the problem is?" value={formData.sbar_assessment} onChange={e => setFormData({...formData, sbar_assessment: e.target.value})} rows={3} className="w-full px-4 py-3 border border-gray-300 rounded-lg" />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">R - Recommendation</label>
                  <textarea placeholder="What should be done?" value={formData.sbar_recommendation} onChange={e => setFormData({...formData, sbar_recommendation: e.target.value})} rows={3} className="w-full px-4 py-3 border border-gray-300 rounded-lg" />
                </div>
              </div>
            </div>

            {/* Submit Buttons */}
            <div className="flex gap-4">
              <button type="submit" disabled={loading} className="flex-1 px-6 py-3 bg-peacock-teal-500 text-white rounded-lg hover:bg-peacock-teal-600 transition disabled:opacity-50">
                {loading ? 'Creating...' : 'Create Handoff'}
              </button>
              <button type="button" onClick={() => navigate('/dashboard')} className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition">
                Cancel
              </button>
            </div>
          </form>
        </div>

        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>💡 Pro Tip:</strong> Fill out the SBAR sections to create a structured handoff report. Voice recording with AI transcription coming soon!
          </p>
        </div>
      </div>
    </Layout>
  )
}
