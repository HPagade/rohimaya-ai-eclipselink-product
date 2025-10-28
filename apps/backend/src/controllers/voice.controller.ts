import { Request, Response } from 'express';
import { UUID } from '@eclipselink/types';
import { NotFoundError, ValidationError } from '../middleware/error.middleware';
import { transcriptionQueue } from '../config/queue.config';
import { db } from '../config/database.config';
import { storageService } from '../services/storage.service';
import { DBVoiceRecording, DBHandoff, DBStaff } from '../types/database.types';

/**
 * Voice Recording Controller
 * Handles voice recording upload and processing endpoints
 * Based on Part 4B specifications
 *
 * Full implementation with:
 * - Cloudflare R2 storage integration
 * - PostgreSQL database operations
 * - BullMQ job queue management
 * - Presigned URL generation for secure downloads
 */

/**
 * POST /v1/voice/upload
 * Upload voice recording for transcription
 */
export async function uploadVoiceRecording(req: Request, res: Response): Promise<void> {
  const { handoffId, duration } = req.body;
  const audioFile = req.file;

  if (!audioFile) {
    throw new ValidationError('Audio file is required');
  }

  try {
    // 1. Validate handoff exists and belongs to facility
    const handoffResult = await db.query<DBHandoff>(
      'SELECT * FROM handoffs WHERE id = $1 AND facility_id = $2',
      [handoffId, req.user!.facilityId]
    );

    if (handoffResult.rows.length === 0) {
      throw new NotFoundError('handoff', handoffId);
    }

    const handoff = handoffResult.rows[0];

    // 2. Upload file to Cloudflare R2
    const audioFormat = (audioFile.mimetype.split('/')[1] || 'webm') as any;
    const uploadResult = await storageService.uploadFile(
      {
        fileName: audioFile.originalname || `recording-${Date.now()}.${audioFormat}`,
        fileBuffer: audioFile.buffer,
        contentType: audioFile.mimetype,
        metadata: {
          'handoff-id': handoffId,
          'uploaded-by': req.user!.userId,
          'duration': String(duration)
        }
      },
      req.user!.facilityId,
      handoffId
    );

    console.log(`✅ Uploaded audio file to R2: ${uploadResult.fileKey}`);

    // 3. Create voice_recording record in database
    const recordingResult = await db.query<DBVoiceRecording>(
      `INSERT INTO voice_recordings (
        handoff_id, uploaded_by, facility_id, duration, file_size, audio_format,
        file_path, file_url, status, uploaded_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW())
      RETURNING *`,
      [
        handoffId,
        req.user!.userId,
        req.user!.facilityId,
        Number(duration),
        uploadResult.fileSize,
        audioFormat,
        uploadResult.fileKey,
        uploadResult.fileUrl,
        'uploaded'
      ]
    );

    const recording = recordingResult.rows[0];

    // 4. Update handoff status to 'recording'
    await db.query(
      'UPDATE handoffs SET status = $1, updated_at = NOW() WHERE id = $2',
      ['recording', handoffId]
    );

    // 5. Queue transcription job with BullMQ
    const transcriptionJob = await transcriptionQueue.add('transcribe-audio', {
      recordingId: recording.id,
      handoffId,
      filePath: uploadResult.fileKey,
      duration: Number(duration),
      audioFormat,
      facilityId: req.user!.facilityId
    }, {
      priority: 1, // High priority for transcription
      removeOnComplete: { count: 100, age: 24 * 60 * 60 }, // Keep last 100 jobs for 24 hours
      removeOnFail: false, // Keep failed jobs for debugging
      attempts: 3, // Retry up to 3 times
      backoff: {
        type: 'exponential',
        delay: 5000 // Start with 5 second delay
      }
    });

    console.log(`🎯 Queued transcription job ${transcriptionJob.id} for recording ${recording.id}`);

    res.status(201).json({
      success: true,
      data: {
        recordingId: recording.id,
        handoffId,
        duration: recording.duration,
        fileSize: recording.file_size,
        audioFormat: recording.audio_format,
        status: recording.status,
        filePath: recording.file_path,
        transcriptionJobId: transcriptionJob.id,
        estimatedProcessingTime: Math.ceil(Number(duration) / 6), // Rough estimate: 1/6 of audio duration
        uploadedAt: recording.uploaded_at,
        message: 'Voice recording uploaded successfully. Transcription will begin shortly.'
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * GET /v1/voice/:id
 * Get voice recording details
 */
export async function getVoiceRecording(req: Request, res: Response): Promise<void> {
  const { id } = req.params;

  try {
    // Fetch recording with staff details
    const result = await db.query<any>(
      `SELECT
        vr.*,
        s.id as staff_id, s.first_name, s.last_name, s.role
      FROM voice_recordings vr
      LEFT JOIN staff s ON vr.uploaded_by = s.id
      WHERE vr.id = $1 AND vr.facility_id = $2`,
      [id, req.user!.facilityId]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('voice_recording', id);
    }

    const row = result.rows[0];

    res.status(200).json({
      success: true,
      data: {
        id: row.id,
        handoffId: row.handoff_id,
        uploadedBy: {
          id: row.staff_id,
          firstName: row.first_name,
          lastName: row.last_name,
          role: row.role
        },
        duration: row.duration,
        fileSize: row.file_size,
        audioFormat: row.audio_format,
        status: row.status,
        filePath: row.file_path,
        fileUrl: row.file_url,
        transcriptionJobId: row.transcription_job_id,
        transcriptionText: row.transcription_text,
        transcriptionConfidence: row.transcription_confidence,
        transcriptionAttempts: row.transcription_attempts,
        audioQualityScore: row.audio_quality_score,
        uploadedAt: row.uploaded_at,
        processedAt: row.processed_at,
        createdAt: row.created_at
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * GET /v1/voice/:id/download
 * Get presigned URL for audio download
 */
export async function getVoiceDownloadUrl(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const { expiresIn = 900 } = req.query; // Default 15 minutes

  try {
    // Fetch recording from database
    const result = await db.query<DBVoiceRecording>(
      'SELECT * FROM voice_recordings WHERE id = $1 AND facility_id = $2',
      [id, req.user!.facilityId]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('voice_recording', id);
    }

    const recording = result.rows[0];

    // Generate presigned URL from Cloudflare R2
    const presignedUrl = await storageService.getPresignedUrl(
      recording.file_path,
      { expiresIn: Number(expiresIn) }
    );

    const expiresAt = new Date(Date.now() + Number(expiresIn) * 1000).toISOString();
    const fileName = `recording-${recording.handoff_id}-${recording.id}.${recording.audio_format}`;

    res.status(200).json({
      success: true,
      data: {
        downloadUrl: presignedUrl,
        expiresAt,
        expiresIn: Number(expiresIn),
        fileName,
        fileSize: recording.file_size,
        contentType: `audio/${recording.audio_format}`,
        duration: recording.duration
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * GET /v1/voice/:id/status
 * Get transcription/processing status
 */
export async function getVoiceStatus(req: Request, res: Response): Promise<void> {
  const { id } = req.params;

  try {
    // Fetch recording status from database
    const result = await db.query<DBVoiceRecording>(
      'SELECT * FROM voice_recordings WHERE id = $1 AND facility_id = $2',
      [id, req.user!.facilityId]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('voice_recording', id);
    }

    const recording = result.rows[0];

    // Fetch job status from queue if available
    let jobInfo = null;
    if (recording.transcription_job_id) {
      try {
        const job = await transcriptionQueue.getJob(recording.transcription_job_id);
        if (job) {
          const state = await job.getState();
          jobInfo = {
            id: job.id,
            state,
            progress: job.progress,
            attempts: job.attemptsMade,
            failedReason: job.failedReason
          };
        }
      } catch (error) {
        console.warn(`Could not fetch job status: ${error}`);
      }
    }

    // Return status based on recording state
    if (recording.status === 'processing' || recording.status === 'uploaded') {
      res.status(200).json({
        success: true,
        data: {
          recordingId: id,
          status: 'processing',
          stage: 'transcription',
          progress: jobInfo?.progress || 0,
          transcriptionJobId: recording.transcription_job_id,
          transcriptionAttempts: recording.transcription_attempts || 0,
          uploadedAt: recording.uploaded_at,
          estimatedCompletionAt: recording.uploaded_at ?
            new Date(new Date(recording.uploaded_at).getTime() + (recording.duration * 1000 / 6)).toISOString() : null,
          message: 'Transcribing audio with Azure Whisper API...',
          jobInfo
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
    } else if (recording.status === 'transcribed') {
      const wordCount = recording.transcription_text ? recording.transcription_text.split(/\s+/).length : 0;

      res.status(200).json({
        success: true,
        data: {
          recordingId: id,
          status: 'transcribed',
          stage: 'completed',
          progress: 100,
          transcriptionJobId: recording.transcription_job_id,
          uploadedAt: recording.uploaded_at,
          processedAt: recording.processed_at,
          processingDuration: recording.processed_at && recording.uploaded_at ?
            Math.floor((new Date(recording.processed_at).getTime() - new Date(recording.uploaded_at).getTime()) / 1000) : null,
          transcription: {
            text: recording.transcription_text,
            confidence: recording.transcription_confidence,
            wordCount,
            language: 'en'
          },
          nextStep: 'sbar_generation',
          message: 'Transcription completed successfully. SBAR generation in progress...'
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
    } else if (recording.status === 'failed') {
      res.status(200).json({
        success: true,
        data: {
          recordingId: id,
          status: 'failed',
          stage: 'transcription',
          progress: 0,
          transcriptionJobId: recording.transcription_job_id,
          uploadedAt: recording.uploaded_at,
          failedAt: recording.processed_at,
          attemptNumber: recording.transcription_attempts || 0,
          maxAttempts: 3,
          error: {
            code: 'TRANSCRIPTION_FAILED',
            message: recording.error_message || 'Transcription failed',
            details: jobInfo?.failedReason ? { reason: jobInfo.failedReason } : null
          },
          retryAvailable: (recording.transcription_attempts || 0) < 3,
          message: recording.error_message || 'Transcription failed. Please try again.',
          jobInfo
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
    } else {
      // Generic response for other statuses
      res.status(200).json({
        success: true,
        data: {
          recordingId: id,
          status: recording.status,
          transcriptionJobId: recording.transcription_job_id,
          uploadedAt: recording.uploaded_at,
          processedAt: recording.processed_at,
          message: `Recording status: ${recording.status}`,
          jobInfo
        },
        meta: {
          requestId: req.headers['x-request-id'] || generateRequestId(),
          timestamp: new Date().toISOString()
        }
      });
    }
  } catch (error) {
    throw error;
  }
}

/**
 * DELETE /v1/voice/:id
 * Delete voice recording
 */
export async function deleteVoiceRecording(req: Request, res: Response): Promise<void> {
  const { id } = req.params;

  try {
    // Fetch recording to get file path
    const result = await db.query<DBVoiceRecording>(
      'SELECT * FROM voice_recordings WHERE id = $1 AND facility_id = $2',
      [id, req.user!.facilityId]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('voice_recording', id);
    }

    const recording = result.rows[0];

    // Delete file from R2 storage
    try {
      await storageService.deleteFile(recording.file_path);
      console.log(`✅ Deleted audio file from R2: ${recording.file_path}`);
    } catch (error) {
      console.warn(`⚠️  Could not delete file from R2: ${error}`);
      // Continue with database deletion even if R2 deletion fails
    }

    // Delete from database (soft delete by updating status)
    await db.query(
      'UPDATE voice_recordings SET status = $1, updated_at = NOW() WHERE id = $2',
      ['deleted', id]
    );

    res.status(200).json({
      success: true,
      message: 'Voice recording deleted successfully',
      data: {
        recordingId: id,
        deletedAt: new Date().toISOString()
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * Helper: Generate UUID
 */
function generateUUID(): UUID {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}` as UUID;
}

/**
 * Helper: Generate request ID
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
