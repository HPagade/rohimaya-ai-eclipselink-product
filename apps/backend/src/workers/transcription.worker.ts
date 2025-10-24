import { Worker, Job } from 'bullmq';
import { TranscriptionJobData, sbarGenerationQueue } from '../config/queue.config';
import { azureOpenAIService } from '../services/azure-openai.service';
import fs from 'fs';
import path from 'path';

/**
 * Transcription Worker
 * Processes voice recordings with Azure Whisper API
 *
 * Flow:
 * 1. Receive job with voice recording details
 * 2. Download audio file from Cloudflare R2 (or read from local in dev)
 * 3. Transcribe with Azure Whisper
 * 4. Save transcription to database
 * 5. Queue SBAR generation job
 * 6. Update handoff status
 */

// Redis connection for worker
const connection = {
  host: process.env.REDIS_HOST || 'localhost',
  port: Number(process.env.REDIS_PORT) || 6379,
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: null
};

export const transcriptionWorker = new Worker<TranscriptionJobData>(
  'transcription',
  async (job: Job<TranscriptionJobData>) => {
    const { recordingId, handoffId, filePath, duration, audioFormat, facilityId } = job.data;

    console.log(`[Transcription Worker] Processing job ${job.id} for recording ${recordingId}`);

    try {
      // Update progress: Starting
      await job.updateProgress(10);

      // TODO: In production, download from Cloudflare R2
      // const audioBuffer = await r2Client.download(filePath);
      // const tempFilePath = `/tmp/${recordingId}.${audioFormat}`;
      // fs.writeFileSync(tempFilePath, audioBuffer);

      // For now, use stub file path (in dev, you'd have test audio files)
      const tempFilePath = path.join(__dirname, '../../test-audio/sample.webm');
      const audioFileExists = fs.existsSync(tempFilePath);

      if (!audioFileExists) {
        console.log(`[Transcription Worker] Audio file not found (expected in dev). Using mock transcription.`);
      }

      // Update progress: Downloading complete
      await job.updateProgress(30);

      let transcriptionResult;

      if (audioFileExists) {
        // Real transcription with Azure Whisper
        console.log(`[Transcription Worker] Transcribing audio with Azure Whisper...`);
        transcriptionResult = await azureOpenAIService.transcribeAudio(tempFilePath, {
          language: 'en',
          temperature: 0 // More deterministic
        });
      } else {
        // Mock transcription for development
        console.log(`[Transcription Worker] Using mock transcription (dev mode)`);
        transcriptionResult = {
          text: `Patient is a 60-year-old female with type 2 diabetes mellitus, admitted three days ago for hyperglycemia. Current blood glucose is 145 milligrams per deciliter, down from 320 on admission. Patient is alert and oriented times three, no acute distress noted. Vital signs are stable: temperature 98.6 Fahrenheit, blood pressure 130 over 85, heart rate 78, respiratory rate 16, oxygen saturation 98 percent on room air. Patient reports decreased thirst and improved energy levels compared to admission. Currently on insulin sliding scale, tolerating regular diet. No skin breakdown, ambulating without assistance. Past medical history includes type 2 diabetes for 10 years, hypertension, and hyperlipidemia. Home medications are Metformin 1000 milligrams twice daily and Lisinopril 10 milligrams once daily. Known allergy to Penicillin causes rash. Patient lives at home with spouse, independent with activities of daily living. Recent labs show HbA1c of 8.2 percent. Discharge education completed, patient verbalizes understanding of home glucose monitoring and medication regimen. Planning discharge tomorrow morning if glucose remains stable. Follow-up appointment scheduled with endocrinology in two weeks. Continue home medications upon discharge.`,
          duration: 45,
          confidence: 0.96,
          language: 'en',
          segments: []
        };
        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000));
      }

      // Update progress: Transcription complete
      await job.updateProgress(70);

      console.log(`[Transcription Worker] Transcription complete. Text length: ${transcriptionResult.text.length} characters`);

      // TODO: Save transcription to database
      // await db.query(`
      //   INSERT INTO ai_generations (id, handoff_id, type, input_data, output_data, model_used, confidence_score, processing_duration, status)
      //   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
      // `, [
      //   generateUUID(),
      //   handoffId,
      //   'transcription',
      //   { recordingId, duration },
      //   { text: transcriptionResult.text, confidence: transcriptionResult.confidence },
      //   'whisper-1',
      //   transcriptionResult.confidence,
      //   transcriptionResult.duration,
      //   'completed'
      // ]);

      // TODO: Update voice_recordings status
      // await db.query(`
      //   UPDATE voice_recordings
      //   SET status = $1, processed_at = NOW(), audio_quality_score = $2
      //   WHERE id = $3
      // `, ['transcribed', transcriptionResult.confidence, recordingId]);

      // TODO: Update handoff status to 'generating'
      // await db.query(`
      //   UPDATE handoffs SET status = $1 WHERE id = $2
      // `, ['generating', handoffId]);

      // Update progress: Queuing SBAR generation
      await job.updateProgress(85);

      // TODO: Get handoff details to determine if initial or update
      // const handoff = await db.query('SELECT * FROM handoffs WHERE id = $1', [handoffId]);
      // const isInitialHandoff = handoff.rows[0].is_initial_handoff;
      // const previousHandoffId = handoff.rows[0].previous_handoff_id;

      // Queue SBAR generation job
      const sbarJob = await sbarGenerationQueue.add('generate-sbar', {
        handoffId,
        patientId: 'stub-patient-id', // TODO: Get from handoff
        transcriptionText: transcriptionResult.text,
        transcriptionId: recordingId,
        isInitialHandoff: false, // TODO: Get from handoff
        previousHandoffId: undefined, // TODO: Get from handoff
        facilityId
      });

      console.log(`[Transcription Worker] Queued SBAR generation job ${sbarJob.id}`);

      // Update progress: Complete
      await job.updateProgress(100);

      // Return result
      return {
        success: true,
        recordingId,
        handoffId,
        transcription: {
          text: transcriptionResult.text,
          confidence: transcriptionResult.confidence,
          wordCount: transcriptionResult.text.split(' ').length,
          duration: transcriptionResult.duration
        },
        sbarJobId: sbarJob.id
      };

    } catch (error) {
      console.error(`[Transcription Worker] Error processing job ${job.id}:`, error);

      // TODO: Update voice_recordings status to failed
      // await db.query(`
      //   UPDATE voice_recordings SET status = $1 WHERE id = $2
      // `, ['failed', recordingId]);

      // TODO: Update handoff status to failed
      // await db.query(`
      //   UPDATE handoffs SET status = $1 WHERE id = $2
      // `, ['failed', handoffId]);

      throw error;
    }
  },
  {
    connection,
    concurrency: 5, // Process up to 5 transcriptions concurrently
    limiter: {
      max: 10, // Max 10 jobs
      duration: 60000 // Per minute (to respect Azure API rate limits)
    }
  }
);

/**
 * Worker Event Listeners
 */
transcriptionWorker.on('completed', (job, result) => {
  console.log(`[Transcription Worker] Job ${job.id} completed successfully`);
  console.log(`  - Recording: ${result.recordingId}`);
  console.log(`  - Confidence: ${result.transcription.confidence}`);
  console.log(`  - Word count: ${result.transcription.wordCount}`);
});

transcriptionWorker.on('failed', (job, error) => {
  console.error(`[Transcription Worker] Job ${job?.id} failed:`, error.message);
  console.error(`  - Attempt: ${job?.attemptsMade}/${job?.opts.attempts}`);
});

transcriptionWorker.on('progress', (job, progress) => {
  console.log(`[Transcription Worker] Job ${job.id} progress: ${progress}%`);
});

transcriptionWorker.on('error', (error) => {
  console.error('[Transcription Worker] Worker error:', error);
});

console.log('[Transcription Worker] Started and ready to process jobs');

export default transcriptionWorker;
