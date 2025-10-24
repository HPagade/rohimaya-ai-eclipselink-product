/**
 * Azure OpenAI Service
 * Handles all interactions with Azure OpenAI API for Whisper and GPT-4
 */

import { OpenAIClient, AzureKeyCredential } from '@azure/openai';
import fs from 'fs';
import path from 'path';

// =============================================
// INTERFACES
// =============================================

export interface TranscriptionResult {
  text: string;
  duration: number;
  confidence: number;
  language: string;
  segments?: TranscriptionSegment[];
}

export interface TranscriptionSegment {
  id: number;
  start: number;
  end: number;
  text: string;
}

export interface TranscriptionOptions {
  language?: string;
  prompt?: string;
  temperature?: number;
}

export interface GPT4CompletionOptions {
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  frequencyPenalty?: number;
  presencePenalty?: number;
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface GPT4Response {
  content: string;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  model: string;
  finishReason: string;
}

// =============================================
// CUSTOM ERRORS
// =============================================

export class TranscriptionError extends Error {
  constructor(message: string, public readonly originalError?: any) {
    super(message);
    this.name = 'TranscriptionError';
  }
}

export class GPT4Error extends Error {
  constructor(message: string, public readonly originalError?: any) {
    super(message);
    this.name = 'GPT4Error';
  }
}

// =============================================
// AZURE OPENAI SERVICE
// =============================================

export class AzureOpenAIService {
  private client: OpenAIClient;
  private whisperDeployment: string;
  private gpt4Deployment: string;
  private apiVersion: string;

  constructor() {
    // Validate environment variables
    this.validateEnvironment();

    // Initialize Azure OpenAI client
    this.client = new OpenAIClient(
      process.env.AZURE_OPENAI_ENDPOINT!,
      new AzureKeyCredential(process.env.AZURE_OPENAI_API_KEY!)
    );

    this.whisperDeployment = process.env.AZURE_OPENAI_WHISPER_DEPLOYMENT || 'whisper-deployment-1';
    this.gpt4Deployment = process.env.AZURE_OPENAI_GPT4_DEPLOYMENT || 'gpt4-deployment-1';
    this.apiVersion = process.env.AZURE_OPENAI_API_VERSION || '2024-02-15-preview';

    console.log('✅ Azure OpenAI Service initialized');
    console.log(`  - Endpoint: ${process.env.AZURE_OPENAI_ENDPOINT}`);
    console.log(`  - Whisper Deployment: ${this.whisperDeployment}`);
    console.log(`  - GPT-4 Deployment: ${this.gpt4Deployment}`);
  }

  /**
   * Validate required environment variables
   */
  private validateEnvironment(): void {
    const required = [
      'AZURE_OPENAI_ENDPOINT',
      'AZURE_OPENAI_API_KEY'
    ];

    const missing = required.filter(key => !process.env[key]);

    if (missing.length > 0) {
      throw new Error(
        `Missing required environment variables: ${missing.join(', ')}\n` +
        'Please check your .env file and ensure all Azure OpenAI credentials are set.'
      );
    }
  }

  // =============================================
  // WHISPER TRANSCRIPTION METHODS
  // =============================================

  /**
   * Transcribe audio file using Whisper API
   * @param audioFilePath - Path to audio file
   * @param options - Transcription options
   * @returns Transcription result with text, confidence, and segments
   */
  async transcribeAudio(
    audioFilePath: string,
    options: TranscriptionOptions = {}
  ): Promise<TranscriptionResult> {
    const startTime = Date.now();

    try {
      // Validate file exists
      if (!fs.existsSync(audioFilePath)) {
        throw new TranscriptionError(`Audio file not found: ${audioFilePath}`);
      }

      // Read audio file
      const audioBuffer = fs.readFileSync(audioFilePath);

      console.log(`🎙️  Transcribing audio: ${path.basename(audioFilePath)}`);
      console.log(`  - File size: ${(audioBuffer.length / 1024 / 1024).toFixed(2)} MB`);
      console.log(`  - Language: ${options.language || 'auto-detect'}`);

      // Call Whisper API
      const result = await this.client.getAudioTranscription(
        this.whisperDeployment,
        audioBuffer,
        {
          language: options.language || 'en',
          prompt: options.prompt,
          temperature: options.temperature || 0,
          responseFormat: 'verbose_json' // Get detailed output with timestamps
        }
      );

      const duration = Date.now() - startTime;

      // Parse result
      const transcription: TranscriptionResult = {
        text: result.text,
        duration: duration,
        confidence: this.calculateConfidence(result),
        language: result.language || 'en',
        segments: result.segments?.map((seg: any) => ({
          id: seg.id,
          start: seg.start,
          end: seg.end,
          text: seg.text
        }))
      };

      console.log(`✅ Transcription completed in ${duration}ms`);
      console.log(`  - Text length: ${transcription.text.length} characters`);
      console.log(`  - Word count: ${transcription.text.split(' ').length} words`);
      console.log(`  - Confidence: ${(transcription.confidence * 100).toFixed(1)}%`);

      return transcription;

    } catch (error: any) {
      console.error('❌ Whisper transcription error:', error);
      throw new TranscriptionError(
        `Failed to transcribe audio: ${error.message}`,
        error
      );
    }
  }

