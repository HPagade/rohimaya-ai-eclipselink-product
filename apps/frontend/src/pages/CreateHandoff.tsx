import { useState } from 'react'
import { ArrowLeft, Loader2, CheckCircle2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

import PatientSelector from '@/components/patients/PatientSelector'
import VoiceRecorder from '@/components/handoffs/VoiceRecorder'
import SBARDisplay from '@/components/handoffs/SBARDisplay'
import { uploadHandoff, type HandoffResponse } from '@/services/handoffApi'

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

type Step = 'select_patient' | 'record_voice' | 'processing' | 'complete'

interface ProcessingStatus {
  step: string
  message: string
  completed: boolean
}

export default function CreateHandoff() {
  const navigate = useNavigate()

  // Multi-step state
  const [currentStep, setCurrentStep] = useState<Step>('select_patient')
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null)
  const [isBaseline, setIsBaseline] = useState(true)

  // Recording state
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [audioDuration, setAudioDuration] = useState(0)

  // Processing state
  const [processingStatuses, setProcessingStatuses] = useState<ProcessingStatus[]>([])
  const [isProcessing, setIsProcessing] = useState(false)

  // Result state
  const [handoffResult, setHandoffResult] = useState<HandoffResponse | null>(null)

  // Hardcoded user ID for now (will come from auth store later)
  const userId = 1

  const handlePatientSelect = (patient: Patient, baseline: boolean) => {
    setSelectedPatient(patient)
    setIsBaseline(baseline)
    setCurrentStep('record_voice')
  }

  const handleBackToPatients = () => {
    setCurrentStep('select_patient')
    setSelectedPatient(null)
  }

  const handleRecordingComplete = async (blob: Blob, duration: number) => {
    if (!selectedPatient) return

    setAudioBlob(blob)
    setAudioDuration(duration)
    setCurrentStep('processing')
    setIsProcessing(true)

    // Initialize processing statuses
    const statuses: ProcessingStatus[] = [
      { step: 'upload', message: 'Uploading voice recording...', completed: false },
      { step: 'transcribe', message: 'Transcribing audio with AI...', completed: false },
      { step: 'sbar', message: 'Generating SBAR documentation...', completed: false },
      { step: 'alerts', message: 'Checking for critical alerts...', completed: false },
      { step: 'save', message: 'Saving handoff to database...', completed: false },
    ]
    setProcessingStatuses(statuses)

    try {
      // Simulate step-by-step progress (in real world, backend would send progress updates)
      const updateProgress = (stepIndex: number) => {
        setProcessingStatuses(prev =>
          prev.map((status, index) =>
            index === stepIndex ? { ...status, completed: true } : status
          )
        )
      }

      // Start upload
      updateProgress(0)

      // Call the actual API
      const result = await uploadHandoff({
        patient_id: selectedPatient.id,
        is_baseline: isBaseline,
        user_id: userId,
        audio_file: blob,
      })

      // Mark all steps as complete when we get the response
      updateProgress(1)
      await new Promise(resolve => setTimeout(resolve, 500))
      updateProgress(2)
      await new Promise(resolve => setTimeout(resolve, 500))
      updateProgress(3)
      await new Promise(resolve => setTimeout(resolve, 500))
      updateProgress(4)
      await new Promise(resolve => setTimeout(resolve, 500))

      setHandoffResult(result)
      setIsProcessing(false)
      setCurrentStep('complete')

      toast.success(`${isBaseline ? 'Baseline' : 'Update'} handoff completed! +${result.points_earned} points`)

    } catch (error) {
      console.error('Error uploading handoff:', error)
      setIsProcessing(false)
      toast.error('Failed to process handoff. Please try again.')
      setCurrentStep('record_voice') // Go back to recording
    }
  }

  const handleCreateAnother = () => {
    // Reset all state
    setCurrentStep('select_patient')
    setSelectedPatient(null)
    setIsBaseline(true)
    setAudioBlob(null)
    setAudioDuration(0)
    setProcessingStatuses([])
    setHandoffResult(null)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center space-x-2 text-lunar-blue-500 hover:text-lunar-blue-600 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Dashboard</span>
          </button>

          <h1 className="text-4xl font-bold text-lunar-blue-500 mb-2">
            Create Handoff
          </h1>
          <p className="text-gray-600">
            Record a voice handoff and let AI generate your SBAR documentation
          </p>
        </div>

        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex items-center justify-between max-w-2xl mx-auto">
            <StepIndicator
              number={1}
              label="Select Patient"
              active={currentStep === 'select_patient'}
              completed={currentStep !== 'select_patient'}
            />
            <div className={`flex-1 h-1 mx-4 ${
              currentStep === 'select_patient' ? 'bg-gray-300' : 'bg-peacock-teal-500'
            }`} />
            <StepIndicator
              number={2}
              label="Record Voice"
              active={currentStep === 'record_voice'}
              completed={currentStep === 'processing' || currentStep === 'complete'}
            />
            <div className={`flex-1 h-1 mx-4 ${
              currentStep === 'select_patient' || currentStep === 'record_voice'
                ? 'bg-gray-300'
                : 'bg-peacock-teal-500'
            }`} />
            <StepIndicator
              number={3}
              label="Review SBAR"
              active={currentStep === 'complete'}
              completed={currentStep === 'complete'}
            />
          </div>
        </div>

        {/* Step Content */}
        {currentStep === 'select_patient' && (
          <PatientSelector onSelectPatient={handlePatientSelect} />
        )}

        {currentStep === 'record_voice' && selectedPatient && (
          <div>
            {/* Patient Info Bar */}
            <div className="bg-peacock-teal-50 border border-peacock-teal-200 rounded-xl p-4 mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm text-peacock-teal-600 mb-1">Recording for:</div>
                  <div className="text-lg font-semibold text-lunar-blue-500">
                    {selectedPatient.first_name} {selectedPatient.last_name}
                  </div>
                  <div className="text-sm text-gray-600">
                    {selectedPatient.mrn} • Room {selectedPatient.room_number}
                  </div>
                </div>
                <div>
                  {isBaseline ? (
                    <span className="px-4 py-2 bg-peacock-teal-500 text-white rounded-full text-sm font-medium">
                      Baseline Handoff
                    </span>
                  ) : (
                    <span className="px-4 py-2 bg-amber-500 text-white rounded-full text-sm font-medium">
                      Update Handoff
                    </span>
                  )}
                </div>
              </div>
              <button
                onClick={handleBackToPatients}
                className="text-sm text-peacock-teal-700 hover:text-peacock-teal-800 mt-2"
              >
                Change patient
              </button>
            </div>

            <VoiceRecorder
              onRecordingComplete={handleRecordingComplete}
              maxDuration={300}
            />
          </div>
        )}

        {currentStep === 'processing' && (
          <div className="bg-white rounded-xl shadow-large p-12">
            <div className="max-w-md mx-auto text-center">
              <div className="mb-6">
                <Loader2 className="w-16 h-16 text-peacock-teal-500 animate-spin mx-auto" />
              </div>
              <h2 className="text-2xl font-semibold text-lunar-blue-500 mb-2">
                Processing Your Handoff
              </h2>
              <p className="text-gray-600 mb-8">
                Our AI is analyzing your voice recording and generating the SBAR documentation
              </p>

              {/* Processing Steps */}
              <div className="space-y-4 text-left">
                {processingStatuses.map((status, index) => (
                  <div
                    key={status.step}
                    className="flex items-center space-x-3"
                  >
                    {status.completed ? (
                      <CheckCircle2 className="w-6 h-6 text-green-500 flex-shrink-0" />
                    ) : (
                      <div className={`w-6 h-6 rounded-full border-2 flex-shrink-0 ${
                        isProcessing && !processingStatuses[index - 1]?.completed && index > 0
                          ? 'border-gray-300'
                          : 'border-peacock-teal-500 border-t-transparent animate-spin'
                      }`} />
                    )}
                    <span className={`text-sm ${
                      status.completed ? 'text-gray-500' : 'text-gray-700 font-medium'
                    }`}>
                      {status.message}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {currentStep === 'complete' && handoffResult && selectedPatient && (
          <div>
            <SBARDisplay
              sbar={handoffResult.sbar || {
                situation: '',
                background: '',
                assessment: '',
                recommendation: ''
              }}
              transcript={handoffResult.transcript_text || ''}
              transcriptConfidence={handoffResult.transcript_confidence || 0}
              pointsEarned={handoffResult.points_earned}
              criticalAlert={handoffResult.critical_alert}
              isBaseline={isBaseline}
              patientName={`${selectedPatient.first_name} ${selectedPatient.last_name}`}
            />

            {/* Action Buttons */}
            <div className="mt-8 flex justify-center space-x-4">
              <button
                onClick={handleCreateAnother}
                className="px-6 py-3 bg-peacock-teal-500 hover:bg-peacock-teal-600 text-white rounded-lg font-medium transition"
              >
                Create Another Handoff
              </button>
              <button
                onClick={() => navigate('/dashboard')}
                className="px-6 py-3 border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-lg font-medium transition"
              >
                Return to Dashboard
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Helper component for step indicator
function StepIndicator({ number, label, active, completed }: {
  number: number
  label: string
  active: boolean
  completed: boolean
}) {
  return (
    <div className="flex flex-col items-center">
      <div className={`w-12 h-12 rounded-full flex items-center justify-center font-semibold mb-2 ${
        completed
          ? 'bg-peacock-teal-500 text-white'
          : active
          ? 'bg-peacock-teal-100 text-peacock-teal-700 border-2 border-peacock-teal-500'
          : 'bg-gray-200 text-gray-500'
      }`}>
        {completed ? <CheckCircle2 className="w-6 h-6" /> : number}
      </div>
      <div className={`text-sm font-medium ${
        active ? 'text-lunar-blue-500' : 'text-gray-500'
      }`}>
        {label}
      </div>
    </div>
  )
}
