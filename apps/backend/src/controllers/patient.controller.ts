import { Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { db } from '../config/database.config';
import { NotFoundError, ValidationError } from '../middleware/error.middleware';
import { DBPatient } from '../types/database.types';

/**
 * Patient Controller
 * Handles patient management endpoints with full database integration
 */

/**
 * POST /v1/patients
 * Create a new patient
 */
export async function createPatient(req: Request, res: Response): Promise<void> {
  const {
    firstName,
    lastName,
    mrn,
    dateOfBirth,
    gender,
    bloodType,
    allergies,
    medicalHistory,
    primaryLanguage,
    emergencyContact,
    insuranceInfo,
  } = req.body;

  // Validation
  if (!firstName || !lastName || !mrn || !dateOfBirth || !gender) {
    throw new ValidationError(
      'Missing required fields: firstName, lastName, mrn, dateOfBirth, gender'
    );
  }

  try {
    // Check if MRN already exists in facility
    const existingPatient = await db.query<DBPatient>(
      'SELECT id FROM patients WHERE mrn = $1 AND facility_id = $2',
      [mrn, req.user!.facilityId]
    );

    if (existingPatient.rows.length > 0) {
      throw new ValidationError(`Patient with MRN ${mrn} already exists in this facility`);
    }

    // Create patient
    const patientId = uuidv4();
    const result = await db.query<DBPatient>(
      `INSERT INTO patients (
        id, facility_id, first_name, last_name, mrn, date_of_birth, gender,
        blood_type, allergies, medical_history, primary_language,
        emergency_contact, insurance_info, status, created_at, updated_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, NOW(), NOW())
      RETURNING *`,
      [
        patientId,
        req.user!.facilityId,
        firstName,
        lastName,
        mrn,
        dateOfBirth,
        gender,
        bloodType || null,
        allergies ? JSON.stringify(allergies) : null,
        medicalHistory || null,
        primaryLanguage || 'English',
        emergencyContact ? JSON.stringify(emergencyContact) : null,
        insuranceInfo ? JSON.stringify(insuranceInfo) : null,
        'active',
      ]
    );

    res.status(201).json({
      success: true,
      data: result.rows[0],
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    throw error;
  }
}

/**
 * GET /v1/patients
 * List all patients for facility with search and filters
 */
export async function listPatients(req: Request, res: Response): Promise<void> {
  const {
    search,
    status,
    limit = 50,
    offset = 0,
    sortBy = 'last_name',
    order = 'asc',
  } = req.query;

  try {
    // Build WHERE clause
    const conditions: string[] = ['facility_id = $1'];
    const params: any[] = [req.user!.facilityId];
    let paramIndex = 2;

    if (status) {
      conditions.push(`status = $${paramIndex}`);
      params.push(status);
      paramIndex++;
    }

    if (search) {
      conditions.push(`(
        first_name ILIKE $${paramIndex} OR
        last_name ILIKE $${paramIndex} OR
        mrn ILIKE $${paramIndex}
      )`);
      params.push(`%${search}%`);
      paramIndex++;
    }

    const whereClause = conditions.join(' AND ');

    // Valid sort columns
    const validSortColumns = ['first_name', 'last_name', 'mrn', 'date_of_birth', 'created_at'];
    const sortColumn = validSortColumns.includes(sortBy as string) ? sortBy : 'last_name';
    const sortOrder = order === 'desc' ? 'DESC' : 'ASC';

    // Get total count
    const countResult = await db.query(
      `SELECT COUNT(*) as total FROM patients WHERE ${whereClause}`,
      params
    );
    const total = parseInt(countResult.rows[0].total);

    // Get patients
    const result = await db.query<DBPatient>(
      `SELECT * FROM patients
       WHERE ${whereClause}
       ORDER BY ${sortColumn} ${sortOrder}
       LIMIT $${paramIndex} OFFSET $${paramIndex + 1}`,
      [...params, limit, offset]
    );

    res.status(200).json({
      success: true,
      data: result.rows,
      pagination: {
        total,
        limit: Number(limit),
        offset: Number(offset),
        hasMore: Number(offset) + result.rows.length < total,
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    throw error;
  }
}

/**
 * GET /v1/patients/:id
 * Get patient by ID with all details
 */
export async function getPatient(req: Request, res: Response): Promise<void> {
  const { id } = req.params;

  try {
    const result = await db.query<DBPatient>(
      'SELECT * FROM patients WHERE id = $1 AND facility_id = $2',
      [id, req.user!.facilityId]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('patient', id);
    }

    res.status(200).json({
      success: true,
      data: result.rows[0],
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    throw error;
  }
}

/**
 * PUT /v1/patients/:id
 * Update patient information
 */
export async function updatePatient(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const {
    firstName,
    lastName,
    dateOfBirth,
    gender,
    bloodType,
    allergies,
    medicalHistory,
    primaryLanguage,
    emergencyContact,
    insuranceInfo,
    status,
  } = req.body;

  try {
    // Verify patient exists and belongs to facility
    const existingPatient = await db.query<DBPatient>(
      'SELECT * FROM patients WHERE id = $1 AND facility_id = $2',
      [id, req.user!.facilityId]
    );

    if (existingPatient.rows.length === 0) {
      throw new NotFoundError('patient', id);
    }

    // Build UPDATE query dynamically
    const updates: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    if (firstName !== undefined) {
      updates.push(`first_name = $${paramIndex++}`);
      values.push(firstName);
    }
    if (lastName !== undefined) {
      updates.push(`last_name = $${paramIndex++}`);
      values.push(lastName);
    }
    if (dateOfBirth !== undefined) {
      updates.push(`date_of_birth = $${paramIndex++}`);
      values.push(dateOfBirth);
    }
    if (gender !== undefined) {
      updates.push(`gender = $${paramIndex++}`);
      values.push(gender);
    }
    if (bloodType !== undefined) {
      updates.push(`blood_type = $${paramIndex++}`);
      values.push(bloodType);
    }
    if (allergies !== undefined) {
      updates.push(`allergies = $${paramIndex++}`);
      values.push(allergies ? JSON.stringify(allergies) : null);
    }
    if (medicalHistory !== undefined) {
      updates.push(`medical_history = $${paramIndex++}`);
      values.push(medicalHistory);
    }
    if (primaryLanguage !== undefined) {
      updates.push(`primary_language = $${paramIndex++}`);
      values.push(primaryLanguage);
    }
    if (emergencyContact !== undefined) {
      updates.push(`emergency_contact = $${paramIndex++}`);
      values.push(emergencyContact ? JSON.stringify(emergencyContact) : null);
    }
    if (insuranceInfo !== undefined) {
      updates.push(`insurance_info = $${paramIndex++}`);
      values.push(insuranceInfo ? JSON.stringify(insuranceInfo) : null);
    }
    if (status !== undefined) {
      updates.push(`status = $${paramIndex++}`);
      values.push(status);
    }

    if (updates.length === 0) {
      throw new ValidationError('No fields to update');
    }

    updates.push(`updated_at = NOW()`);
    values.push(id);

    const result = await db.query<DBPatient>(
      `UPDATE patients SET ${updates.join(', ')} WHERE id = $${paramIndex} RETURNING *`,
      values
    );

    res.status(200).json({
      success: true,
      data: result.rows[0],
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    throw error;
  }
}

/**
 * GET /v1/patients/:id/handoffs
 * Get all handoffs for a patient with staff details
 */
export async function getPatientHandoffs(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const { limit = 50, offset = 0 } = req.query;

  try {
    // Verify patient exists and belongs to facility
    const patient = await db.query<DBPatient>(
      'SELECT * FROM patients WHERE id = $1 AND facility_id = $2',
      [id, req.user!.facilityId]
    );

    if (patient.rows.length === 0) {
      throw new NotFoundError('patient', id);
    }

    // Get handoffs with staff details
    const result = await db.query(
      `SELECT
        h.*,
        fs.first_name as from_staff_first_name,
        fs.last_name as from_staff_last_name,
        ts.first_name as to_staff_first_name,
        ts.last_name as to_staff_last_name
      FROM handoffs h
      LEFT JOIN staff fs ON h.from_staff_id = fs.id
      LEFT JOIN staff ts ON h.to_staff_id = ts.id
      WHERE h.patient_id = $1
      ORDER BY h.created_at DESC
      LIMIT $2 OFFSET $3`,
      [id, limit, offset]
    );

    res.status(200).json({
      success: true,
      data: result.rows,
      pagination: {
        limit: Number(limit),
        offset: Number(offset),
        hasMore: result.rows.length === Number(limit),
      },
      meta: {
        requestId: req.headers['x-request-id'] || generateRequestId(),
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    throw error;
  }
}

/**
 * Helper: Generate request ID
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
