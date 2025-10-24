/**
 * SBAR Generation Service
 * Handles generation of SBAR reports from clinical handoff transcriptions
 * Uses Azure OpenAI GPT-4 with specialized prompts
 */

import { azureOpenAIService, ChatMessage, GPT4Error } from './azure-openai.service';

// =============================================
// INTERFACES
// =============================================

export interface PatientContext {
  id: string;
  firstName: string;
  lastName: string;
  mrn: string;
  dateOfBirth: string;
  gender: string;
  admissionDate?: string;
  roomNumber?: string;
  bedNumber?: string;
  knownAllergies?: string[];
  knownMedications?: string[];
}

export interface SBARReport {
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
  currentStatus?: string;
  vitalSigns?: VitalSigns;
  medications?: Medication[];
  allergies?: Allergy[];
  recentLabs?: any;
  pendingTasks?: string[];
  changesSinceLastVersion?: SBARChange[];
  version: number;
  isInitial: boolean;
  previousVersionId?: string | null;
  completenessScore?: number;
  readabilityScore?: number;
}

export interface VitalSigns {
  temperature?: number;
  bpSystolic?: number;
  bpDiastolic?: number;
  heartRate?: number;
  respiratoryRate?: number;
  oxygenSaturation?: number;
  pain?: number;
}

export interface Medication {
  name: string;
  dose: string;
  frequency: string;
  route: string;
}

export interface Allergy {
  allergen: string;
  reaction: string;
  severity: string;
}

export interface SBARChange {
  section: 'situation' | 'background' | 'assessment' | 'recommendation';
  type: 'update' | 'addition' | 'removal' | 'unchanged';
  previousValue?: string;
  newValue?: string;
  field?: string;
}

export interface GenerateSBARInput {
  transcription: string;
  patientContext: PatientContext;
  handoffType: string;
  isInitial: boolean;
  previousSBAR?: SBARReport;
}

export interface SBARValidation {
  isValid: boolean;
  errors: string[];
  completenessScore: number;
}

// =============================================
// CUSTOM ERRORS
// =============================================

export class SBARGenerationError extends Error {
  constructor(message: string, public readonly originalError?: any) {
    super(message);
    this.name = 'SBARGenerationError';
  }
}

// =============================================
// PROMPT TEMPLATES
// =============================================

const INITIAL_HANDOFF_SYSTEM_PROMPT = `You are a clinical documentation specialist creating SBAR (Situation, Background, Assessment, Recommendation) reports for healthcare handoffs. You follow the I-PASS framework and Joint Commission standards.

Your task is to generate a comprehensive SBAR report from a clinical handoff transcription. This is an INITIAL handoff (admission or first documentation), so provide complete information in all sections.

OUTPUT FORMAT (JSON):
{
  "situation": "Current patient status, chief complaint, vital signs, and immediate concerns",
  "background": "Relevant medical history, medications, allergies, social history",
  "assessment": "Clinical findings, lab results, current condition assessment",
  "recommendation": "Treatment plan, follow-up needs, pending tasks",
  "currentStatus": "Brief status summary",
  "medications": [{"name": "...", "dose": "...", "frequency": "...", "route": "..."}],
  "allergies": [{"allergen": "...", "reaction": "...", "severity": "..."}],
  "vitalSigns": {"temperature": 0, "bpSystolic": 0, "bpDiastolic": 0, "heartRate": 0, "respiratoryRate": 0, "oxygenSaturation": 0},
  "pendingTasks": ["task 1", "task 2"]
}

GUIDELINES:
- Extract ALL relevant clinical information
- Use clear, professional medical language
- Include specific measurements with units
- Organize information logically
- Flag critical information
- Be thorough - this is the baseline for future updates
- Follow I-PASS framework: Illness severity, Patient summary, Action list, Situation awareness, Synthesis by receiver
- Ensure Joint Commission compliance`;

const UPDATE_HANDOFF_SYSTEM_PROMPT = `You are a clinical documentation specialist updating SBAR (Situation, Background, Assessment, Recommendation) reports for healthcare handoffs.

Your task is to generate an UPDATED SBAR report that captures CHANGES since the previous handoff. You will receive:
1. The current handoff transcription (describing changes)
2. The previous SBAR report (baseline)

OUTPUT FORMAT (JSON):
{
  "situation": "Updated current status - highlight what has CHANGED",
  "background": "Use '[Stable - see v{N}]' if unchanged, otherwise update",
  "assessment": "Updated clinical findings - emphasize changes",
  "recommendation": "Updated care plan - note what's new or modified",
  "currentStatus": "Brief current status",
  "medications": [/* only if changed */],
  "allergies": [/* only if new allergies discovered */],
  "vitalSigns": {/* current vital signs */},
  "pendingTasks": [/* current pending tasks */],
  "changesSinceLastVersion": [
    {"section": "situation", "type": "update", "previousValue": "...", "newValue": "...", "field": "..."},
    {"section": "assessment", "type": "addition", "newValue": "...", "field": "..."}
  ]
}

GUIDELINES:
- Focus on CHANGES and UPDATES - don't repeat stable information
- Use "[Stable - see vN]" to reference unchanged sections
- Clearly document what has changed
- Maintain continuity with previous version
- Track specific changes in changesSinceLastVersion array
- Types of changes: "update", "addition", "removal", "unchanged"`;

