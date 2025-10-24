import { Queue, QueueOptions } from 'bullmq';
import Redis from 'ioredis';

/**
 * BullMQ Queue Configuration
 * Manages async job processing for transcription and SBAR generation
 */

// Redis connection configuration
const redisConnection = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: Number(process.env.REDIS_PORT) || 6379,
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: null, // Required for BullMQ
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  }
});

// Default queue options
const defaultQueueOptions: QueueOptions = {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000 // Start with 2 seconds, doubles each retry
    },
    removeOnComplete: {
      count: 100, // Keep last 100 completed jobs
      age: 24 * 60 * 60 // Remove after 24 hours
    },
    removeOnFail: {
      count: 500, // Keep last 500 failed jobs
      age: 7 * 24 * 60 * 60 // Remove after 7 days
    }
  }
};

/**
 * Transcription Queue
 * Handles voice-to-text transcription with Azure Whisper
 */
export const transcriptionQueue = new Queue('transcription', {
  ...defaultQueueOptions,
  defaultJobOptions: {
    ...defaultQueueOptions.defaultJobOptions,
    attempts: 3, // Retry up to 3 times for transcription
    priority: 1, // High priority
    timeout: 60000 // 1 minute timeout
  }
});

/**
 * SBAR Generation Queue
 * Handles SBAR report generation with GPT-4
 */
export const sbarGenerationQueue = new Queue('sbar-generation', {
  ...defaultQueueOptions,
  defaultJobOptions: {
    ...defaultQueueOptions.defaultJobOptions,
    attempts: 3, // Retry up to 3 times
    priority: 2, // Lower priority than transcription
    timeout: 120000 // 2 minute timeout
  }
});

/**
 * Notification Queue
 * Handles push notifications, emails, SMS (future)
 */
export const notificationQueue = new Queue('notification', {
  ...defaultQueueOptions,
  defaultJobOptions: {
    ...defaultQueueOptions.defaultJobOptions,
    attempts: 5, // Retry more for notifications
    priority: 3, // Lower priority
    timeout: 30000 // 30 second timeout
  }
});

/**
 * Job Data Interfaces
 */
export interface TranscriptionJobData {
  recordingId: string;
  handoffId: string;
  filePath: string;
  duration: number;
  audioFormat: string;
  facilityId: string;
}

export interface SbarGenerationJobData {
  handoffId: string;
  patientId: string;
  transcriptionText: string;
  transcriptionId: string;
  isInitialHandoff: boolean;
  previousHandoffId?: string;
  previousSbarId?: string;
  facilityId: string;
}

export interface NotificationJobData {
  userId: string;
  type: 'push' | 'email' | 'sms';
  title: string;
  message: string;
  data?: Record<string, any>;
}

/**
 * Queue Event Listeners
 */
transcriptionQueue.on('error', (error) => {
  console.error('Transcription queue error:', error);
});

sbarGenerationQueue.on('error', (error) => {
  console.error('SBAR generation queue error:', error);
});

notificationQueue.on('error', (error) => {
  console.error('Notification queue error:', error);
});

/**
 * Graceful shutdown
 */
export async function closeQueues(): Promise<void> {
  console.log('Closing job queues...');
  await Promise.all([
    transcriptionQueue.close(),
    sbarGenerationQueue.close(),
    notificationQueue.close(),
    redisConnection.quit()
  ]);
  console.log('Job queues closed');
}

/**
 * Get queue stats (useful for monitoring)
 */
export async function getQueueStats() {
  const [
    transcriptionStats,
    sbarStats,
    notificationStats
  ] = await Promise.all([
    transcriptionQueue.getJobCounts(),
    sbarGenerationQueue.getJobCounts(),
    notificationQueue.getJobCounts()
  ]);

  return {
    transcription: transcriptionStats,
    sbarGeneration: sbarStats,
    notification: notificationStats
  };
}
