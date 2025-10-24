/**
 * Test Script: End-to-End Workflow Demo
 * Demonstrates the complete voice transcription → SBAR generation pipeline
 *
 * This script shows how the system processes a voice recording through the entire workflow:
 * 1. Queue a transcription job
 * 2. Worker processes with Azure Whisper (or mock)
 * 3. Worker queues SBAR generation job
 * 4. SBAR worker generates structured report with GPT-4
 *
 * Usage:
 *   npm run test:workflow
 *   or
 *   npx ts-node test-workflow.ts
 */

import { transcriptionQueue, sbarGenerationQueue } from './src/config/queue.config';

// Import workers to start them
import './src/workers/transcription.worker';
import './src/workers/sbar-generation.worker';

async function testWorkflow() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║                                                            ║');
  console.log('║         EclipseLink AI - Workflow Test Script             ║');
  console.log('║                                                            ║');
  console.log('╚════════════════════════════════════════════════════════════╝');
  console.log('');
  console.log('This script demonstrates the complete async processing pipeline:');
  console.log('  1. Queue transcription job');
  console.log('  2. Transcription worker processes with Azure Whisper');
  console.log('  3. SBAR generation worker creates structured report');
  console.log('');
  console.log('─────────────────────────────────────────────────────────────');
  console.log('');

  try {
    // Step 1: Add a test transcription job
    console.log('📤 Queueing transcription job...');

    const transcriptionJob = await transcriptionQueue.add('transcribe-audio', {
      recordingId: 'test-recording-001',
      handoffId: 'test-handoff-001',
      patientId: 'test-patient-001',
      filePath: 'test-audio/sample.webm',
      duration: 185, // 3 minutes 5 seconds
      audioFormat: 'webm',
      facilityId: 'test-facility-001'
    });

    console.log(`✅ Transcription job queued: ${transcriptionJob.id}`);
    console.log('');

    // Step 2: Monitor job progress
    console.log('⏳ Monitoring job progress...');
    console.log('   (Workers will process automatically)');
    console.log('');

    // Wait for transcription to complete
    const transcriptionResult = await transcriptionJob.waitUntilFinished(
      transcriptionQueue.events,
      30000 // 30 second timeout
    );

    console.log('✅ Transcription completed!');
    console.log(`   - Recording ID: ${transcriptionResult.recordingId}`);
    console.log(`   - Confidence: ${(transcriptionResult.transcription.confidence * 100).toFixed(1)}%`);
    console.log(`   - Word count: ${transcriptionResult.transcription.wordCount}`);
    console.log(`   - SBAR job queued: ${transcriptionResult.sbarJobId}`);
    console.log('');

    // Step 3: Monitor SBAR generation
    console.log('⏳ Waiting for SBAR generation...');
    console.log('');

    // Get the SBAR job that was queued
    const sbarJob = await sbarGenerationQueue.getJob(transcriptionResult.sbarJobId);

    if (!sbarJob) {
      throw new Error('SBAR job not found');
    }

    // Wait for SBAR generation to complete
    const sbarResult = await sbarJob.waitUntilFinished(
      sbarGenerationQueue.events,
      60000 // 60 second timeout (GPT-4 can be slow)
    );

    console.log('✅ SBAR generation completed!');
    console.log('');
    console.log('─────────────────────────────────────────────────────────────');
    console.log('');
    console.log('📋 SBAR Report (Version ' + sbarResult.version + '):');
    console.log('');
    console.log('SITUATION:');
    console.log(sbarResult.sbar.situation);
    console.log('');
    console.log('BACKGROUND:');
    console.log(sbarResult.sbar.background);
    console.log('');
    console.log('ASSESSMENT:');
    console.log(sbarResult.sbar.assessment);
    console.log('');
    console.log('RECOMMENDATION:');
    console.log(sbarResult.sbar.recommendation);
    console.log('');
    console.log('─────────────────────────────────────────────────────────────');
    console.log('');
    console.log('📊 Quality Metrics:');
    console.log(`   - Completeness: ${(sbarResult.qualityMetrics.completenessScore * 100).toFixed(0)}%`);
    console.log(`   - Readability: ${(sbarResult.qualityMetrics.readabilityScore * 100).toFixed(0)}%`);
    console.log(`   - I-PASS Adherence: ${sbarResult.qualityMetrics.adherenceToIPassFramework ? 'Yes' : 'No'}`);
    console.log(`   - Critical Info Present: ${sbarResult.qualityMetrics.criticalInfoPresent ? 'Yes' : 'No'}`);
    console.log('');
    console.log('🤖 AI Metadata:');
    console.log(`   - Model: ${sbarResult.aiMetadata.model}`);
    console.log(`   - Tokens: ${sbarResult.aiMetadata.totalTokens} (${sbarResult.aiMetadata.promptTokens} prompt + ${sbarResult.aiMetadata.completionTokens} completion)`);
    console.log(`   - Estimated Cost: $${sbarResult.aiMetadata.estimatedCost.toFixed(4)}`);
    console.log('');
    console.log('─────────────────────────────────────────────────────────────');
    console.log('');
    console.log('✨ Workflow completed successfully!');
    console.log('');

  } catch (error) {
    console.error('');
    console.error('❌ Error during workflow test:');
    console.error(error);
    console.error('');

    if (error instanceof Error) {
      if (error.message.includes('timeout')) {
        console.error('💡 Tip: Job timed out. Check that:');
        console.error('   1. Redis is running (redis-server)');
        console.error('   2. Workers are running');
        console.error('   3. Azure OpenAI credentials are configured');
      }
    }
  } finally {
    // Clean up: close queues and exit
    console.log('🔒 Closing queues and exiting...');
    await transcriptionQueue.close();
    await sbarGenerationQueue.close();
    process.exit(0);
  }
}

// Run the test
console.log('');
console.log('Starting workflow test in 2 seconds...');
console.log('(Workers are initializing)');
console.log('');

setTimeout(() => {
  testWorkflow();
}, 2000);
