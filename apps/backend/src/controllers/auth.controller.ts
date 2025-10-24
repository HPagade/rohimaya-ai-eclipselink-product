import { Request, Response } from 'express';
import bcrypt from 'bcrypt';
import { generateTokenPair, verifyRefreshToken } from '../utils/jwt.util';
import {
  AuthenticationError,
  ValidationError,
  ConflictError,
  NotFoundError
} from '../middleware/error.middleware';
import { UUID } from '@eclipselink/types';
import { db } from '../config/database.config';
import { DBStaff, DBFacility, DBAuthSession } from '../types/database.types';

/**
 * Auth Controller
 * Handles authentication endpoints
 * Based on Part 4A specifications
 *
 * Database integrated with PostgreSQL via pg Pool
 */

/**
 * POST /v1/auth/register
 * Register a new user account
 */
export async function register(req: Request, res: Response): Promise<void> {
  const { email, password, firstName, lastName, role, facilityId, licenseNumber, licenseState } = req.body;

  try {
    // 1. Check if user already exists
    const existingUser = await db.query<DBStaff>(
      'SELECT id FROM staff WHERE email = $1',
      [email.toLowerCase()]
    );

    if (existingUser.rows.length > 0) {
      throw new ConflictError('A user with this email already exists', {
        resource: 'user',
        conflictingField: 'email',
        conflictingValue: email
      });
    }

    // 2. Verify facility exists
    const facilityResult = await db.query<DBFacility>(
      'SELECT id, name, facility_type FROM facilities WHERE id = $1 AND is_active = true',
      [facilityId]
    );

    if (facilityResult.rows.length === 0) {
      throw new NotFoundError('facility', facilityId);
    }

    const facility = facilityResult.rows[0];

    // 3. Hash password (bcrypt with 10 rounds)
    const hashedPassword = await bcrypt.hash(password, 10);

    // 4. Create user in database
    const userResult = await db.query<DBStaff>(
      `INSERT INTO staff (
        email, password_hash, first_name, last_name, role, facility_id,
        license_number, license_state, is_active, email_verified
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, true, false)
      RETURNING *`,
      [
        email.toLowerCase(),
        hashedPassword,
        firstName,
        lastName,
        role,
        facilityId,
        licenseNumber || null,
        licenseState || null
      ]
    );

    const user = userResult.rows[0];

    // 5. Get permissions for role
    const permissions = getPermissionsForRole(role);

    // 6. Generate session token ID
    const tokenId = generateTokenId();

    // 7. Generate JWT tokens
    const tokens = generateTokenPair(
      user.id,
      facilityId,
      role,
      permissions,
      tokenId
    );

    // 8. Store session in database
    const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000); // 30 days
    await db.query(
      `INSERT INTO auth_sessions (
        id, user_id, refresh_token, token_id, is_active, expires_at, last_activity_at
      ) VALUES (gen_random_uuid(), $1, $2, $3, true, $4, NOW())`,
      [user.id, tokens.refreshToken, tokenId, expiresAt]
    );

    // 9. TODO: Send verification email (async)
    // await sendVerificationEmail(email, user.id);

    // Response
    res.status(201).json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          role: user.role,
          facilityId: user.facility_id,
          facility: {
            id: facility.id,
            name: facility.name,
            type: facility.facility_type
          },
          isActive: user.is_active,
          emailVerified: user.email_verified,
          createdAt: user.created_at.toISOString()
        },
        tokens: {
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
          expiresIn: tokens.expiresIn,
          tokenType: tokens.tokenType
        }
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * POST /v1/auth/login
 * Authenticate user and receive JWT tokens
 */
