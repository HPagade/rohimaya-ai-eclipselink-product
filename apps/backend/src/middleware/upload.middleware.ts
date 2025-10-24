import multer from 'multer';
import { Request } from 'express';
import { APIError } from './error.middleware';

/**
 * File Upload Middleware
 * Handles voice recording uploads
 * Based on Part 4B specifications
 */

// Allowed audio MIME types
const ALLOWED_AUDIO_TYPES = [
  'audio/webm',
  'audio/mp3',
  'audio/mpeg',
  'audio/wav',
  'audio/ogg',
  'audio/m4a',
  'audio/x-m4a'
];

// Max file size: 10MB
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB in bytes

/**
 * File filter - validate audio format
 */
const fileFilter = (
  req: Request,
  file: Express.Multer.File,
  callback: multer.FileFilterCallback
) => {
  if (ALLOWED_AUDIO_TYPES.includes(file.mimetype)) {
    callback(null, true);
  } else {
    callback(
      new APIError(
        'INVALID_FILE_FORMAT',
        'Unsupported audio format',
        400,
        {
          supportedFormats: ALLOWED_AUDIO_TYPES,
          receivedFormat: file.mimetype
        }
      )
    );
  }
};

/**
 * Multer configuration for memory storage
 * Files stored in memory temporarily for upload to R2
 */
const storage = multer.memoryStorage();

/**
 * Voice upload middleware
 */
export const voiceUpload = multer({
  storage,
  limits: {
    fileSize: MAX_FILE_SIZE,
    files: 1 // Only one file per upload
  },
  fileFilter
});

/**
 * Error handler for multer errors
 */
export function handleMulterError(
  err: any,
  req: Request,
  res: any,
  next: any
) {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return next(
        new APIError(
          'FILE_TOO_LARGE',
          'Audio file exceeds maximum size of 10MB',
          400,
          {
            maxSize: MAX_FILE_SIZE,
            maxSizeFormatted: '10 MB'
          }
        )
      );
    }

    if (err.code === 'LIMIT_UNEXPECTED_FILE') {
      return next(
        new APIError(
          'VALIDATION_ERROR',
          'Unexpected file field',
          400,
          {
            message: 'Only one file allowed with field name "audio"'
          }
        )
      );
    }

    return next(
      new APIError(
        'FILE_UPLOAD_ERROR',
        err.message,
        400
      )
    );
  }

  next(err);
}
