/**
 * Storage Service - Cloudflare R2
 * Handles voice recording uploads and file management
 * Using S3-compatible API (Cloudflare R2 is S3-compatible)
 */

import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand, HeadObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import crypto from 'crypto';
import path from 'path';

// =============================================
// INTERFACES
// =============================================

export interface UploadOptions {
  fileName: string;
  fileBuffer: Buffer;
  contentType: string;
  metadata?: Record<string, string>;
}

export interface UploadResult {
  fileKey: string;
  fileUrl: string;
  fileSize: number;
  contentType: string;
}

export interface PresignedUrlOptions {
  expiresIn?: number; // seconds, default 3600 (1 hour)
}

// =============================================
// CUSTOM ERRORS
// =============================================

export class StorageError extends Error {
  constructor(message: string, public readonly originalError?: any) {
    super(message);
    this.name = 'StorageError';
  }
}

// =============================================
// STORAGE SERVICE
// =============================================

export class StorageService {
  private client: S3Client;
  private bucketName: string;
  private publicUrl: string;

  constructor() {
    // Validate environment variables
    this.validateEnvironment();

    // Initialize S3 client for R2
    this.client = new S3Client({
      region: 'auto', // R2 uses 'auto' as region
      endpoint: `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
      credentials: {
        accessKeyId: process.env.R2_ACCESS_KEY_ID!,
        secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!
      }
    });

    this.bucketName = process.env.R2_BUCKET_NAME || 'eclipselink-production';
    this.publicUrl = process.env.R2_PUBLIC_URL || '';

    console.log('✅ Storage Service (Cloudflare R2) initialized');
    console.log(`  - Bucket: ${this.bucketName}`);
  }

  /**
   * Validate required environment variables
   */
  private validateEnvironment(): void {
    const required = [
      'R2_ACCOUNT_ID',
      'R2_ACCESS_KEY_ID',
      'R2_SECRET_ACCESS_KEY',
      'R2_BUCKET_NAME'
    ];

    const missing = required.filter(key => !process.env[key]);

    if (missing.length > 0) {
      throw new Error(
        `Missing required environment variables: ${missing.join(', ')}\n` +
        'Please check your .env file and ensure all R2 credentials are set.'
      );
    }
  }

  /**
   * Generate unique file key
   */
  private generateFileKey(originalFileName: string, facilityId: string, handoffId: string): string {
    const timestamp = Date.now();
    const randomId = crypto.randomBytes(8).toString('hex');
    const ext = path.extname(originalFileName);
    const cleanFileName = path.basename(originalFileName, ext).replace(/[^a-zA-Z0-9-_]/g, '_');

    // Structure: voice-recordings/{facilityId}/{year}/{month}/{handoffId}_{timestamp}_{random}_{filename}.ext
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');

    return `voice-recordings/${facilityId}/${year}/${month}/${handoffId}_${timestamp}_${randomId}_${cleanFileName}${ext}`;
  }

  /**
   * Upload file to R2
   * @param options Upload options
   * @param facilityId Facility ID for organizing files
   * @param handoffId Handoff ID for associating files
   * @returns Upload result with file key and URL
   */
  async uploadFile(
    options: UploadOptions,
    facilityId: string,
    handoffId: string
  ): Promise<UploadResult> {
    const startTime = Date.now();

    try {
      const { fileName, fileBuffer, contentType, metadata = {} } = options;

      console.log(`📤 Uploading file: ${fileName}`);
      console.log(`  - Size: ${(fileBuffer.length / 1024 / 1024).toFixed(2)} MB`);
      console.log(`  - Content-Type: ${contentType}`);

      // Generate unique file key
      const fileKey = this.generateFileKey(fileName, facilityId, handoffId);

      // Prepare metadata
      const fileMetadata = {
        'facility-id': facilityId,
        'handoff-id': handoffId,
        'original-filename': fileName,
        'upload-timestamp': new Date().toISOString(),
        ...metadata
      };

      // Upload to R2
      const command = new PutObjectCommand({
        Bucket: this.bucketName,
        Key: fileKey,
        Body: fileBuffer,
        ContentType: contentType,
        Metadata: fileMetadata,
        // Set cache control for audio files
        CacheControl: 'max-age=31536000', // 1 year
        // Set content disposition for downloads
        ContentDisposition: `attachment; filename="${fileName}"`
      });

      await this.client.send(command);

      const duration = Date.now() - startTime;

      const result: UploadResult = {
        fileKey,
        fileUrl: this.publicUrl ? `${this.publicUrl}/${fileKey}` : fileKey,
        fileSize: fileBuffer.length,
        contentType
      };

      console.log(`✅ File uploaded successfully in ${duration}ms`);
      console.log(`  - Key: ${fileKey}`);
      console.log(`  - URL: ${result.fileUrl}`);

      return result;

    } catch (error: any) {
      console.error('❌ File upload error:', error);
      throw new StorageError(
        `Failed to upload file: ${error.message}`,
        error
      );
    }
  }

  /**
   * Generate presigned URL for secure file download
   * @param fileKey File key in R2
   * @param options Presigned URL options
   * @returns Presigned URL that expires after specified time
   */
  async getPresignedUrl(
    fileKey: string,
    options: PresignedUrlOptions = {}
  ): Promise<string> {
    try {
      const { expiresIn = 3600 } = options; // Default 1 hour

      console.log(`🔗 Generating presigned URL for: ${fileKey}`);
      console.log(`  - Expires in: ${expiresIn} seconds`);

      const command = new GetObjectCommand({
        Bucket: this.bucketName,
        Key: fileKey
      });

      const url = await getSignedUrl(this.client, command, {
        expiresIn
      });

      console.log(`✅ Presigned URL generated`);

      return url;

    } catch (error: any) {
      console.error('❌ Presigned URL generation error:', error);
      throw new StorageError(
        `Failed to generate presigned URL: ${error.message}`,
        error
      );
    }
  }

  /**
   * Check if file exists
   * @param fileKey File key in R2
   * @returns True if file exists
   */
  async fileExists(fileKey: string): Promise<boolean> {
    try {
      const command = new HeadObjectCommand({
        Bucket: this.bucketName,
        Key: fileKey
      });

      await this.client.send(command);
      return true;

    } catch (error: any) {
      if (error.name === 'NotFound') {
        return false;
      }
      throw new StorageError(
        `Failed to check file existence: ${error.message}`,
        error
      );
    }
  }

  /**
   * Delete file from R2
   * @param fileKey File key in R2
   */
  async deleteFile(fileKey: string): Promise<void> {
    try {
      console.log(`🗑️  Deleting file: ${fileKey}`);

      const command = new DeleteObjectCommand({
        Bucket: this.bucketName,
        Key: fileKey
      });

      await this.client.send(command);

      console.log(`✅ File deleted successfully`);

    } catch (error: any) {
      console.error('❌ File deletion error:', error);
      throw new StorageError(
        `Failed to delete file: ${error.message}`,
        error
      );
    }
  }

  /**
   * Get file metadata
   * @param fileKey File key in R2
   * @returns File metadata
   */
  async getFileMetadata(fileKey: string): Promise<Record<string, any>> {
    try {
      const command = new HeadObjectCommand({
        Bucket: this.bucketName,
        Key: fileKey
      });

      const response = await this.client.send(command);

      return {
        contentType: response.ContentType,
        contentLength: response.ContentLength,
        lastModified: response.LastModified,
        metadata: response.Metadata || {}
      };

    } catch (error: any) {
      throw new StorageError(
        `Failed to get file metadata: ${error.message}`,
        error
      );
    }
  }

  /**
   * Health check for storage service
   */
  async healthCheck(): Promise<{ status: 'healthy' | 'unhealthy'; message: string }> {
    try {
      // Test by creating and deleting a small test file
      const testKey = `health-check/test-${Date.now()}.txt`;
      const testBuffer = Buffer.from('health check test');

      // Upload test file
      const uploadCommand = new PutObjectCommand({
        Bucket: this.bucketName,
        Key: testKey,
        Body: testBuffer,
        ContentType: 'text/plain'
      });

      await this.client.send(uploadCommand);

      // Delete test file
      const deleteCommand = new DeleteObjectCommand({
        Bucket: this.bucketName,
        Key: testKey
      });

      await this.client.send(deleteCommand);

      return {
        status: 'healthy',
        message: 'Storage service is operational'
      };

    } catch (error: any) {
      return {
        status: 'unhealthy',
        message: `Storage service error: ${error.message}`
      };
    }
  }
}

// Export singleton instance
export const storageService = new StorageService();