  /**
   * Calculate confidence score from Whisper result
   * Whisper doesn't provide direct confidence scores, so we estimate
   */
  private calculateConfidence(result: any): number {
    if (!result.text) return 0;

    const hasInaudible = result.text.toLowerCase().includes('[inaudible]');
    const textLength = result.text.length;
    const segmentCount = result.segments?.length || 0;

    // Simple heuristic scoring
    let confidence = 0.85; // Base confidence

    if (hasInaudible) confidence -= 0.15;
    if (textLength < 100) confidence -= 0.10;
    if (segmentCount < 5) confidence -= 0.05;

    return Math.max(0.5, Math.min(1.0, confidence));
  }

  // =============================================
  // GPT-4 GENERATION METHODS
  // =============================================

  /**
   * Generate chat completion using GPT-4
   * @param messages - Array of chat messages
   * @param options - Generation options
   * @returns GPT-4 response with tokens and metadata
   */
  async generateCompletion(
    messages: ChatMessage[],
    options: GPT4CompletionOptions = {}
  ): Promise<GPT4Response> {
    const startTime = Date.now();

    try {
      console.log(`🤖 Generating GPT-4 completion`);
      console.log(`  - Messages: ${messages.length}`);
      console.log(`  - Temperature: ${options.temperature ?? 0.7}`);
      console.log(`  - Max tokens: ${options.maxTokens ?? 2000}`);

      const response = await this.client.getChatCompletions(
        this.gpt4Deployment,
        messages,
        {
          temperature: options.temperature ?? 0.7,
          maxTokens: options.maxTokens ?? 2000,
          topP: options.topP ?? 0.95,
          frequencyPenalty: options.frequencyPenalty ?? 0,
          presencePenalty: options.presencePenalty ?? 0
        }
      );

      if (!response.choices || response.choices.length === 0) {
        throw new GPT4Error('No completion generated');
      }

      const choice = response.choices[0];
      const duration = Date.now() - startTime;

      const result: GPT4Response = {
        content: choice.message?.content || '',
        promptTokens: response.usage?.promptTokens || 0,
        completionTokens: response.usage?.completionTokens || 0,
        totalTokens: response.usage?.totalTokens || 0,
        model: response.model || this.gpt4Deployment,
        finishReason: choice.finishReason || 'stop'
      };

      console.log(`✅ GPT-4 completion generated in ${duration}ms`);
      console.log(`  - Tokens: ${result.totalTokens} (${result.promptTokens} prompt + ${result.completionTokens} completion)`);
      console.log(`  - Estimated cost: $${this.calculateCost(result.promptTokens, result.completionTokens).toFixed(4)}`);

      return result;

    } catch (error: any) {
      console.error('❌ GPT-4 completion error:', error);
      throw new GPT4Error(
        `Failed to generate completion: ${error.message}`,
        error
      );
    }
  }

  /**
   * Calculate estimated cost for GPT-4 usage
   * Based on GPT-4 pricing: $0.03/1K input tokens, $0.06/1K output tokens
   */
  private calculateCost(promptTokens: number, completionTokens: number): number {
    const INPUT_COST_PER_1K = 0.03;
    const OUTPUT_COST_PER_1K = 0.06;

    const inputCost = (promptTokens / 1000) * INPUT_COST_PER_1K;
    const outputCost = (completionTokens / 1000) * OUTPUT_COST_PER_1K;

    return inputCost + outputCost;
  }

  /**
   * Health check for Azure OpenAI service
   * Tests connectivity and authentication
   */
  async healthCheck(): Promise<{ status: 'healthy' | 'unhealthy'; message: string }> {
    try {
      // Simple test with minimal tokens
      const testMessages: ChatMessage[] = [
        { role: 'user', content: 'Hello' }
      ];

      await this.generateCompletion(testMessages, {
        maxTokens: 5,
        temperature: 0
      });

      return {
        status: 'healthy',
        message: 'Azure OpenAI service is operational'
      };
    } catch (error: any) {
      return {
        status: 'unhealthy',
        message: `Azure OpenAI service error: ${error.message}`
      };
    }
  }
}

// Export singleton instance
export const azureOpenAIService = new AzureOpenAIService();
