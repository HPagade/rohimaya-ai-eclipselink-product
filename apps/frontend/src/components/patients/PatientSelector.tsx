import { useState, useEffect } from 'react'
import { User } from 'lucide-react'

interface Patient {
  id: number
  mrn: string
  first_name: string
  last_name: string
  date_of_birth: string
  room_number: string
  primary_diagnosis: string
  admission_date: string
  has_baseline: boolean
}

interface PatientSelectorProps {
  onSelectPatient: (patient: Patient, isBaseline: boolean) => void
}

export default function PatientSelector({ onSelectPatient }: PatientSelectorProps) {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null)

  useEffect(() => {
    fetchPatients()
  }, [])

  const fetchPatients = async () => {
    try {
      // TODO: Replace with real API call when backend is ready
      // const response = await fetch(`${import.meta.env.VITE_API_URL}/api/patients?status=active`)
      // const data = await response.json()

      // Mock data for now
      await new Promise(resolve => setTimeout(resolve, 800))
      const mockPatients: Patient[] = [
        {
          id: 1,
          mrn: 'MRN-10234',
          first_name: 'Sarah',
          last_name: 'Johnson',
          date_of_birth: '1958-03-15',
          room_number: '302',
          primary_diagnosis: 'Community-acquired pneumonia',
          admission_date: '2025-10-26',
          has_baseline: false
        },
        {
          id: 2,
          mrn: 'MRN-10235',
          first_name: 'Michael',
          last_name: 'Chen',
          date_of_birth: '1945-07-22',
          room_number: '315',
          primary_diagnosis: 'Post-operative hip replacement',
          admission_date: '2025-10-25',
          has_baseline: true
        },
        {
          id: 3,
          mrn: 'MRN-10236',
          first_name: 'Elizabeth',
          last_name: 'Martinez',
          date_of_birth: '1962-11-08',
          room_number: '218',
          primary_diagnosis: 'CHF exacerbation',
          admission_date: '2025-10-24',
          has_baseline: true
        },
        {
          id: 4,
          mrn: 'MRN-10237',
          first_name: 'Robert',
          last_name: 'Williams',
          date_of_birth: '1970-05-30',
          room_number: '421',
          primary_diagnosis: 'Diabetic ketoacidosis',
          admission_date: '2025-10-27',
          has_baseline: false
        }
      ]

      setPatients(mockPatients)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching patients:', error)
      setLoading(false)
    }
  }

  const calculateAge = (dob: string) => {
    const birthDate = new Date(dob)
    const today = new Date()
    let age = today.getFullYear() - birthDate.getFullYear()
    const monthDiff = today.getMonth() - birthDate.getMonth()
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--
    }
    return age
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  const handleSelectPatient = (patient: Patient) => {
    setSelectedPatientId(patient.id)
    // If patient has baseline, this is an update. Otherwise, it's a baseline.
    const isBaseline = !patient.has_baseline
    onSelectPatient(patient, isBaseline)
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-large p-8">
        <div className="text-center text-gray-500">Loading patients...</div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-large p-8">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-lunar-blue-500 mb-2">
          Select Patient
        </h2>
        <p className="text-gray-600">
          Choose the patient for this handoff
        </p>
      </div>

      <div className="space-y-4">
        {patients.map((patient) => (
          <button
            key={patient.id}
            onClick={() => handleSelectPatient(patient)}
            className={`w-full text-left p-6 rounded-lg border-2 transition-all ${
              selectedPatientId === patient.id
                ? 'border-peacock-teal-500 bg-peacock-teal-50'
                : 'border-gray-200 hover:border-peacock-teal-300 hover:bg-gray-50'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4">
                <div className="bg-lunar-blue-100 p-3 rounded-full">
                  <User className="w-6 h-6 text-lunar-blue-500" />
                </div>

                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-semibold text-lunar-blue-500">
                      {patient.first_name} {patient.last_name}
                    </h3>
                    <span className="text-sm text-gray-500">
                      {calculateAge(patient.date_of_birth)}yo
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-x-6 gap-y-1 text-sm">
                    <div>
                      <span className="text-gray-500">MRN:</span>{' '}
                      <span className="text-gray-700 font-medium">{patient.mrn}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Room:</span>{' '}
                      <span className="text-gray-700 font-medium">{patient.room_number}</span>
                    </div>
                    <div className="col-span-2">
                      <span className="text-gray-500">Diagnosis:</span>{' '}
                      <span className="text-gray-700">{patient.primary_diagnosis}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Admitted:</span>{' '}
                      <span className="text-gray-700">{formatDate(patient.admission_date)}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                {patient.has_baseline ? (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                    Update (5 pts)
                  </span>
                ) : (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-peacock-teal-100 text-peacock-teal-800">
                    Baseline (10 pts)
                  </span>
                )}
              </div>
            </div>
          </button>
        ))}
      </div>

      {patients.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No active patients found
        </div>
      )}
    </div>
  )
}
