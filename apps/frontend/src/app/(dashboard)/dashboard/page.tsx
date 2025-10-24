'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { api } from '@/lib/api-client';
import { useRouter } from 'next/navigation';
import { Plus, FileText, Users, Activity } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();

  const { data: handoffs, isLoading } = useQuery({
    queryKey: ['handoffs', 'recent'],
    queryFn: () => api.getHandoffs({ limit: 10, sortBy: 'created_at', order: 'desc' }),
  });

  const stats = {
    activeHandoffs: handoffs?.filter((h: any) => h.status === 'assigned' || h.status === 'in_progress')?.length || 0,
    completedToday: handoffs?.filter((h: any) => {
      const today = new Date().toDateString();
      return h.status === 'completed' && new Date(h.updatedAt).toDateString() === today;
    })?.length || 0,
    totalHandoffs: handoffs?.length || 0,
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">
            Welcome to EclipseLink AI™ Clinical Handoff Platform
          </p>
        </div>
        <Button onClick={() => router.push('/dashboard/handoffs/create')}>
          <Plus className="w-4 h-4 mr-2" />
          New Handoff
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Active Handoffs
            </CardTitle>
            <Activity className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeHandoffs}</div>
            <p className="text-xs text-gray-500 mt-1">
              Currently in progress
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Completed Today
            </CardTitle>
            <FileText className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedToday}</div>
            <p className="text-xs text-gray-500 mt-1">
              Handoffs finalized
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Total Handoffs
            </CardTitle>
            <Users className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalHandoffs}</div>
            <p className="text-xs text-gray-500 mt-1">
              Last 10 records
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Handoffs */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Handoffs</CardTitle>
          <CardDescription>
            Your most recent clinical handoffs
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="text-center py-8 text-gray-500">Loading...</div>
          ) : handoffs && handoffs.length > 0 ? (
            <div className="space-y-4">
              {handoffs.map((handoff: any) => (
                <div
                  key={handoff.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
                  onClick={() => router.push(`/dashboard/handoffs/${handoff.id}`)}
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <div className="font-medium text-gray-900">
                        Patient ID: {handoff.patientId}
                      </div>
                      <span
                        className={`px-2 py-1 text-xs rounded-full ${
                          handoff.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : handoff.status === 'assigned'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {handoff.status}
                      </span>
                    </div>
                    <div className="text-sm text-gray-500 mt-1">
                      {new Date(handoff.createdAt).toLocaleString()}
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    View Details
                  </Button>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No handoffs yet</p>
              <Button
                className="mt-4"
                onClick={() => router.push('/dashboard/handoffs/create')}
              >
                Create Your First Handoff
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