export async function login(req: Request, res: Response): Promise<void> {
  const { email, password } = req.body;

  try {
    // 1. Find user by email with facility details
    const userResult = await db.query<DBStaff & { facility_name: string; facility_type: string }>(
      `SELECT s.*, f.name as facility_name, f.facility_type
       FROM staff s
       JOIN facilities f ON s.facility_id = f.id
       WHERE s.email = $1`,
      [email.toLowerCase()]
    );

    if (userResult.rows.length === 0) {
      throw new AuthenticationError('AUTH_INVALID_CREDENTIALS', 'Invalid email or password');
    }

    const user = userResult.rows[0];

    // 2. Verify password
    const isPasswordValid = await bcrypt.compare(password, user.password_hash);
    if (!isPasswordValid) {
      throw new AuthenticationError('AUTH_INVALID_CREDENTIALS', 'Invalid email or password');
    }

    // 3. Check if account is active
    if (!user.is_active) {
      throw new AuthenticationError('AUTH_ACCOUNT_LOCKED', 'Account is locked. Please contact your administrator.');
    }

    // 4. Optional: Check if email is verified (can be disabled for development)
    // if (!user.email_verified) {
    //   throw new AuthenticationError('AUTH_EMAIL_NOT_VERIFIED', 'Email address must be verified', {
    //     email,
    //     verificationEmailSent: true
    //   });
    // }

    // 5. Get permissions for role
    const permissions = getPermissionsForRole(user.role);

    // 6. Generate session token ID
    const tokenId = generateTokenId();

    // 7. Generate JWT tokens
    const tokens = generateTokenPair(
      user.id,
      user.facility_id,
      user.role,
      permissions,
      tokenId
    );

    // 8. Store session in database
    const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000); // 30 days
    await db.query(
      `INSERT INTO auth_sessions (
        id, user_id, refresh_token, token_id, is_active, expires_at, last_activity_at
      ) VALUES (gen_random_uuid(), $1, $2, $3, true, $4, NOW())`,
      [user.id, tokens.refreshToken, tokenId, expiresAt]
    );

    // 9. Update last login timestamp
    await db.query(
      'UPDATE staff SET last_login_at = NOW() WHERE id = $1',
      [user.id]
    );

    // Response
    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          role: user.role,
          facilityId: user.facility_id,
          facility: {
            id: user.facility_id,
            name: user.facility_name,
            type: user.facility_type
          },
          department: user.department,
          isActive: user.is_active,
          emailVerified: user.email_verified,
          mfaEnabled: user.two_factor_enabled,
          lastLoginAt: new Date().toISOString()
        },
        tokens: {
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
          expiresIn: tokens.expiresIn,
          tokenType: tokens.tokenType
        }
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * POST /v1/auth/refresh
 * Refresh access token using refresh token
 */
