import { UUID } from '@eclipselink/types';

/**
 * Extend Express Request type to include authenticated user
 */
declare global {
  namespace Express {
    interface Request {
      user?: {
        userId: UUID;
        facilityId: UUID;
        role: string;
        permissions: string[];
      };
    }
  }
}

export {};
