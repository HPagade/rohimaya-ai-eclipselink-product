import { useState, useRef, useEffect } from 'react'
import { Mic, Square, Play, Pause } from 'lucide-react'

interface VoiceRecorderProps {
  onRecordingComplete: (audioBlob: Blob, duration: number) => void
  maxDuration?: number // seconds
}

export default function VoiceRecorder({ onRecordingComplete, maxDuration = 300 }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [duration, setDuration] = useState(0)
  const [audioLevel, setAudioLevel] = useState(0)

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const timerRef = useRef<NodeJS.Timeout | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
      if (audioContextRef.current) audioContextRef.current.close()
    }
  }, [])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

      // Setup audio visualization
      const audioContext = new AudioContext()
      const source = audioContext.createMediaStreamSource(stream)
      const analyser = audioContext.createAnalyser()
      analyser.fftSize = 256
      source.connect(analyser)

      audioContextRef.current = audioContext
      analyserRef.current = analyser

      // Visualize audio level
      const dataArray = new Uint8Array(analyser.frequencyBinCount)
      const updateLevel = () => {
        if (analyser && isRecording) {
          analyser.getByteFrequencyData(dataArray)
          const average = dataArray.reduce((a, b) => a + b) / dataArray.length
          setAudioLevel(average / 255) // Normalize to 0-1
          requestAnimationFrame(updateLevel)
        }
      }
      updateLevel()

      // Setup MediaRecorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })

      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        onRecordingComplete(audioBlob, duration)

        // Cleanup
        stream.getTracks().forEach(track => track.stop())
        if (audioContextRef.current) {
          audioContextRef.current.close()
          audioContextRef.current = null
        }
      }

      mediaRecorder.start()
      setIsRecording(true)
      setDuration(0)

      // Start timer
      timerRef.current = setInterval(() => {
        setDuration(prev => {
          const newDuration = prev + 1
          if (newDuration >= maxDuration) {
            stopRecording()
          }
          return newDuration
        })
      }, 1000)

    } catch (error) {
      console.error('Error accessing microphone:', error)
      alert('Unable to access microphone. Please grant permission.')
    }
  }

  const pauseRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.pause()
      setIsPaused(true)
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }

  const resumeRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'paused') {
      mediaRecorderRef.current.resume()
      setIsPaused(false)

      // Resume timer
      timerRef.current = setInterval(() => {
        setDuration(prev => {
          const newDuration = prev + 1
          if (newDuration >= maxDuration) {
            stopRecording()
          }
          return newDuration
        })
      }, 1000)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      setIsPaused(false)
      setAudioLevel(0)
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="bg-white rounded-xl shadow-large p-8 space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-semibold text-lunar-blue-500 mb-2">
          {isRecording ? 'Recording Handoff...' : 'Ready to Record'}
        </h2>
        <p className="text-gray-600">
          {isRecording
            ? 'Speak clearly about the patient\'s condition and care plan'
            : 'Click the microphone to start recording your handoff'}
        </p>
      </div>

      {/* Waveform Visualization */}
      <div className="bg-gray-50 rounded-lg p-6 h-32 flex items-center justify-center">
        <div className="flex items-end space-x-1 h-full">
          {[...Array(40)].map((_, i) => (
            <div
              key={i}
              className="bg-peacock-teal-500 rounded-t transition-all duration-100"
              style={{
                width: '4px',
                height: isRecording
                  ? `${Math.max(10, audioLevel * 100 * (0.5 + Math.random() * 0.5))}%`
                  : '10%',
                opacity: isRecording ? 0.8 : 0.3
              }}
            />
          ))}
        </div>
      </div>

      {/* Timer */}
      <div className="text-center">
        <div className="text-5xl font-mono font-bold text-lunar-blue-500">
          {formatTime(duration)}
        </div>
        <div className="text-sm text-gray-500 mt-1">
          Max: {formatTime(maxDuration)}
        </div>
      </div>

      {/* Controls */}
      <div className="flex justify-center space-x-4">
        {!isRecording ? (
          <button
            onClick={startRecording}
            className="flex items-center space-x-2 bg-peacock-teal-500 hover:bg-peacock-teal-600 text-white px-8 py-4 rounded-full font-medium transition shadow-lg"
          >
            <Mic className="w-6 h-6" />
            <span>Start Recording</span>
          </button>
        ) : (
          <>
            {!isPaused ? (
              <button
                onClick={pauseRecording}
                className="flex items-center space-x-2 bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-full font-medium transition"
              >
                <Pause className="w-5 h-5" />
                <span>Pause</span>
              </button>
            ) : (
              <button
                onClick={resumeRecording}
                className="flex items-center space-x-2 bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-full font-medium transition"
              >
                <Play className="w-5 h-5" />
                <span>Resume</span>
              </button>
            )}

            <button
              onClick={stopRecording}
              className="flex items-center space-x-2 bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-full font-medium transition"
            >
              <Square className="w-5 h-5" />
              <span>Stop & Save</span>
            </button>
          </>
        )}
      </div>

      {/* Tips */}
      {!isRecording && (
        <div className="bg-peacock-teal-50 border border-peacock-teal-200 rounded-lg p-4">
          <p className="text-sm text-peacock-teal-800">
            <strong>Tips for a great handoff:</strong>
          </p>
          <ul className="text-sm text-peacock-teal-700 mt-2 space-y-1 list-disc list-inside">
            <li>Identify yourself and the patient</li>
            <li>State current condition and vital signs</li>
            <li>Mention medications and treatments</li>
            <li>Note any changes or concerns</li>
            <li>State the plan and next steps</li>
          </ul>
        </div>
      )}
    </div>
  )
}
