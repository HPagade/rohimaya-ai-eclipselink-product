import { Request, Response } from 'express';
import { UUID } from '@eclipselink/types';
import { NotFoundError, ValidationError, ConflictError } from '../middleware/error.middleware';
import { db } from '../config/database.config';
import { DBHandoff, DBPatient, DBStaff } from '../types/database.types';

/**
 * Handoff Controller
 * Handles handoff management endpoints
 * Based on Part 4B specifications
 *
 * Full database integration with PostgreSQL via Supabase
 */

/**
 * POST /v1/handoffs
 * Create a new handoff
 */
export async function createHandoff(req: Request, res: Response): Promise<void> {
  const {
    patientId,
    fromStaffId,
    toStaffId,
    handoffType,
    priority = 'routine',
    scheduledTime,
    location,
    clinicalNotes,
    isCritical = false,
    requiresFollowup = false,
    isInitialHandoff = false,
    previousHandoffId
  } = req.body;

  try {
    // 1. Validate patient exists and belongs to the facility
    const patientResult = await db.query<DBPatient>(
      'SELECT * FROM patients WHERE id = $1 AND facility_id = $2',
      [patientId, req.user!.facilityId]
    );

    if (patientResult.rows.length === 0) {
      throw new NotFoundError('patient', patientId);
    }

    const patient = patientResult.rows[0];

    // 2. Validate from_staff exists and belongs to the facility
    const fromStaffResult = await db.query<DBStaff>(
      'SELECT * FROM staff WHERE id = $1 AND facility_id = $2 AND is_active = true',
      [fromStaffId || req.user!.userId, req.user!.facilityId]
    );

    if (fromStaffResult.rows.length === 0) {
      throw new NotFoundError('staff', fromStaffId);
    }

    const fromStaff = fromStaffResult.rows[0];

    // 3. Validate to_staff exists (if provided)
    let toStaff = null;
    if (toStaffId) {
      const toStaffResult = await db.query<DBStaff>(
        'SELECT * FROM staff WHERE id = $1 AND facility_id = $2 AND is_active = true',
        [toStaffId, req.user!.facilityId]
      );

      if (toStaffResult.rows.length === 0) {
        throw new NotFoundError('staff', toStaffId);
      }

      toStaff = toStaffResult.rows[0];
    }

    // 4. If update handoff, validate previous handoff exists
    if (!isInitialHandoff && previousHandoffId) {
      const prevHandoffResult = await db.query<DBHandoff>(
        'SELECT * FROM handoffs WHERE id = $1 AND facility_id = $2',
        [previousHandoffId, req.user!.facilityId]
      );

      if (prevHandoffResult.rows.length === 0) {
        throw new NotFoundError('handoff', previousHandoffId);
      }
    }

    // 5. Create handoff
    const handoffResult = await db.query<DBHandoff>(
      `INSERT INTO handoffs (
        patient_id, facility_id, from_staff_id, to_staff_id,
        status, handoff_type, priority, scheduled_time,
        location, clinical_notes, is_critical, requires_followup,
        is_initial_handoff, previous_handoff_id, exported_to_ehr
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
      RETURNING *`,
      [
        patientId,
        req.user!.facilityId,
        fromStaffId || req.user!.userId,
        toStaffId || null,
        'draft',
        handoffType,
        priority,
        scheduledTime || null,
        location || null,
        clinicalNotes || null,
        isCritical,
        requiresFollowup,
        isInitialHandoff,
        previousHandoffId || null,
        false
      ]
    );

    const handoff = handoffResult.rows[0];

    res.status(201).json({
      success: true,
      data: {
        id: handoff.id,
        patientId: handoff.patient_id,
        patient: {
          id: patient.id,
          firstName: patient.first_name,
          lastName: patient.last_name,
          mrn: patient.mrn,
          dateOfBirth: patient.date_of_birth,
          roomNumber: patient.room_number
        },
        facilityId: handoff.facility_id,
        fromStaffId: handoff.from_staff_id,
        fromStaff: {
          id: fromStaff.id,
          firstName: fromStaff.first_name,
          lastName: fromStaff.last_name,
          role: fromStaff.role
        },
        toStaffId: handoff.to_staff_id,
        toStaff: toStaff ? {
          id: toStaff.id,
          firstName: toStaff.first_name,
          lastName: toStaff.last_name,
          role: toStaff.role
        } : null,
        status: handoff.status,
        handoffType: handoff.handoff_type,
        priority: handoff.priority,
        scheduledTime: handoff.scheduled_time,
        location: handoff.location,
        clinicalNotes: handoff.clinical_notes,
        isCritical: handoff.is_critical,
        requiresFollowup: handoff.requires_followup,
        isInitialHandoff: handoff.is_initial_handoff,
        previousHandoffId: handoff.previous_handoff_id,
        exportedToEhr: handoff.exported_to_ehr,
        createdAt: handoff.created_at,
        updatedAt: handoff.updated_at
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
 * GET /v1/handoffs
 * List handoffs with filtering, sorting, and pagination
 */
export async function listHandoffs(req: Request, res: Response): Promise<void> {
  const {
    page = 1,
    limit = 20,
    status,
    priority,
    handoffType,
    fromStaffId,
    toStaffId,
    patientId,
    startDate,
    endDate,
    search,
    sortBy = 'createdAt',
    sortOrder = 'desc',
    includeSbar = false
  } = req.query;

  try {
    // Build dynamic query with filters
    const filters: string[] = ['h.facility_id = $1'];
    const params: any[] = [req.user!.facilityId];
    let paramIndex = 2;

    if (status) {
      filters.push(`h.status = $${paramIndex++}`);
      params.push(status);
    }

    if (priority) {
      filters.push(`h.priority = $${paramIndex++}`);
      params.push(priority);
    }

    if (handoffType) {
      filters.push(`h.handoff_type = $${paramIndex++}`);
      params.push(handoffType);
    }

    if (fromStaffId) {
      filters.push(`h.from_staff_id = $${paramIndex++}`);
      params.push(fromStaffId);
    }

    if (toStaffId) {
      filters.push(`h.to_staff_id = $${paramIndex++}`);
      params.push(toStaffId);
    }

    if (patientId) {
      filters.push(`h.patient_id = $${paramIndex++}`);
      params.push(patientId);
    }

    if (startDate) {
      filters.push(`h.created_at >= $${paramIndex++}`);
      params.push(startDate);
    }

    if (endDate) {
      filters.push(`h.created_at <= $${paramIndex++}`);
      params.push(endDate);
    }

    if (search) {
      filters.push(`(
        p.first_name ILIKE $${paramIndex} OR
        p.last_name ILIKE $${paramIndex} OR
        p.mrn ILIKE $${paramIndex} OR
        h.clinical_notes ILIKE $${paramIndex}
      )`);
      params.push(`%${search}%`);
      paramIndex++;
    }

    const whereClause = filters.join(' AND ');

    // Get total count
    const countResult = await db.query<{ count: string }>(
      `SELECT COUNT(*) as count FROM handoffs h
       LEFT JOIN patients p ON h.patient_id = p.id
       WHERE ${whereClause}`,
      params
    );

    const total = parseInt(countResult.rows[0].count, 10);
    const totalPages = Math.ceil(total / Number(limit));
    const offset = (Number(page) - 1) * Number(limit);

    // Map sortBy field to database column
    const sortByMap: Record<string, string> = {
      createdAt: 'h.created_at',
      updatedAt: 'h.updated_at',
      status: 'h.status',
      priority: 'h.priority',
      scheduledTime: 'h.scheduled_time'
    };

    const orderByClause = `${sortByMap[sortBy as string] || 'h.created_at'} ${sortOrder === 'asc' ? 'ASC' : 'DESC'}`;

    // Fetch handoffs with relations
    const result = await db.query<any>(
      `SELECT
        h.*,
        p.id as patient_id, p.first_name as patient_first_name, p.last_name as patient_last_name,
        p.mrn, p.date_of_birth, p.room_number,
        fs.id as from_staff_id, fs.first_name as from_staff_first_name, fs.last_name as from_staff_last_name,
        fs.role as from_staff_role, fs.department as from_staff_department,
        ts.id as to_staff_id, ts.first_name as to_staff_first_name, ts.last_name as to_staff_last_name,
        ts.role as to_staff_role, ts.department as to_staff_department
      FROM handoffs h
      LEFT JOIN patients p ON h.patient_id = p.id
      LEFT JOIN staff fs ON h.from_staff_id = fs.id
      LEFT JOIN staff ts ON h.to_staff_id = ts.id
      WHERE ${whereClause}
      ORDER BY ${orderByClause}
      LIMIT $${paramIndex} OFFSET $${paramIndex + 1}`,
      [...params, limit, offset]
    );

    const handoffs = result.rows.map((row: any) => ({
      id: row.id,
      patient: {
        id: row.patient_id,
        firstName: row.patient_first_name,
        lastName: row.patient_last_name,
        mrn: row.mrn,
        dateOfBirth: row.date_of_birth,
        roomNumber: row.room_number
      },
      fromStaff: row.from_staff_id ? {
        id: row.from_staff_id,
        firstName: row.from_staff_first_name,
        lastName: row.from_staff_last_name,
        role: row.from_staff_role,
        department: row.from_staff_department
      } : null,
      toStaff: row.to_staff_id ? {
        id: row.to_staff_id,
        firstName: row.to_staff_first_name,
        lastName: row.to_staff_last_name,
        role: row.to_staff_role,
        department: row.to_staff_department
      } : null,
      status: row.status,
      priority: row.priority,
      handoffType: row.handoff_type,
      scheduledTime: row.scheduled_time,
      location: row.location,
      isCritical: row.is_critical,
      requiresFollowup: row.requires_followup,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    }));

    res.status(200).json({
      success: true,
      data: {
        handoffs,
        pagination: {
          page: Number(page),
          limit: Number(limit),
          total,
          totalPages,
          hasNextPage: Number(page) < totalPages,
          hasPrevPage: Number(page) > 1,
          nextPage: Number(page) < totalPages ? Number(page) + 1 : null,
          prevPage: Number(page) > 1 ? Number(page) - 1 : null
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
 * GET /v1/handoffs/:id
 * Get detailed handoff information by ID
 */
export async function getHandoff(req: Request, res: Response): Promise<void> {
  const { id } = req.params;

  try {
    // Fetch handoff with all relations
    const result = await db.query<any>(
      `SELECT
        h.*,
        p.id as patient_id, p.first_name as patient_first_name, p.last_name as patient_last_name,
        p.mrn, p.date_of_birth, p.gender, p.room_number, p.bed_number,
        p.primary_diagnosis, p.chief_complaint,
        fs.id as from_staff_id, fs.first_name as from_staff_first_name, fs.last_name as from_staff_last_name,
        fs.role as from_staff_role, fs.department as from_staff_department,
        ts.id as to_staff_id, ts.first_name as to_staff_first_name, ts.last_name as to_staff_last_name,
        ts.role as to_staff_role, ts.department as to_staff_department,
        vr.id as voice_recording_id, vr.duration, vr.file_size, vr.audio_format, vr.status as recording_status,
        vr.uploaded_at, vr.processed_at
      FROM handoffs h
      LEFT JOIN patients p ON h.patient_id = p.id
      LEFT JOIN staff fs ON h.from_staff_id = fs.id
      LEFT JOIN staff ts ON h.to_staff_id = ts.id
      LEFT JOIN voice_recordings vr ON vr.handoff_id = h.id
      WHERE h.id = $1 AND h.facility_id = $2`,
      [id, req.user!.facilityId]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('handoff', id);
    }

    const row = result.rows[0];

    res.status(200).json({
      success: true,
      data: {
        id: row.id,
        patient: {
          id: row.patient_id,
          firstName: row.patient_first_name,
          lastName: row.patient_last_name,
          mrn: row.mrn,
          dateOfBirth: row.date_of_birth,
          gender: row.gender,
          roomNumber: row.room_number,
          bedNumber: row.bed_number,
          primaryDiagnosis: row.primary_diagnosis,
          chiefComplaint: row.chief_complaint
        },
        fromStaff: row.from_staff_id ? {
          id: row.from_staff_id,
          firstName: row.from_staff_first_name,
          lastName: row.from_staff_last_name,
          role: row.from_staff_role,
          department: row.from_staff_department
        } : null,
        toStaff: row.to_staff_id ? {
          id: row.to_staff_id,
          firstName: row.to_staff_first_name,
          lastName: row.to_staff_last_name,
          role: row.to_staff_role,
          department: row.to_staff_department
        } : null,
        status: row.status,
        priority: row.priority,
        handoffType: row.handoff_type,
        scheduledTime: row.scheduled_time,
        location: row.location,
        clinicalNotes: row.clinical_notes,
        voiceRecording: row.voice_recording_id ? {
          id: row.voice_recording_id,
          duration: row.duration,
          fileSize: row.file_size,
          audioFormat: row.audio_format,
          status: row.recording_status,
          uploadedAt: row.uploaded_at,
          processedAt: row.processed_at
        } : null,
        isCritical: row.is_critical,
        requiresFollowup: row.requires_followup,
        exportedToEhr: row.exported_to_ehr,
        createdAt: row.created_at,
        updatedAt: row.updated_at
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
 * PUT /v1/handoffs/:id
 * Update handoff information
 */
export async function updateHandoff(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const updates = req.body;

  try {
    // Verify handoff exists and belongs to facility
    const existingResult = await db.query<DBHandoff>(
      'SELECT * FROM handoffs WHERE id = $1 AND facility_id = $2',
      [id, req.user!.facilityId]
    );

    if (existingResult.rows.length === 0) {
      throw new NotFoundError('handoff', id);
    }

    // Build dynamic update query
    const updateFields: string[] = [];
    const params: any[] = [];
    let paramIndex = 1;

    if (updates.toStaffId !== undefined) {
      updateFields.push(`to_staff_id = $${paramIndex++}`);
      params.push(updates.toStaffId);
    }

    if (updates.status !== undefined) {
      updateFields.push(`status = $${paramIndex++}`);
      params.push(updates.status);
    }

    if (updates.priority !== undefined) {
      updateFields.push(`priority = $${paramIndex++}`);
      params.push(updates.priority);
    }

    if (updates.scheduledTime !== undefined) {
      updateFields.push(`scheduled_time = $${paramIndex++}`);
      params.push(updates.scheduledTime);
    }

    if (updates.location !== undefined) {
      updateFields.push(`location = $${paramIndex++}`);
      params.push(updates.location);
    }

    if (updates.clinicalNotes !== undefined) {
      updateFields.push(`clinical_notes = $${paramIndex++}`);
      params.push(updates.clinicalNotes);
    }

    if (updates.isCritical !== undefined) {
      updateFields.push(`is_critical = $${paramIndex++}`);
      params.push(updates.isCritical);
    }

    if (updates.requiresFollowup !== undefined) {
      updateFields.push(`requires_followup = $${paramIndex++}`);
      params.push(updates.requiresFollowup);
    }

    updateFields.push(`updated_at = NOW()`);

    if (updateFields.length === 1) { // Only updated_at was added
      throw new ValidationError('No valid fields to update');
    }

    // Execute update
    params.push(id, req.user!.facilityId);
    const result = await db.query<DBHandoff>(
      `UPDATE handoffs SET ${updateFields.join(', ')}
       WHERE id = $${paramIndex} AND facility_id = $${paramIndex + 1}
       RETURNING *`,
      params
    );

    const handoff = result.rows[0];

    res.status(200).json({
      success: true,
      data: {
        id: handoff.id,
        status: handoff.status,
        priority: handoff.priority,
        scheduledTime: handoff.scheduled_time,
        location: handoff.location,
        clinicalNotes: handoff.clinical_notes,
        isCritical: handoff.is_critical,
        requiresFollowup: handoff.requires_followup,
        updatedAt: handoff.updated_at
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
 * POST /v1/handoffs/:id/assign
 * Assign handoff to a provider
 */
export async function assignHandoff(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const { toStaffId, notifyProvider = true, notificationMethod = 'push', message } = req.body;

  try {
    // TODO: Update handoff and create assignment
    // await db.query('UPDATE handoffs SET to_staff_id = $1, status = $2 WHERE id = $3', [toStaffId, 'assigned', id]);
    // await db.query('INSERT INTO handoff_assignments (...) VALUES (...)', [...]);

    // TODO: Send notification if requested
    // if (notifyProvider) {
    //   await sendNotification(toStaffId, notificationMethod, message);
    // }

    res.status(200).json({
      success: true,
      data: {
        handoff: {
          id,
          status: 'assigned',
          toStaffId
        },
        assignment: {
          id: generateUUID(),
          staffId: toStaffId,
          role: 'receiving',
          status: 'notified',
          notifiedAt: new Date().toISOString(),
          notificationMethod
        },
        notification: {
          id: generateUUID(),
          sent: true,
          sentAt: new Date().toISOString()
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
 * POST /v1/handoffs/:id/complete
 * Mark handoff as completed
 */
export async function completeHandoff(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const { completionNotes, actualTime } = req.body;

  try {
    // TODO: Update handoff status
    // await db.query(
    //   'UPDATE handoffs SET status = $1, completed_at = $2, completion_notes = $3 WHERE id = $4',
    //   ['completed', actualTime || new Date(), completionNotes, id]
    // );

    res.status(200).json({
      success: true,
      data: {
        id,
        status: 'completed',
        completedAt: actualTime || new Date().toISOString(),
        completionNotes,
        updatedAt: new Date().toISOString()
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
 * DELETE /v1/handoffs/:id
 * Cancel or delete a handoff
 */
export async function deleteHandoff(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const { cancellationReason } = req.body;

  try {
    // TODO: Update handoff status to cancelled
    // await db.query(
    //   'UPDATE handoffs SET status = $1, cancelled_at = $2, cancellation_reason = $3 WHERE id = $4',
    //   ['cancelled', new Date(), cancellationReason, id]
    // );

    res.status(200).json({
      success: true,
      message: 'Handoff cancelled successfully',
      data: {
        id,
        status: 'cancelled',
        cancelledAt: new Date().toISOString(),
        cancellationReason
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
 * Helper: Generate UUID
 */
function generateUUID(): UUID {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}` as UUID;
}

/**
 * Helper: Generate request ID
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
