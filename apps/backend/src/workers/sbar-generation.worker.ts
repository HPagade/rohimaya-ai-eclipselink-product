import { Worker, Job } from 'bullmq';
import { SbarGenerationJobData, notificationQueue } from '../config/queue.config';
import { azureOpenAIService, ChatMessage } from '../services/azure-openai.service';

/**
 * SBAR Generation Worker
 * Processes transcribed handoffs and generates structured SBAR reports
 *
 * Flow:
 * 1. Receive job with transcription text and handoff details
 * 2. Determine if initial or update handoff
 * 3. If update, fetch previous SBAR for comparison context
 * 4. Generate SBAR report with GPT-4 using I-PASS framework
 * 5. Parse and validate SBAR structure
 * 6. Calculate quality metrics (completeness, readability, adherence)
 * 7. Detect changes from previous version (if update)
 * 8. Save SBAR to database
 * 9. Update handoff status to 'ready'
 * 10. Queue notification to assigned provider
 */

// Redis connection for worker
const connection = {
  host: process.env.REDIS_HOST || 'localhost',
  port: Number(process.env.REDIS_PORT) || 6379,
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: null
};

/**
 * System prompt for SBAR generation
 * Based on I-PASS clinical handoff framework
 */
const SBAR_SYSTEM_PROMPT = `You are an expert clinical documentation AI assistant specialized in generating structured SBAR (Situation-Background-Assessment-Recommendation) reports for patient handoffs.

Your task is to convert voice transcription into a clear, concise, and clinically accurate SBAR report following the I-PASS framework.

SBAR Structure:
1. **Situation**: Current patient status, chief complaint, vital signs, current symptoms
2. **Background**: Medical history, admission reason, hospital course, medications, allergies
3. **Assessment**: Clinical assessment, lab results, imaging findings, current trends
4. **Recommendation**: Care plan, pending tasks, follow-up actions, safety concerns

Requirements:
- Use clear, professional medical language
- Include specific values (vitals, labs, medications with doses)
- Highlight critical information (allergies, abnormal vitals, urgent tasks)
- Be concise but comprehensive
- Follow chronological order in Background section
- Prioritize safety-critical information

Output Format:
Return ONLY a valid JSON object with this structure:
{
  "situation": "...",
  "background": "...",
  "assessment": "...",
  "recommendation": "..."
}

Do NOT include any markdown, explanations, or additional text outside the JSON object.`;

/**
 * Generate initial SBAR prompt
 */
function buildInitialSbarPrompt(transcriptionText: string): ChatMessage[] {
  return [
    {
      role: 'system',
      content: SBAR_SYSTEM_PROMPT
    },
    {
      role: 'user',
      content: `Generate a comprehensive SBAR report from this voice transcription of a patient admission handoff:

TRANSCRIPTION:
${transcriptionText}

This is the INITIAL/BASELINE handoff for this patient. Generate a complete SBAR report capturing all relevant clinical information.`
    }
  ];
}

/**
 * Generate update SBAR prompt with previous context
 */
function buildUpdateSbarPrompt(
  transcriptionText: string,
  previousSbar: any
): ChatMessage[] {
  return [
    {
      role: 'system',
      content: SBAR_SYSTEM_PROMPT + `

IMPORTANT: This is an UPDATE handoff. You will receive the previous SBAR report and a new transcription.
Your task is to generate an UPDATED SBAR that:
1. Incorporates new information from the transcription
2. Updates changed values (vitals, labs, status)
3. Maintains unchanged relevant information from previous SBAR
4. Highlights significant changes or trends
5. Updates recommendations based on current status`
    },
    {
      role: 'user',
      content: `Generate an UPDATED SBAR report for this patient.

PREVIOUS SBAR (Version ${previousSbar.version}):
Situation: ${previousSbar.situation}
Background: ${previousSbar.background}
Assessment: ${previousSbar.assessment}
Recommendation: ${previousSbar.recommendation}

NEW TRANSCRIPTION:
${transcriptionText}

Generate an updated SBAR that incorporates the new information while maintaining relevant context from the previous version. Focus on what has changed and what remains important for continuity of care.`
    }
  ];
}

/**
 * Parse and validate SBAR JSON response
 */
