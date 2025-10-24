'use client';

import { useQuery } from '@tanstack/react-query';
import { useRouter, useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { SBARViewer } from '@/components/sbar/sbar-viewer';
import { api } from '@/lib/api-client';
import { ArrowLeft, CheckCircle, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useState } from 'react';

export default function HandoffDetailPage() {
  const router = useRouter();
  const params = useParams();
  const { toast } = useToast();
  const handoffId = params.id as string;

  const [isCompleting, setIsCompleting] = useState(false);

  const { data: handoff, isLoading: handoffLoading, refetch: refetchHandoff } = useQuery({
    queryKey: ['handoff', handoffId],
    queryFn: () => api.getHandoff(handoffId),
    enabled: !!handoffId,
  });

  const { data: sbar, isLoading: sbarLoading, refetch: refetchSbar } = useQuery({
    queryKey: ['sbar', handoffId],
    queryFn: () => api.getSbar(handoffId),
    enabled: !!handoffId,
  });

  const handleCompleteHandoff = async () => {
    setIsCompleting(true);
    try {
      await api.completeHandoff(handoffId, 'Handoff completed successfully');
      toast({
        title: 'Handoff Completed',
        description: 'This handoff has been marked as complete',
      });
      refetchHandoff();
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.response?.data?.error?.message || 'Failed to complete handoff',
        variant: 'destructive',
      });
    } finally {
      setIsCompleting(false);
    }
  };

  if (handoffLoading || sbarLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!handoff) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Handoff not found</p>
        <Button className="mt-4" onClick={() => router.push('/dashboard')}>
          Back to Dashboard
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
            <h1 className="text-3xl font-bold text-gray-900">Handoff Details</h1>
            <p className="text-gray-500 mt-1">
              ID: {handoffId.substring(0, 8)}...
            </p>
          </div>
        </div>
        {handoff.status !== 'completed' && (
          <Button
            onClick={handleCompleteHandoff}
            disabled={isCompleting}
          >
            <CheckCircle className="w-4 h-4 mr-2" />
            {isCompleting ? 'Completing...' : 'Mark Complete'}
          </Button>
        )}
      </div>

      {/* Handoff Info */}
      <Card>
        <CardHeader>
          <CardTitle>Handoff Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-sm text-gray-600">Patient ID</div>
              <div className="font-medium mt-1">{handoff.patientId}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Type</div>
              <div className="font-medium mt-1 capitalize">
                {handoff.handoffType?.replace('_', ' ')}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Priority</div>
              <div className="font-medium mt-1 capitalize">{handoff.priority}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Status</div>
              <div className={`inline-flex px-2 py-1 rounded-full text-xs font-semibold mt-1 ${
                handoff.status === 'completed'
                  ? 'bg-green-100 text-green-800'
                  : handoff.status === 'assigned'
                  ? 'bg-blue-100 text-blue-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {handoff.status}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Created At</div>
              <div className="font-medium mt-1">
                {new Date(handoff.createdAt).toLocaleString()}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">From Staff</div>
              <div className="font-medium mt-1">{handoff.fromStaffId}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">To Staff</div>
              <div className="font-medium mt-1">{handoff.toStaffId}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Facility</div>
              <div className="font-medium mt-1">{handoff.facilityId}</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* SBAR Report */}
      {sbar ? (
        <SBARViewer sbar={sbar} onUpdate={() => refetchSbar()} />
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-4" />
            <p className="text-gray-500">SBAR report is being generated...</p>
            <p className="text-sm text-gray-400 mt-2">
              This may take a few moments
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
