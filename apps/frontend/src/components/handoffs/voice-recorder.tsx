'use client';

import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Mic, Square, Play, Pause } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface VoiceRecorderProps {
  onRecordingComplete: (blob: Blob, duration: number) => void;
  maxDuration?: number; // in seconds
}

export function VoiceRecorder({
  onRecordingComplete,
  maxDuration = 600, // 10 minutes default
}: VoiceRecorderProps) {
  const { toast } = useToast();
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioURL, setAudioURL] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);
  const pausedTimeRef = useRef<number>(0);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm',
      });

      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        setAudioURL(url);

        const duration = Math.floor(recordingTime / 1000);
        onRecordingComplete(blob, duration);

        // Stop all tracks
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setIsPaused(false);
      startTimeRef.current = Date.now();

      // Start timer
      timerRef.current = setInterval(() => {
        const elapsed = Date.now() - startTimeRef.current - pausedTimeRef.current;
        setRecordingTime(elapsed);

        // Auto-stop at max duration
        if (elapsed >= maxDuration * 1000) {
          stopRecording();
        }
      }, 100);

      toast({
        title: 'Recording Started',
        description: 'Speak clearly into your microphone',
      });
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast({
        title: 'Microphone Access Denied',
        description: 'Please allow microphone access to record',
        variant: 'destructive',
      });
    }
  };

  const pauseRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.pause();
      setIsPaused(true);

      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  };

  const resumeRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.resume();
      setIsPaused(false);

      const pauseDuration = Date.now() - startTimeRef.current - recordingTime;
      pausedTimeRef.current += pauseDuration;

      timerRef.current = setInterval(() => {
        const elapsed = Date.now() - startTimeRef.current - pausedTimeRef.current;
        setRecordingTime(elapsed);

        if (elapsed >= maxDuration * 1000) {
          stopRecording();
        }
      }, 100);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsPaused(false);

      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }

      toast({
        title: 'Recording Complete',
        description: `Duration: ${formatTime(recordingTime)}`,
      });
    }
  };

  const formatTime = (ms: number) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-col items-center space-y-4">
          {/* Recording Timer */}
          <div className="text-center">
            {isRecording && (
              <div className="flex items-center justify-center space-x-2 mb-2">
                <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                <span className="text-sm text-gray-500">
                  {isPaused ? 'Paused' : 'Recording'}
                </span>
              </div>
            )}
            <div className="text-4xl font-mono font-bold text-gray-900">
              {formatTime(recordingTime)}
            </div>
            <div className="text-sm text-gray-500 mt-1">
              Max duration: {maxDuration / 60} minutes
            </div>
          </div>

          {/* Recording Controls */}
          <div className="flex items-center space-x-4">
            {!isRecording && !audioURL && (
              <Button
                size="lg"
                onClick={startRecording}
                className="w-32"
              >
                <Mic className="w-5 h-5 mr-2" />
                Start
              </Button>
            )}

            {isRecording && (
              <>
                {!isPaused ? (
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={pauseRecording}
                    className="w-32"
                  >
                    <Pause className="w-5 h-5 mr-2" />
                    Pause
                  </Button>
                ) : (
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={resumeRecording}
                    className="w-32"
                  >
                    <Play className="w-5 h-5 mr-2" />
                    Resume
                  </Button>
                )}
                <Button
                  size="lg"
                  variant="destructive"
                  onClick={stopRecording}
                  className="w-32"
                >
                  <Square className="w-5 h-5 mr-2" />
                  Stop
                </Button>
              </>
            )}
          </div>

          {/* Audio Playback */}
          {audioURL && !isRecording && (
            <div className="w-full space-y-4">
              <audio
                src={audioURL}
                controls
                className="w-full"
              />
              <Button
                variant="outline"
                onClick={() => {
                  setAudioURL(null);
                  setRecordingTime(0);
                  pausedTimeRef.current = 0;
                }}
                className="w-full"
              >
                Record Again
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