function parseSbarResponse(content: string): {
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
} {
  try {
    // Remove markdown code blocks if present
    let cleanContent = content.trim();
    if (cleanContent.startsWith('```json')) {
      cleanContent = cleanContent.replace(/^```json\n/, '').replace(/\n```$/, '');
    } else if (cleanContent.startsWith('```')) {
      cleanContent = cleanContent.replace(/^```\n/, '').replace(/\n```$/, '');
    }

    const parsed = JSON.parse(cleanContent);

    // Validate required fields
    if (!parsed.situation || !parsed.background || !parsed.assessment || !parsed.recommendation) {
      throw new Error('Missing required SBAR sections');
    }

    return {
      situation: parsed.situation.trim(),
      background: parsed.background.trim(),
      assessment: parsed.assessment.trim(),
      recommendation: parsed.recommendation.trim()
    };
  } catch (error) {
    console.error('[SBAR Worker] Failed to parse GPT-4 response:', content);
    throw new Error(`Invalid SBAR JSON format: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Calculate quality metrics for SBAR report
 */
function calculateQualityMetrics(sbar: {
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
}): {
  completenessScore: number;
  readabilityScore: number;
  adherenceToIPassFramework: boolean;
  criticalInfoPresent: boolean;
} {
  // Completeness: Check for key elements
  const hasVitals = /\d+\/\d+|HR|BP|temp|O2 sat|SpO2/i.test(sbar.situation + sbar.assessment);
  const hasMedications = /medication|drug|dose|mg|ml/i.test(sbar.background);
  const hasAllergies = /allergy|allergies|allergic|NKDA/i.test(sbar.background);
  const hasTasks = /follow.?up|monitor|continue|discharge|pending/i.test(sbar.recommendation);

  const completenessScore = [hasVitals, hasMedications, hasAllergies, hasTasks]
    .filter(Boolean).length / 4;

  // Readability: Word count and sentence structure
  const totalWords = Object.values(sbar).join(' ').split(/\s+/).length;
  const avgWordsPerSection = totalWords / 4;
  const readabilityScore = avgWordsPerSection >= 30 && avgWordsPerSection <= 150 ? 0.95 : 0.75;

  // I-PASS adherence: All sections present and non-empty
  const adherenceToIPassFramework =
    sbar.situation.length > 20 &&
    sbar.background.length > 50 &&
    sbar.assessment.length > 30 &&
    sbar.recommendation.length > 20;

  // Critical info: Allergies and vitals present
  const criticalInfoPresent = hasAllergies && hasVitals;

  return {
    completenessScore: Math.round(completenessScore * 100) / 100,
    readabilityScore: Math.round(readabilityScore * 100) / 100,
    adherenceToIPassFramework,
    criticalInfoPresent
  };
}

/**
 * Detect changes between SBAR versions
 */
function detectChanges(
  newSbar: any,
  previousSbar: any
): Array<{
  section: string;
  type: 'addition' | 'removal' | 'update';
  field: string;
  previousValue?: string;
  newValue?: string;
  significance: 'high' | 'medium' | 'low';
}> {
  const changes: any[] = [];

  // Compare vital signs
  const newVitals = extractVitals(newSbar.situation + newSbar.assessment);
  const oldVitals = extractVitals(previousSbar.situation + previousSbar.assessment);

  for (const [key, newValue] of Object.entries(newVitals)) {
    const oldValue = (oldVitals as any)[key];
    if (oldValue && oldValue !== newValue) {
      changes.push({
        section: 'assessment',
        type: 'update',
        field: key,
        previousValue: oldValue,
        newValue: newValue,
        significance: key === 'temperature' || key === 'bloodPressure' ? 'high' : 'medium'
      });
    }
  }

  // Detect new medications or removed medications
  if (newSbar.background.toLowerCase().includes('medication') ||
      previousSbar.background.toLowerCase().includes('medication')) {
    changes.push({
      section: 'background',
      type: 'update',
      field: 'medications',
      significance: 'high'
    });
  }

  return changes;
}

/**
 * Extract vital signs from text
 */
function extractVitals(text: string): Record<string, string> {
  const vitals: Record<string, string> = {};

  // Blood pressure (e.g., "130/85", "BP 120/80")
  const bpMatch = text.match(/(?:BP|blood pressure)[:\s]+(\d{2,3}\/\d{2,3})/i);
  if (bpMatch) vitals.bloodPressure = bpMatch[1];

  // Heart rate (e.g., "HR 78", "heart rate 72")
  const hrMatch = text.match(/(?:HR|heart rate)[:\s]+(\d{2,3})/i);
  if (hrMatch) vitals.heartRate = hrMatch[1];

  // Temperature (e.g., "98.6°F", "temp 37.2°C")
  const tempMatch = text.match(/(?:temp|temperature)[:\s]+(\d+\.?\d*\s*[°]?[FC])/i);
  if (tempMatch) vitals.temperature = tempMatch[1];

  // Oxygen saturation (e.g., "O2 sat 98%", "SpO2 95%")
  const o2Match = text.match(/(?:O2 sat|SpO2)[:\s]+(\d{2,3}%)/i);
  if (o2Match) vitals.oxygenSaturation = o2Match[1];

  return vitals;
}

/**
 * SBAR Generation Worker
 */
export const sbarGenerationWorker = new Worker<SbarGenerationJobData>(
  'sbar-generation',
  async (job: Job<SbarGenerationJobData>) => {
    const {
      handoffId,
      patientId,
      transcriptionText,
      transcriptionId,
      isInitialHandoff,
      previousHandoffId,
      previousSbarId,
      facilityId
    } = job.data;

    console.log(`[SBAR Worker] Processing job ${job.id} for handoff ${handoffId}`);
    console.log(`  - Type: ${isInitialHandoff ? 'INITIAL' : 'UPDATE'}`);
    console.log(`  - Transcription length: ${transcriptionText.length} characters`);

    try {
      // Update progress: Starting
      await job.updateProgress(10);

      // Fetch previous SBAR if this is an update handoff
      let previousSbar = null;
      if (!isInitialHandoff && previousSbarId) {
        // TODO: Fetch from database
        // previousSbar = await db.query('SELECT * FROM sbar_reports WHERE id = $1', [previousSbarId]);
        console.log(`[SBAR Worker] Would fetch previous SBAR ${previousSbarId} for comparison`);

        // Mock previous SBAR for development
        previousSbar = {
          version: 1,
          situation: 'Patient is a 60-year-old female with type 2 diabetes. Blood glucose was 145 mg/dL on last check.',
          background: 'PMH: Type 2 diabetes x10 years, hypertension, hyperlipidemia. Medications: Metformin 1000mg BID, Lisinopril 10mg daily. Allergies: Penicillin (rash).',
          assessment: 'VS: T 98.6°F, BP 130/85, HR 78, RR 16, SpO2 98% RA. Blood glucose improving. Patient alert and oriented x3.',
          recommendation: 'Continue current medications. Monitor blood glucose. Plan discharge in 24-48 hours if stable.'
        };
      }

      // Update progress: Building prompt
      await job.updateProgress(25);

      // Build GPT-4 prompt
      const messages = isInitialHandoff
        ? buildInitialSbarPrompt(transcriptionText)
        : buildUpdateSbarPrompt(transcriptionText, previousSbar!);

      console.log(`[SBAR Worker] Generating SBAR with GPT-4...`);
      console.log(`  - Prompt type: ${isInitialHandoff ? 'Initial' : 'Update'}`);

      // Update progress: Calling GPT-4
      await job.updateProgress(40);

      // Generate SBAR with GPT-4
      const gptResponse = await azureOpenAIService.generateCompletion(messages, {
        temperature: 0.3, // Lower temperature for more consistent medical documentation
        maxTokens: 2000,
        topP: 0.95,
        frequencyPenalty: 0.2,
        presencePenalty: 0.1
      });

      console.log(`[SBAR Worker] GPT-4 response received`);
      console.log(`  - Tokens used: ${gptResponse.totalTokens}`);
      console.log(`  - Estimated cost: $${((gptResponse.promptTokens / 1000) * 0.03 + (gptResponse.completionTokens / 1000) * 0.06).toFixed(4)}`);

      // Update progress: Parsing response
      await job.updateProgress(60);

      // Parse and validate SBAR
      const sbar = parseSbarResponse(gptResponse.content);

      console.log(`[SBAR Worker] SBAR parsed successfully`);
      console.log(`  - Situation: ${sbar.situation.substring(0, 100)}...`);
      console.log(`  - Background: ${sbar.background.substring(0, 100)}...`);
      console.log(`  - Assessment: ${sbar.assessment.substring(0, 100)}...`);
      console.log(`  - Recommendation: ${sbar.recommendation.substring(0, 100)}...`);

      // Update progress: Calculating quality metrics
      await job.updateProgress(75);

      // Calculate quality metrics
      const qualityMetrics = calculateQualityMetrics(sbar);

      console.log(`[SBAR Worker] Quality metrics calculated`);
      console.log(`  - Completeness: ${(qualityMetrics.completenessScore * 100).toFixed(0)}%`);
      console.log(`  - Readability: ${(qualityMetrics.readabilityScore * 100).toFixed(0)}%`);
      console.log(`  - I-PASS adherence: ${qualityMetrics.adherenceToIPassFramework ? 'Yes' : 'No'}`);

      // Detect changes from previous version (if update)
      let changes: any[] = [];
      if (!isInitialHandoff && previousSbar) {
        changes = detectChanges(sbar, previousSbar);
        console.log(`[SBAR Worker] Detected ${changes.length} changes from previous version`);
      }

      // Update progress: Saving to database
      await job.updateProgress(85);

      // TODO: Save SBAR to database
      const sbarId = `sbar_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const version = isInitialHandoff ? 1 : (previousSbar?.version || 0) + 1;

      // await db.query(`
      //   INSERT INTO sbar_reports (
      //     id, handoff_id, patient_id, facility_id, version, previous_version_id,
      //     is_initial, situation, background, assessment, recommendation,
      //     completeness_score, readability_score, adherence_to_ipass,
      //     critical_info_present, changes_since_last_version,
      //     ai_model_used, ai_confidence_score, prompt_tokens, completion_tokens,
      //     generation_duration, status, created_at
      //   ) VALUES (
      //     $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, NOW()
      //   )
      // `, [
      //   sbarId, handoffId, patientId, facilityId, version, previousSbarId,
      //   isInitialHandoff, sbar.situation, sbar.background, sbar.assessment, sbar.recommendation,
      //   qualityMetrics.completenessScore, qualityMetrics.readabilityScore,
      //   qualityMetrics.adherenceToIPassFramework, qualityMetrics.criticalInfoPresent,
      //   JSON.stringify(changes), gptResponse.model, 0.95,
      //   gptResponse.promptTokens, gptResponse.completionTokens,
      //   Date.now() - startTime, 'completed'
      // ]);

      // TODO: Update handoff status to 'ready'
      // await db.query(`
      //   UPDATE handoffs
      //   SET status = $1, sbar_report_id = $2, sbar_generated_at = NOW()
      //   WHERE id = $3
      // `, ['ready', sbarId, handoffId]);

      console.log(`[SBAR Worker] SBAR saved to database (stub)`);
      console.log(`  - ID: ${sbarId}`);
      console.log(`  - Version: ${version}`);

      // Update progress: Queuing notification
      await job.updateProgress(95);

      // TODO: Queue notification to assigned provider
      // await notificationQueue.add('handoff-ready', {
      //   handoffId,
      //   recipientUserId: assignedProviderId,
      //   notificationType: 'handoff_ready',
      //   priority: handoffPriority,
      //   data: {
      //     patientName,
      //     handoffType,
      //     sbarVersion: version
      //   }
      // });

      console.log(`[SBAR Worker] Notification queued (stub)`);

      // Update progress: Complete
      await job.updateProgress(100);

      // Return result
      return {
        success: true,
        sbarId,
        handoffId,
        patientId,
        version,
        isInitial: isInitialHandoff,
        sbar: {
          situation: sbar.situation,
          background: sbar.background,
          assessment: sbar.assessment,
          recommendation: sbar.recommendation
        },
        qualityMetrics,
        changes: changes.length > 0 ? changes : undefined,
        aiMetadata: {
          model: gptResponse.model,
          promptTokens: gptResponse.promptTokens,
          completionTokens: gptResponse.completionTokens,
          totalTokens: gptResponse.totalTokens,
          estimatedCost: (gptResponse.promptTokens / 1000) * 0.03 + (gptResponse.completionTokens / 1000) * 0.06
        }
      };

    } catch (error) {
      console.error(`[SBAR Worker] Error processing job ${job.id}:`, error);

      // TODO: Update handoff status to failed
      // await db.query(`
      //   UPDATE handoffs SET status = $1, error_message = $2 WHERE id = $3
      // `, ['failed', error instanceof Error ? error.message : 'Unknown error', handoffId]);

      throw error;
    }
  },
  {
    connection,
    concurrency: 3, // Process up to 3 SBAR generations concurrently
    limiter: {
      max: 5, // Max 5 jobs
      duration: 60000 // Per minute (to respect Azure GPT-4 rate limits)
    }
  }
);

