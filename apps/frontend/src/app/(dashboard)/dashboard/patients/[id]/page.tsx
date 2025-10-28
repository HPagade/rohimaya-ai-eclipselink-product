'use client';

import { useQuery } from '@tanstack/react-query';
import { useRouter, useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { api } from '@/lib/api-client';
import { ArrowLeft, User, FileText, Loader2, Plus } from 'lucide-react';

export default function PatientDetailPage() {
  const router = useRouter();
  const params = useParams();
  const patientId = params.id as string;

  const { data: patient, isLoading: patientLoading } = useQuery({
    queryKey: ['patient', patientId],
    queryFn: () => api.getPatient(patientId),
    enabled: !!patientId,
  });

  const { data: handoffs, isLoading: handoffsLoading } = useQuery({
    queryKey: ['patient-handoffs', patientId],
    queryFn: () => api.getPatientHandoffs(patientId),
    enabled: !!patientId,
  });

  if (patientLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Patient not found</p>
        <Button className="mt-4" onClick={() => router.push('/dashboard/patients')}>
          Back to Patients
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" onClick={() => router.back()}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {patient.firstName} {patient.lastName}
            </h1>
            <p className="text-gray-500 mt-1">
              MRN: {patient.mrn}
            </p>
          </div>
        </div>
        <Button
          onClick={() => router.push(`/dashboard/handoffs/create?patientId=${patientId}`)}
        >
          <Plus className="w-4 h-4 mr-2" />
          New Handoff
        </Button>
      </div>

      {/* Patient Information */}
      <Card>
        <CardHeader>
          <CardTitle>Patient Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-sm text-gray-600">Full Name</div>
              <div className="font-medium mt-1">
                {patient.firstName} {patient.lastName}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">MRN</div>
              <div className="font-medium mt-1">{patient.mrn}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Date of Birth</div>
              <div className="font-medium mt-1">
                {new Date(patient.dateOfBirth).toLocaleDateString()}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Age</div>
              <div className="font-medium mt-1">
                {Math.floor((Date.now() - new Date(patient.dateOfBirth).getTime()) / (1000 * 60 * 60 * 24 * 365))} years
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Gender</div>
              <div className="font-medium mt-1 capitalize">{patient.gender}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Blood Type</div>
              <div className="font-medium mt-1">{patient.bloodType || 'Unknown'}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Status</div>
              <div className={`inline-flex px-2 py-1 rounded-full text-xs font-semibold mt-1 ${
                patient.status === 'active'
                  ? 'bg-green-100 text-green-800'
                  : patient.status === 'discharged'
                  ? 'bg-gray-100 text-gray-800'
                  : 'bg-blue-100 text-blue-800'
              }`}>
                {patient.status}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Primary Language</div>
              <div className="font-medium mt-1">{patient.primaryLanguage || 'English'}</div>
            </div>
          </div>

          {patient.allergies && patient.allergies.length > 0 && (
            <div className="mt-6">
              <div className="text-sm text-gray-600 mb-2">Allergies</div>
              <div className="flex flex-wrap gap-2">
                {patient.allergies.map((allergy: string, index: number) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm font-medium"
                  >
                    {allergy}
                  </span>
                ))}
              </div>
            </div>
          )}

          {patient.medicalHistory && (
            <div className="mt-6">
              <div className="text-sm text-gray-600 mb-2">Medical History</div>
              <p className="text-gray-700">{patient.medicalHistory}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Handoff History */}
      <Card>
        <CardHeader>
          <CardTitle>Handoff History</CardTitle>
          <CardDescription>
            All clinical handoffs for this patient
          </CardDescription>
        </CardHeader>
        <CardContent>
          {handoffsLoading ? (
            <div className="text-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-primary mx-auto" />
            </div>
          ) : handoffs && handoffs.length > 0 ? (
            <div className="space-y-3">
              {handoffs.map((handoff: any) => (
                <div
                  key={handoff.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
                  onClick={() => router.push(`/dashboard/handoffs/${handoff.id}`)}
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <FileText className="w-5 h-5 text-gray-400" />
                      <div>
                        <div className="font-medium text-gray-900">
                          {handoff.handoffType?.replace('_', ' ').toUpperCase()}
                          {handoff.isInitialHandoff && (
                            <span className="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                              Initial
                            </span>
                          )}
                        </div>
                        <div className="text-sm text-gray-500 mt-1">
                          {new Date(handoff.createdAt).toLocaleString()} • Priority: {handoff.priority}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        handoff.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : handoff.status === 'ready'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {handoff.status}
                    </span>
                    <Button variant="ghost" size="sm">
                      View SBAR
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No handoffs yet</p>
              <Button
                className="mt-4"
                onClick={() => router.push(`/dashboard/handoffs/create?patientId=${patientId}`)}
              >
                Create First Handoff
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
