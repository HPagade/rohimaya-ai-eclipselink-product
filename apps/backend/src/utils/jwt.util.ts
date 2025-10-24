import jwt from 'jsonwebtoken';
import { UUID } from '@eclipselink/types';

/**
 * JWT Payload Structure
 * Based on Part 4A specifications
 */
export interface JWTPayload {
  userId: UUID;
  facilityId: UUID;
  role: string;
  permissions: string[];
  iat: number;
  exp: number;
  iss: string;
  aud: string;
}

export interface RefreshTokenPayload {
  userId: UUID;
  tokenId: string;
  type: 'refresh';
  iat: number;
  exp: number;
  iss: string;
  aud: string;
}

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
  tokenType: 'Bearer';
}

/**
 * JWT Configuration
 */
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'your-refresh-secret-key';
const ACCESS_TOKEN_EXPIRY = '1h'; // 1 hour
const REFRESH_TOKEN_EXPIRY = '30d'; // 30 days
const ISSUER = 'eclipselink-api';
const AUDIENCE = 'eclipselink-frontend';

/**
 * Generate access token (1 hour expiry)
 */
export function generateAccessToken(
  userId: UUID,
  facilityId: UUID,
  role: string,
  permissions: string[]
): string {
  const payload: Omit<JWTPayload, 'iat' | 'exp'> = {
    userId,
    facilityId,
    role,
    permissions,
    iss: ISSUER,
    aud: AUDIENCE
  };

  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: ACCESS_TOKEN_EXPIRY,
    issuer: ISSUER,
    audience: AUDIENCE
  });
}

/**
 * Generate refresh token (30 days expiry)
 */
export function generateRefreshToken(userId: UUID, tokenId: string): string {
  const payload: Omit<RefreshTokenPayload, 'iat' | 'exp'> = {
    userId,
    tokenId,
    type: 'refresh',
    iss: ISSUER,
    aud: AUDIENCE
  };

  return jwt.sign(payload, JWT_REFRESH_SECRET, {
    expiresIn: REFRESH_TOKEN_EXPIRY,
    issuer: ISSUER,
    audience: AUDIENCE
  });
}

/**
 * Generate both access and refresh tokens
 */
export function generateTokenPair(
  userId: UUID,
  facilityId: UUID,
  role: string,
  permissions: string[],
  tokenId: string
): TokenPair {
  const accessToken = generateAccessToken(userId, facilityId, role, permissions);
  const refreshToken = generateRefreshToken(userId, tokenId);

  return {
    accessToken,
    refreshToken,
    expiresIn: 3600, // 1 hour in seconds
    tokenType: 'Bearer'
  };
}

/**
 * Verify access token
 */
export function verifyAccessToken(token: string): JWTPayload {
  try {
    const decoded = jwt.verify(token, JWT_SECRET, {
      issuer: ISSUER,
      audience: AUDIENCE
    }) as JWTPayload;

    return decoded;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new Error('AUTH_INVALID_TOKEN');
    }
    if (error instanceof jwt.JsonWebTokenError) {
      throw new Error('AUTH_INVALID_TOKEN');
    }
    throw new Error('AUTH_INVALID_TOKEN');
  }
}

/**
 * Verify refresh token
 */
export function verifyRefreshToken(token: string): RefreshTokenPayload {
  try {
    const decoded = jwt.verify(token, JWT_REFRESH_SECRET, {
      issuer: ISSUER,
      audience: AUDIENCE
    }) as RefreshTokenPayload;

    return decoded;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new Error('AUTH_INVALID_TOKEN');
    }
    if (error instanceof jwt.JsonWebTokenError) {
      throw new Error('AUTH_INVALID_TOKEN');
    }
    throw new Error('AUTH_INVALID_TOKEN');
  }
}

/**
 * Decode token without verification (for debugging)
 */
export function decodeToken(token: string): JWTPayload | RefreshTokenPayload | null {
  try {
    return jwt.decode(token) as JWTPayload | RefreshTokenPayload;
  } catch {
    return null;
  }
}

/**
 * Check if token is expired without throwing
 */
export function isTokenExpired(token: string): boolean {
  try {
    verifyAccessToken(token);
    return false;
  } catch {
    return true;
  }
}