/**
 * Worker Event Listeners
 */
sbarGenerationWorker.on('completed', (job, result) => {
  console.log(`[SBAR Worker] Job ${job.id} completed successfully`);
  console.log(`  - SBAR ID: ${result.sbarId}`);
  console.log(`  - Version: ${result.version} ${result.isInitial ? '(INITIAL)' : '(UPDATE)'}`);
  console.log(`  - Completeness: ${(result.qualityMetrics.completenessScore * 100).toFixed(0)}%`);
  console.log(`  - Changes detected: ${result.changes?.length || 0}`);
  console.log(`  - Cost: $${result.aiMetadata.estimatedCost.toFixed(4)}`);
});

sbarGenerationWorker.on('failed', (job, error) => {
  console.error(`[SBAR Worker] Job ${job?.id} failed:`, error.message);
  console.error(`  - Attempt: ${job?.attemptsMade}/${job?.opts.attempts}`);
  if (job?.data) {
    console.error(`  - Handoff: ${job.data.handoffId}`);
  }
});

sbarGenerationWorker.on('progress', (job, progress) => {
  console.log(`[SBAR Worker] Job ${job.id} progress: ${progress}%`);
});

sbarGenerationWorker.on('error', (error) => {
  console.error('[SBAR Worker] Worker error:', error);
});

console.log('[SBAR Worker] Started and ready to process jobs');

export default sbarGenerationWorker;