// =============================================
// SBAR GENERATION SERVICE
// =============================================

export class SBARGenerationService {
  /**
   * Generate SBAR report from transcription
   * Automatically determines if initial or update based on input
   */
  async generateSBAR(input: GenerateSBARInput): Promise<SBARReport> {
    console.log(`\n📝 Generating SBAR Report`);
    console.log(`  - Patient: ${input.patientContext.firstName} ${input.patientContext.lastName} (MRN: ${input.patientContext.mrn})`);
    console.log(`  - Type: ${input.isInitial ? 'Initial' : 'Update'} handoff`);
    console.log(`  - Transcription length: ${input.transcription.length} characters`);

    if (input.isInitial) {
      return this.generateInitialSBAR(input);
    } else {
      return this.generateUpdateSBAR(input);
    }
  }

  /**
   * Generate initial SBAR report (comprehensive)
   */
  private async generateInitialSBAR(input: GenerateSBARInput): Promise<SBARReport> {
    const { transcription, patientContext } = input;

    // Build user message with context
    const userMessage = `
PATIENT INFORMATION:
- Name: ${patientContext.firstName} ${patientContext.lastName}
- MRN: ${patientContext.mrn}
- DOB: ${patientContext.dateOfBirth}
- Gender: ${patientContext.gender}
- Room: ${patientContext.roomNumber || 'Not assigned'}
${patientContext.bedNumber ? `- Bed: ${patientContext.bedNumber}` : ''}
${patientContext.admissionDate ? `- Admitted: ${patientContext.admissionDate}` : ''}
${patientContext.knownAllergies?.length ? `- Known Allergies: ${patientContext.knownAllergies.join(', ')}` : ''}
${patientContext.knownMedications?.length ? `- Known Medications: ${patientContext.knownMedications.join(', ')}` : ''}

HANDOFF TRANSCRIPTION:
${transcription}

Generate a comprehensive SBAR report from this initial clinical handoff.`;

    try {
      const messages: ChatMessage[] = [
        { role: 'system', content: INITIAL_HANDOFF_SYSTEM_PROMPT },
        { role: 'user', content: userMessage }
      ];

      console.log(`  - Calling GPT-4 for initial SBAR generation...`);

      const completion = await azureOpenAIService.generateCompletion(
        messages,
        {
          temperature: 0.3, // Lower for consistency
          maxTokens: 2500
        }
      );

      // Parse JSON response
      const sbarData = this.parseSBARResponse(completion.content);

      // Validate completeness
      const validation = this.validateSBAR(sbarData, true);

      if (!validation.isValid) {
        throw new SBARGenerationError(`SBAR validation failed: ${validation.errors.join(', ')}`);
      }

      const result: SBARReport = {
        ...sbarData,
        version: 1,
        isInitial: true,
        previousVersionId: null,
        completenessScore: validation.completenessScore,
        readabilityScore: this.calculateReadabilityScore(sbarData)
      };

      console.log(`✅ Initial SBAR generated successfully`);
      console.log(`  - Completeness: ${(result.completenessScore! * 100).toFixed(1)}%`);
      console.log(`  - Readability: ${(result.readabilityScore! * 100).toFixed(1)}%`);

      return result;

    } catch (error: any) {
      console.error('❌ Initial SBAR generation error:', error);
      throw new SBARGenerationError('Failed to generate initial SBAR', error);
    }
  }

  /**
   * Generate update SBAR report (changes only)
   */
  private async generateUpdateSBAR(input: GenerateSBARInput): Promise<SBARReport> {
    const { transcription, patientContext, previousSBAR } = input;

    if (!previousSBAR) {
      throw new SBARGenerationError('Previous SBAR required for update handoff');
    }

    // Build user message with context AND previous SBAR
    const userMessage = `
PATIENT INFORMATION:
- Name: ${patientContext.firstName} ${patientContext.lastName}
- MRN: ${patientContext.mrn}

PREVIOUS SBAR (Version ${previousSBAR.version}):
---
SITUATION: ${previousSBAR.situation}

BACKGROUND: ${previousSBAR.background}

ASSESSMENT: ${previousSBAR.assessment}

RECOMMENDATION: ${previousSBAR.recommendation}
---

CURRENT HANDOFF TRANSCRIPTION (describing changes):
${transcription}

Generate an updated SBAR report that captures the changes since the previous version.
Focus on what has changed - use "[Stable - see v${previousSBAR.version}]" for unchanged sections.`;

    try {
      const messages: ChatMessage[] = [
        { role: 'system', content: UPDATE_HANDOFF_SYSTEM_PROMPT },
        { role: 'user', content: userMessage }
      ];

      console.log(`  - Calling GPT-4 for update SBAR generation...`);

      const completion = await azureOpenAIService.generateCompletion(
        messages,
        {
          temperature: 0.3,
          maxTokens: 2000
        }
      );

      // Parse JSON response
      const sbarData = this.parseSBARResponse(completion.content);

      // Merge stable sections from previous version
      const mergedSBAR = this.mergeWithPrevious(sbarData, previousSBAR);

      // Validate
      const validation = this.validateSBAR(mergedSBAR, false);

      if (!validation.isValid) {
        throw new SBARGenerationError(`SBAR validation failed: ${validation.errors.join(', ')}`);
      }

      const result: SBARReport = {
        ...mergedSBAR,
        version: previousSBAR.version + 1,
        isInitial: false,
        previousVersionId: previousSBAR.previousVersionId,
        completenessScore: validation.completenessScore,
        readabilityScore: this.calculateReadabilityScore(mergedSBAR)
      };

      console.log(`✅ Update SBAR generated successfully`);
      console.log(`  - Version: ${result.version}`);
      console.log(`  - Changes: ${result.changesSinceLastVersion?.length || 0}`);

      return result;

    } catch (error: any) {
      console.error('❌ Update SBAR generation error:', error);
      throw new SBARGenerationError('Failed to generate update SBAR', error);
    }
  }