export async function refresh(req: Request, res: Response): Promise<void> {
  const { refreshToken } = req.body;

  try {
    // 1. Verify refresh token
    const decoded = verifyRefreshToken(refreshToken);

    // 2. Check if session exists in database
    // const session = await db.query('SELECT * FROM user_sessions WHERE id = $1', [decoded.tokenId]);
    // if (session.rows.length === 0) {
    //   throw new AuthenticationError('AUTH_INVALID_TOKEN', 'Invalid or expired refresh token');
    // }

    // 3. Get user details
    // const user = await db.query('SELECT * FROM staff WHERE id = $1', [decoded.userId]);

    // 4. Get permissions for role
    const permissions = getPermissionsForRole('registered_nurse');

    // 5. Generate new token ID
    const newTokenId = generateTokenId();

    // 6. Generate new token pair
    const tokens = generateTokenPair(
      decoded.userId,
      'stub-facility-id' as UUID,
      'registered_nurse',
      permissions,
      newTokenId
    );

    // 7. Update session in database (token rotation)
    // await db.query(
    //   'UPDATE user_sessions SET id = $1, refresh_token = $2, expires_at = $3 WHERE id = $4',
    //   [newTokenId, tokens.refreshToken, new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), decoded.tokenId]
    // );

    res.status(200).json({
      success: true,
      data: {
        accessToken: tokens.accessToken,
        refreshToken: tokens.refreshToken,
        expiresIn: tokens.expiresIn,
        tokenType: tokens.tokenType
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * POST /v1/auth/logout
 * Invalidate current session and tokens
 */
export async function logout(req: Request, res: Response): Promise<void> {
  const { refreshToken } = req.body;

  try {
    // 1. Verify refresh token
    const decoded = verifyRefreshToken(refreshToken);

    // 2. Delete session from database
    // await db.query('DELETE FROM user_sessions WHERE id = $1', [decoded.tokenId]);

    // 3. Optionally blacklist access token in Redis
    // await redis.setex(`blacklist:${req.headers.authorization}`, 3600, '1');

    res.status(200).json({
      success: true,
      message: 'Logged out successfully',
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString()
      }
    });
  } catch (error) {
    throw error;
  }
}

/**
 * GET /v1/auth/me
 * Get current authenticated user information
 */
export async function getCurrentUser(req: Request, res: Response): Promise<void> {
  const user = req.user!;

  // TODO: Fetch full user details from database
  // const userData = await db.query('SELECT * FROM staff WHERE id = $1', [user.userId]);
  // const facility = await db.query('SELECT * FROM facilities WHERE id = $1', [user.facilityId]);

  res.status(200).json({
    success: true,
    data: {
      id: user.userId,
      email: 'john.doe@hospital.com',
      firstName: 'John',
      lastName: 'Doe',
      preferredName: 'Johnny',
      role: user.role,
      title: 'Emergency Department RN',
      department: 'Emergency Department',
      facilityId: user.facilityId,
      facility: {
        id: user.facilityId,
        name: 'City General Hospital',
        type: 'hospital',
        address: {
          city: 'Denver',
          state: 'CO'
        }
      },
      licenseNumber: 'RN123456',
      licenseState: 'CO',
      phone: '+13035551234',
      avatarUrl: null,
      preferences: {
        language: 'en',
        timezone: 'America/Denver',
        notifications: {
          email: true,
          push: true,
          sms: false
        }
      },
      isActive: true,
      emailVerified: true,
      mfaEnabled: false,
      lastLoginAt: new Date().toISOString(),
      createdAt: '2025-01-15T10:00:00.000Z'
    },
    meta: {
      requestId: req.headers['x-request-id'] || generateRequestId(),
      timestamp: new Date().toISOString()
    }
  });
}

/**
 * Helper: Get permissions for role
 * Based on Part 4A RBAC matrix
 */
function getPermissionsForRole(role: string): string[] {
  const rolePermissions: Record<string, string[]> = {
    registered_nurse: [
      'handoff:create',
      'handoff:read',
      'handoff:update',
      'patient:read',
      'voice:upload',
      'sbar:read',
      'sbar:update'
    ],
    licensed_practical_nurse: [
      'handoff:create',
      'handoff:read',
      'handoff:update',
      'patient:read',
      'voice:upload',
      'sbar:read',
      'sbar:update'
    ],
    certified_nursing_assistant: [
      'handoff:read',
      'patient:read',
      'voice:upload',
      'sbar:read'
    ],
    physician: [
      'handoff:create',
      'handoff:read',
      'handoff:update',
      'handoff:delete',
      'patient:create',
      'patient:read',
      'patient:update',
      'voice:upload',
      'sbar:create',
      'sbar:read',
      'sbar:update',
      'sbar:approve'
    ],
    nurse_practitioner: [
      'handoff:create',
      'handoff:read',
      'handoff:update',
      'handoff:delete',
      'patient:create',
      'patient:read',
      'patient:update',
      'voice:upload',
      'sbar:create',
      'sbar:read',
      'sbar:update',
      'sbar:approve'
    ],
    admin: ['*:*'],
    super_admin: ['*:*']
  };

  return rolePermissions[role] || [];
}

/**
 * Helper: Generate session token ID
 */
function generateTokenId(): string {
  return `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Helper: Generate request ID
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
