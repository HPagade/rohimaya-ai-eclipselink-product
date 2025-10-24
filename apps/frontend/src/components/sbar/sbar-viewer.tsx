'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Edit2, Save, X, FileText } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { api } from '@/lib/api-client';

interface SBARData {
  id: string;
  handoffId: string;
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
  completenessScore: number;
  qualityScore: number;
  version: number;
  createdAt: string;
}

interface SBARViewerProps {
  sbar: SBARData;
  onUpdate?: () => void;
}

export function SBARViewer({ sbar: initialSbar, onUpdate }: SBARViewerProps) {
  const { toast } = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [editedSbar, setEditedSbar] = useState({
    situation: initialSbar.situation,
    background: initialSbar.background,
    assessment: initialSbar.assessment,
    recommendation: initialSbar.recommendation,
  });

  const handleSave = async () => {
    setIsSubmitting(true);

    try {
      await api.updateSbar(initialSbar.id, {
        situation: editedSbar.situation,
        background: editedSbar.background,
        assessment: editedSbar.assessment,
        recommendation: editedSbar.recommendation,
      });

      toast({
        title: 'SBAR Updated',
        description: 'Changes saved successfully',
      });

      setIsEditing(false);
      if (onUpdate) onUpdate();
    } catch (error: any) {
      toast({
        title: 'Update Failed',
        description: error.response?.data?.error?.message || 'Failed to update SBAR',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setEditedSbar({
      situation: initialSbar.situation,
      background: initialSbar.background,
      assessment: initialSbar.assessment,
      recommendation: initialSbar.recommendation,
    });
    setIsEditing(false);
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-50';
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">SBAR Report</h2>
          <p className="text-gray-500 text-sm mt-1">
            Version {initialSbar.version} • Generated {new Date(initialSbar.createdAt).toLocaleString()}
          </p>
        </div>
        <div className="flex items-center space-x-3">
          {!isEditing ? (
            <Button onClick={() => setIsEditing(true)}>
              <Edit2 className="w-4 h-4 mr-2" />
              Edit
            </Button>
          ) : (
            <>
              <Button
                variant="outline"
                onClick={handleCancel}
                disabled={isSubmitting}
              >
                <X className="w-4 h-4 mr-2" />
                Cancel
              </Button>
              <Button
                onClick={handleSave}
                disabled={isSubmitting}
              >
                <Save className="w-4 h-4 mr-2" />
                {isSubmitting ? 'Saving...' : 'Save Changes'}
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Quality Scores */}
      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-600">Completeness Score</div>
              <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(initialSbar.completenessScore)}`}>
                {Math.round(initialSbar.completenessScore * 100)}%
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-600">Quality Score</div>
              <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(initialSbar.qualityScore)}`}>
                {Math.round(initialSbar.qualityScore * 100)}%
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* SBAR Content */}
      <div className="space-y-4">
        {/* Situation */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <FileText className="w-5 h-5 mr-2 text-blue-600" />
              Situation
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isEditing ? (
              <textarea
                value={editedSbar.situation}
                onChange={(e) => setEditedSbar({ ...editedSbar, situation: e.target.value })}
                className="w-full min-h-[100px] p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="What is happening with the patient?"
              />
            ) : (
              <p className="text-gray-700 whitespace-pre-wrap">{initialSbar.situation}</p>
            )}
          </CardContent>
        </Card>

        {/* Background */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <FileText className="w-5 h-5 mr-2 text-green-600" />
              Background
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isEditing ? (
              <textarea
                value={editedSbar.background}
                onChange={(e) => setEditedSbar({ ...editedSbar, background: e.target.value })}
                className="w-full min-h-[100px] p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="What is the clinical context?"
              />
            ) : (
              <p className="text-gray-700 whitespace-pre-wrap">{initialSbar.background}</p>
            )}
          </CardContent>
        </Card>

        {/* Assessment */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <FileText className="w-5 h-5 mr-2 text-yellow-600" />
              Assessment
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isEditing ? (
              <textarea
                value={editedSbar.assessment}
                onChange={(e) => setEditedSbar({ ...editedSbar, assessment: e.target.value })}
                className="w-full min-h-[100px] p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="What do you think the problem is?"
              />
            ) : (
              <p className="text-gray-700 whitespace-pre-wrap">{initialSbar.assessment}</p>
            )}
          </CardContent>
        </Card>

        {/* Recommendation */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <FileText className="w-5 h-5 mr-2 text-red-600" />
              Recommendation
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isEditing ? (
              <textarea
                value={editedSbar.recommendation}
                onChange={(e) => setEditedSbar({ ...editedSbar, recommendation: e.target.value })}
                className="w-full min-h-[100px] p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="What should be done?"
              />
            ) : (
              <p className="text-gray-700 whitespace-pre-wrap">{initialSbar.recommendation}</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