  /**
   * Parse GPT-4 JSON response to SBAR object
   */
  private parseSBARResponse(content: string): Partial<SBARReport> {
    try {
      // Extract JSON from response (might have markdown code blocks)
      const jsonMatch = content.match(/```json\s*([\s\S]*?)\s*```/) || content.match(/\{[\s\S]*\}/);

      if (!jsonMatch) {
        throw new Error('No JSON found in response');
      }

      const jsonString = jsonMatch[1] || jsonMatch[0];
      const parsed = JSON.parse(jsonString);

      return parsed;
    } catch (error: any) {
      console.error('Failed to parse SBAR response:', error);
      console.error('Raw content:', content.substring(0, 500));
      throw new SBARGenerationError('Failed to parse GPT-4 response as JSON', error);
    }
  }

  /**
   * Merge updated SBAR with previous version for stable sections
   */
  private mergeWithPrevious(
    updated: Partial<SBARReport>,
    previous: SBARReport
  ): Partial<SBARReport> {
    const merged = { ...updated };

    // Replace "[Stable - see vN]" references with actual content
    const stablePattern = /\[Stable - see v\d+\]/i;

    if (updated.situation && stablePattern.test(updated.situation)) {
      merged.situation = previous.situation;
    }

    if (updated.background && stablePattern.test(updated.background)) {
      merged.background = previous.background;
    }

    if (updated.assessment && stablePattern.test(updated.assessment)) {
      merged.assessment = previous.assessment;
    }

    if (updated.recommendation && stablePattern.test(updated.recommendation)) {
      merged.recommendation = previous.recommendation;
    }

    return merged;
  }

  /**
   * Validate SBAR completeness and correctness
   */
  private validateSBAR(sbar: Partial<SBARReport>, isInitial: boolean): SBARValidation {
    const errors: string[] = [];
    let score = 0;
    const maxScore = 4; // 4 main sections

    // Required sections
    if (!sbar.situation || sbar.situation.length < 10) {
      errors.push('Situation section is missing or too short');
    } else {
      score++;
    }

    if (!sbar.background || sbar.background.length < 10) {
      errors.push('Background section is missing or too short');
    } else {
      score++;
    }

    if (!sbar.assessment || sbar.assessment.length < 10) {
      errors.push('Assessment section is missing or too short');
    } else {
      score++;
    }

    if (!sbar.recommendation || sbar.recommendation.length < 10) {
      errors.push('Recommendation section is missing or too short');
    } else {
      score++;
    }

    // For initial handoffs, require more detail
    if (isInitial && score < 3) {
      errors.push('Initial SBAR must have at least 3 complete sections');
    }

    return {
      isValid: errors.length === 0,
      errors,
      completenessScore: score / maxScore
    };
  }

  /**
   * Calculate readability score (simplified Flesch-Kincaid)
   */
  private calculateReadabilityScore(sbar: Partial<SBARReport>): number {
    const text = [
      sbar.situation,
      sbar.background,
      sbar.assessment,
      sbar.recommendation
    ].filter(Boolean).join(' ');

    const sentences = text.split(/[.!?]+/).length;
    const words = text.split(/\s+/).length;
    const syllables = this.countSyllables(text);

    if (sentences === 0 || words === 0) return 0;

    // Flesch Reading Ease (simplified)
    const score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words);

    // Normalize to 0-1 range (60-100 is good range)
    return Math.max(0, Math.min(1, (score - 40) / 60));
  }

  /**
   * Count syllables in text (approximation)
   */
  private countSyllables(text: string): number {
    return text
      .toLowerCase()
      .split(/\s+/)
      .reduce((count, word) => {
        word = word.replace(/[^a-z]/g, '');
        const vowels = word.match(/[aeiouy]+/g);
        return count + (vowels ? vowels.length : 1);
      }, 0);
  }
}

// Export singleton instance
export const sbarGenerationService = new SBARGenerationService();
