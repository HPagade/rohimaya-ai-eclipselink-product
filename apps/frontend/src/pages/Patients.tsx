import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import patientService, { Patient } from '@/services/patientService'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'

export default function Patients() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    mrn: '',
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: '',
    room_number: '',
    primary_diagnosis: '',
    allergies: ''
  })

  useEffect(() => {
    loadPatients()
  }, [search])

  const loadPatients = async () => {
    try {
      const result = await patientService.list({ search, page_size: 50 })
      setPatients(result.patients)
    } catch (error) {
      console.error('Error loading patients:', error)
      toast.error('Failed to load patients')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await patientService.create(formData)
      toast.success('Patient created successfully!')
      setShowForm(false)
      setFormData({ mrn: '', first_name: '', last_name: '', date_of_birth: '', gender: '', room_number: '', primary_diagnosis: '', allergies: '' })
      loadPatients()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create patient')
    }
  }

  return (
    <Layout>
      <div>
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Patients</h1>
          <button onClick={() => setShowForm(!showForm)} className="px-4 py-2 bg-peacock-teal-500 text-white rounded-lg hover:bg-peacock-teal-600 transition">
            {showForm ? 'Cancel' : '+ Add Patient'}
          </button>
        </div>

        {showForm && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">New Patient</h2>
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input required placeholder="MRN" value={formData.mrn} onChange={e => setFormData({...formData, mrn: e.target.value})} className="px-4 py-2 border rounded-lg" />
              <input required placeholder="First Name" value={formData.first_name} onChange={e => setFormData({...formData, first_name: e.target.value})} className="px-4 py-2 border rounded-lg" />
              <input required placeholder="Last Name" value={formData.last_name} onChange={e => setFormData({...formData, last_name: e.target.value})} className="px-4 py-2 border rounded-lg" />
              <input required type="date" placeholder="Date of Birth" value={formData.date_of_birth} onChange={e => setFormData({...formData, date_of_birth: e.target.value})} className="px-4 py-2 border rounded-lg" />
              <input placeholder="Room Number" value={formData.room_number} onChange={e => setFormData({...formData, room_number: e.target.value})} className="px-4 py-2 border rounded-lg" />
              <input placeholder="Diagnosis" value={formData.primary_diagnosis} onChange={e => setFormData({...formData, primary_diagnosis: e.target.value})} className="px-4 py-2 border rounded-lg" />
              <input placeholder="Allergies" value={formData.allergies} onChange={e => setFormData({...formData, allergies: e.target.value})} className="px-4 py-2 border rounded-lg md:col-span-2" />
              <button type="submit" className="md:col-span-2 px-4 py-2 bg-peacock-teal-500 text-white rounded-lg hover:bg-peacock-teal-600 transition">Create Patient</button>
            </form>
          </div>
        )}

        <div className="bg-white rounded-lg shadow mb-6 p-4">
          <input type="search" placeholder="Search patients..." value={search} onChange={e => setSearch(e.target.value)} className="w-full px-4 py-2 border rounded-lg" />
        </div>

        <div className="bg-white rounded-lg shadow">
          {loading ? (
            <div className="p-8 text-center text-gray-500">Loading...</div>
          ) : patients.length === 0 ? (
            <div className="p-8 text-center text-gray-500">No patients found. Add your first patient!</div>
          ) : (
            <div className="divide-y divide-gray-200">
              {patients.map(patient => (
                <div key={patient.id} className="p-4 hover:bg-gray-50 transition">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-lg">{patient.first_name} {patient.last_name}</div>
                      <div className="text-sm text-gray-600">MRN: {patient.mrn} • Room: {patient.room_number || 'N/A'}</div>
                      {patient.primary_diagnosis && <div className="text-sm text-gray-600 mt-1">Diagnosis: {patient.primary_diagnosis}</div>}
                      {patient.allergies && <div className="text-sm text-red-600 mt-1">⚠️ Allergies: {patient.allergies}</div>}
                    </div>
                    <Link to={`/patients/${patient.id}`} className="text-peacock-teal-600 hover:text-peacock-teal-700">View →</Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}
