import { Award, AlertTriangle, FileText, Printer, Download } from 'lucide-react'

interface SBARData {
  situation: string
  background: string
  assessment: string
  recommendation: string
}

interface CriticalAlert {
  alert_type: string
  severity: string
  confidence: number
  message: string
  recommended_actions: string
}

interface SBARDisplayProps {
  sbar: SBARData
  transcript: string
  transcriptConfidence: number
  pointsEarned: number
  criticalAlert?: CriticalAlert
  isBaseline: boolean
  patientName: string
  processingTimeMs?: number
}

export default function SBARDisplay({
  sbar,
  transcript,
  transcriptConfidence,
  pointsEarned,
  criticalAlert,
  isBaseline,
  patientName,
  processingTimeMs
}: SBARDisplayProps) {

  const handlePrint = () => {
    window.print()
  }

  const handleExport = () => {
    // Create a text version of the SBAR
    const content = `
CLINICAL HANDOFF - ${patientName}
Generated: ${new Date().toLocaleString()}
Type: ${isBaseline ? 'Baseline Handoff' : 'Update Handoff'}

${criticalAlert ? `
⚠️ CRITICAL ALERT: ${criticalAlert.alert_type.replace('_', ' ').toUpperCase()}
Severity: ${criticalAlert.severity}
${criticalAlert.message}
Recommended Actions: ${criticalAlert.recommended_actions}
` : ''}

SITUATION:
${sbar.situation}

BACKGROUND:
${sbar.background}

ASSESSMENT:
${sbar.assessment}

RECOMMENDATION:
${sbar.recommendation}

---
ORIGINAL TRANSCRIPT (Confidence: ${(transcriptConfidence * 100).toFixed(0)}%):
${transcript}

---
Points Earned: ${pointsEarned}
Processing Time: ${processingTimeMs ? `${(processingTimeMs / 1000).toFixed(1)}s` : 'N/A'}
`.trim()

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `handoff-${patientName.replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      {/* Success Header with Points */}
      <div className="bg-gradient-to-r from-peacock-teal-500 to-peacock-teal-600 text-white rounded-xl shadow-large p-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold mb-2">
              {isBaseline ? 'Baseline Handoff Complete!' : 'Update Handoff Complete!'}
            </h2>
            <p className="text-peacock-teal-100 text-lg">
              SBAR generated successfully for {patientName}
            </p>
          </div>

          <div className="text-center">
            <div className="bg-white bg-opacity-20 rounded-full p-6 mb-2">
              <Award className="w-12 h-12" />
            </div>
            <div className="text-4xl font-bold">{pointsEarned}</div>
            <div className="text-peacock-teal-100 text-sm">points earned</div>
          </div>
        </div>
      </div>

      {/* Critical Alert Banner */}
      {criticalAlert && (
        <div className="bg-red-50 border-2 border-red-500 rounded-xl p-6">
          <div className="flex items-start space-x-4">
            <div className="bg-red-500 text-white p-3 rounded-full">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <h3 className="text-xl font-bold text-red-800">
                  Critical Alert: {criticalAlert.alert_type.replace(/_/g, ' ').toUpperCase()}
                </h3>
                <span className="px-3 py-1 bg-red-500 text-white text-xs font-semibold rounded-full">
                  {criticalAlert.severity.toUpperCase()}
                </span>
                <span className="text-sm text-red-600">
                  {(criticalAlert.confidence * 100).toFixed(0)}% confidence
                </span>
              </div>
              <p className="text-red-800 font-medium mb-3">
                {criticalAlert.message}
              </p>
              <div className="bg-red-100 border border-red-300 rounded-lg p-3">
                <p className="text-sm font-semibold text-red-900 mb-1">
                  Recommended Actions:
                </p>
                <p className="text-sm text-red-800">
                  {criticalAlert.recommended_actions}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-end space-x-3">
        <button
          onClick={handlePrint}
          className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
        >
          <Printer className="w-4 h-4" />
          <span>Print</span>
        </button>
        <button
          onClick={handleExport}
          className="flex items-center space-x-2 px-4 py-2 bg-lunar-blue-500 hover:bg-lunar-blue-600 text-white rounded-lg transition"
        >
          <Download className="w-4 h-4" />
          <span>Export</span>
        </button>
      </div>

      {/* SBAR Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Situation */}
        <div className="bg-white rounded-xl shadow-large p-6 border-l-4 border-peacock-teal-500">
          <div className="flex items-center space-x-2 mb-3">
            <div className="bg-peacock-teal-100 p-2 rounded">
              <FileText className="w-5 h-5 text-peacock-teal-600" />
            </div>
            <h3 className="text-xl font-semibold text-lunar-blue-500">Situation</h3>
          </div>
          <p className="text-gray-700 leading-relaxed">{sbar.situation}</p>
        </div>

        {/* Background */}
        <div className="bg-white rounded-xl shadow-large p-6 border-l-4 border-lunar-blue-400">
          <div className="flex items-center space-x-2 mb-3">
            <div className="bg-lunar-blue-100 p-2 rounded">
              <FileText className="w-5 h-5 text-lunar-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-lunar-blue-500">Background</h3>
          </div>
          <p className="text-gray-700 leading-relaxed">{sbar.background}</p>
        </div>

        {/* Assessment */}
        <div className="bg-white rounded-xl shadow-large p-6 border-l-4 border-amber-400">
          <div className="flex items-center space-x-2 mb-3">
            <div className="bg-amber-100 p-2 rounded">
              <FileText className="w-5 h-5 text-amber-600" />
            </div>
            <h3 className="text-xl font-semibold text-lunar-blue-500">Assessment</h3>
          </div>
          <p className="text-gray-700 leading-relaxed">{sbar.assessment}</p>
        </div>

        {/* Recommendation */}
        <div className="bg-white rounded-xl shadow-large p-6 border-l-4 border-phoenix-orange-500">
          <div className="flex items-center space-x-2 mb-3">
            <div className="bg-phoenix-orange-100 p-2 rounded">
              <FileText className="w-5 h-5 text-phoenix-orange-600" />
            </div>
            <h3 className="text-xl font-semibold text-lunar-blue-500">Recommendation</h3>
          </div>
          <p className="text-gray-700 leading-relaxed">{sbar.recommendation}</p>
        </div>
      </div>

      {/* Transcript Section */}
      <div className="bg-gray-50 rounded-xl shadow-large p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-lunar-blue-500">Original Transcript</h3>
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <span>
              Confidence: <strong>{(transcriptConfidence * 100).toFixed(0)}%</strong>
            </span>
            {processingTimeMs && (
              <span>
                Processing: <strong>{(processingTimeMs / 1000).toFixed(1)}s</strong>
              </span>
            )}
          </div>
        </div>
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {transcript}
          </p>
        </div>
      </div>
    </div>
  )
}
