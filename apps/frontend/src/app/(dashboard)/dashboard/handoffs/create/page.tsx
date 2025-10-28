'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { VoiceRecorder } from '@/components/handoffs/voice-recorder';
import { useToast } from '@/hooks/use-toast';
import { api } from '@/lib/api-client';
import { ArrowLeft, Upload, Loader2 } from 'lucide-react';

export default function CreateHandoffPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { toast } = useToast();

  const [step, setStep] = useState(1); // 1: Basic Info, 2: Voice Recording, 3: Processing
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Pre-fill from URL params
  useEffect(() => {
    const patientIdParam = searchParams.get('patientId');
    if (patientIdParam) {
      setPatientId(patientIdParam);
    }
  }, [searchParams]);

  // Form state
  const [patientId, setPatientId] = useState('');
  const [toStaffId, setToStaffId] = useState('');
  const [handoffType, setHandoffType] = useState('shift_change');
  const [priority, setPriority] = useState('routine');
  const [isInitialHandoff, setIsInitialHandoff] = useState(false);
  const [previousHandoffId, setPreviousHandoffId] = useState('');

  // Recording state
  const [recordingBlob, setRecordingBlob] = useState<Blob | null>(null);
  const [recordingDuration, setRecordingDuration] = useState(0);

  // Processing state
  const [handoffId, setHandoffId] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [processingStatus, setProcessingStatus] = useState('');

  const handleBasicInfoSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!patientId || !toStaffId) {
      toast({
        title: 'Validation Error',
        description: 'Please fill in all required fields',
        variant: 'destructive',
      });
      return;
    }

    try {
      // Create handoff
      const handoff = await api.createHandoff({
        patientId,
        toStaffId,
        handoffType,
        priority,
        status: 'draft',
        isInitialHandoff,
        previousHandoffId: previousHandoffId || null,
      });

      setHandoffId(handoff.id);
      setStep(2);

      toast({
        title: 'Handoff Created',
        description: 'Now record your handoff details',
      });
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.response?.data?.error?.message || 'Failed to create handoff',
        variant: 'destructive',
      });
    }
  };

  const handleRecordingComplete = (blob: Blob, duration: number) => {
    setRecordingBlob(blob);
    setRecordingDuration(duration);
  };

  const handleUploadRecording = async () => {
    if (!recordingBlob || !handoffId) return;

    setIsSubmitting(true);
    setStep(3);

    try {
      // Upload voice recording
      setProcessingStatus('Uploading voice recording...');
      const voiceRecording = await api.uploadVoiceRecording(
        handoffId,
        recordingBlob,
        recordingDuration,
        (progress) => setUploadProgress(progress)
      );

      // Poll for transcription and SBAR generation
      setProcessingStatus('Transcribing audio...');
      const finalStatus = await api.pollVoiceStatus(
        voiceRecording.id,
        (status) => {
          if (status.status === 'processing') {
            setProcessingStatus('Generating SBAR report...');
          }
        }
      );

      if (finalStatus.status === 'transcribed') {
        toast({
          title: 'Success!',
          description: 'Handoff created and SBAR report generated',
        });
        router.push(`/dashboard/handoffs/${handoffId}`);
      } else {
        throw new Error('Voice processing failed');
      }
    } catch (error: any) {
      setIsSubmitting(false);
      toast({
        title: 'Processing Error',
        description: error.message || 'Failed to process voice recording',
        variant: 'destructive',
      });
      setStep(2); // Go back to recording step
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Button
          variant="ghost"
          onClick={() => router.back()}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Create New Handoff</h1>
          <p className="text-gray-500 mt-1">
            Step {step} of 3: {step === 1 ? 'Basic Information' : step === 2 ? 'Voice Recording' : 'Processing'}
          </p>
        </div>
      </div>

      {/* Step 1: Basic Information */}
      {step === 1 && (
        <Card>
          <CardHeader>
            <CardTitle>Handoff Details</CardTitle>
            <CardDescription>
              Enter the basic information for this clinical handoff
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleBasicInfoSubmit} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="patientId" className="text-sm font-medium">
                  Patient ID <span className="text-red-500">*</span>
                </label>
                <Input
                  id="patientId"
                  placeholder="e.g., P123456"
                  value={patientId}
                  onChange={(e) => setPatientId(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="toStaffId" className="text-sm font-medium">
                  Receiving Staff ID <span className="text-red-500">*</span>
                </label>
                <Input
                  id="toStaffId"
                  placeholder="e.g., S789012"
                  value={toStaffId}
                  onChange={(e) => setToStaffId(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="handoffType" className="text-sm font-medium">
                  Handoff Type
                </label>
                <select
                  id="handoffType"
                  value={handoffType}
                  onChange={(e) => setHandoffType(e.target.value)}
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                >
                  <option value="shift_change">Shift Change</option>
                  <option value="transfer">Transfer</option>
                  <option value="admission">Admission</option>
                  <option value="discharge">Discharge</option>
                  <option value="procedure">Procedure</option>
                </select>
              </div>

              <div className="space-y-2">
                <label htmlFor="priority" className="text-sm font-medium">
                  Priority
                </label>
                <select
                  id="priority"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                >
                  <option value="routine">Routine</option>
                  <option value="urgent">Urgent</option>
                  <option value="emergent">Emergent</option>
                </select>
              </div>

              {/* Initial Handoff Toggle */}
              <div className="flex items-center space-x-2 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <input
                  type="checkbox"
                  id="isInitialHandoff"
                  checked={isInitialHandoff}
                  onChange={(e) => {
                    setIsInitialHandoff(e.target.checked);
                    if (e.target.checked) {
                      setPreviousHandoffId(''); // Clear previous handoff if initial
                    }
                  }}
                  className="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary"
                />
                <label htmlFor="isInitialHandoff" className="text-sm font-medium text-blue-900 cursor-pointer">
                  This is an <strong>initial handoff</strong> (patient admission)
                </label>
              </div>

              {/* Previous Handoff ID (only if not initial) */}
              {!isInitialHandoff && (
                <div className="space-y-2">
                  <label htmlFor="previousHandoffId" className="text-sm font-medium">
                    Previous Handoff ID (for update handoffs)
                  </label>
                  <Input
                    id="previousHandoffId"
                    placeholder="e.g., h12345678-abcd-..."
                    value={previousHandoffId}
                    onChange={(e) => setPreviousHandoffId(e.target.value)}
                  />
                  <p className="text-xs text-gray-500">
                    Leave empty if this is a shift change without a specific previous handoff to reference
                  </p>
                </div>
              )}

              <Button type="submit" className="w-full">
                Continue to Recording
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Step 2: Voice Recording */}
      {step === 2 && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Record Handoff</CardTitle>
              <CardDescription>
                Record your clinical handoff using the SBAR format
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-900 mb-2">
                    {isInitialHandoff ? 'Initial Handoff - SBAR Format:' : 'Update Handoff - SBAR Format:'}
                  </h3>
                  {isInitialHandoff ? (
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li><strong>S</strong>ituation - Current patient status, chief complaint, vital signs</li>
                      <li><strong>B</strong>ackground - Complete medical history, medications, allergies, admission reason</li>
                      <li><strong>A</strong>ssessment - Clinical assessment, lab results, current trends</li>
                      <li><strong>R</strong>ecommendation - Full care plan, pending tasks, follow-ups</li>
                      <li className="mt-2 text-xs italic">Record 5-10 minutes covering complete patient history</li>
                    </ul>
                  ) : (
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li><strong>S</strong>ituation - What changed since last handoff?</li>
                      <li><strong>B</strong>ackground - Any new medications, allergies, or updates?</li>
                      <li><strong>A</strong>ssessment - New findings, changes in condition?</li>
                      <li><strong>R</strong>ecommendation - Updated care plan, new pending tasks?</li>
                      <li className="mt-2 text-xs italic">Record 1-3 minutes focusing only on changes</li>
                    </ul>
                  )}
                </div>

                <VoiceRecorder
                  onRecordingComplete={handleRecordingComplete}
                  maxDuration={600}
                />

                {recordingBlob && (
                  <Button
                    onClick={handleUploadRecording}
                    disabled={isSubmitting}
                    className="w-full"
                    size="lg"
                  >
                    <Upload className="w-5 h-5 mr-2" />
                    Upload and Process Recording
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Step 3: Processing */}
      {step === 3 && (
        <Card>
          <CardHeader>
            <CardTitle>Processing Handoff</CardTitle>
            <CardDescription>
              Please wait while we process your recording...
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6 py-8">
              <div className="flex flex-col items-center space-y-4">
                <Loader2 className="w-12 h-12 text-primary animate-spin" />
                <div className="text-center">
                  <div className="text-lg font-semibold">{processingStatus}</div>
                  {uploadProgress > 0 && uploadProgress < 100 && (
                    <div className="mt-2">
                      <div className="w-64 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary transition-all duration-300"
                          style={{ width: `${uploadProgress}%` }}
                        />
                      </div>
                      <div className="text-sm text-gray-500 mt-1">
                        {uploadProgress}% uploaded
                      </div>
                    </div>
                  )}
                </div>
              </div>

              <div className="text-center text-sm text-gray-500">
                <p>This may take a few moments.</p>
                <p>We're transcribing your voice and generating the SBAR report.</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
