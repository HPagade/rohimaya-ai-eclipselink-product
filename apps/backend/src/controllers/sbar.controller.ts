import { Request, Response } from 'express';
import { UUID } from '@eclipselink/types';
import { NotFoundError, ValidationError } from '../middleware/error.middleware';
import { db } from '../config/database.config';
import { DBSbarReport, DBHandoff, DBPatient } from '../types/database.types';

/**
 * SBAR Controller
 * Handles SBAR report endpoints
 * Based on Part 4C specifications
 *
 * Complete implementation with:
 * - PostgreSQL database queries
 * - Version history tracking
 * - Change detection between versions
 * - Manual editing support
 */

/**
 * GET /v1/sbar/:handoffId
 * Get SBAR report for a specific handoff
 */
export async function getSbar(req: Request, res: Response): Promise<void> {
  const { handoffId } = req.params;

  try {
    // Fetch latest SBAR report with patient and handoff details
    const result = await db.query<any>(
      `SELECT
        sr.*,
        h.id as handoff_id,
        h.status as handoff_status,
        h.handoff_type,
        h.priority,
        p.id as patient_id,
        p.first_name,
        p.last_name,
        p.mrn,
        p.date_of_birth,
        p.gender
      FROM sbar_reports sr
      JOIN handoffs h ON sr.handoff_id = h.id
      JOIN patients p ON sr.patient_id = p.id
      WHERE sr.handoff_id = $1 AND h.facility_id = $2
      ORDER BY sr.version DESC
      LIMIT 1`,
      [handoffId, req.user!.facilityId]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('sbar_report', handoffId);
    }

    const sbar = result.rows[0];

    res.status(200).json({
      success: true,
      data: {
        id: sbar.id,
        handoffId: sbar.handoff_id,
        patientId: sbar.patient_id,
        patient: {
          firstName: sbar.first_name,
          lastName: sbar.last_name,
          mrn: sbar.mrn,
          dateOfBirth: sbar.date_of_birth,
          gender: sbar.gender
        },
        version: sbar.version,
        previousVersionId: sbar.previous_version_id,
        isLatest: true, // Always true since we fetch latest
        isInitial: sbar.is_initial,
        situation: sbar.situation,
        background: sbar.background,
        assessment: sbar.assessment,
        recommendation: sbar.recommendation,
        changesSinceLastVersion: sbar.changes_since_last_version || [],
        qualityMetrics: {
          completenessScore: sbar.completeness_score,
          readabilityScore: sbar.readability_score,
          adherenceToIPassFramework: sbar.adherence_to_ipass_framework,
          criticalInfoPresent: sbar.critical_info_present
        },
        aiGeneration: {
          model: sbar.ai_model_used,
          generationType: sbar.is_initial ? 'initial' : 'update',
          promptTokens: sbar.prompt_tokens,
          completionTokens: sbar.completion_tokens,
          totalTokens: sbar.total_tokens,
          processingDuration: sbar.generation_duration_ms,
          confidenceScore: sbar.completeness_score // Use completeness as proxy
        },
        editHistory: sbar.edit_history || [],
        status: sbar.status,
        handoffDetails: {
          type: sbar.handoff_type,
          priority: sbar.priority,
          status: sbar.handoff_status
        },
        createdAt: sbar.created_at,
        updatedAt: sbar.updated_at
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
 * GET /v1/sbar/:handoffId/versions
 * Get all SBAR versions for a patient's handoff chain
 */
export async function getSbarVersions(req: Request, res: Response): Promise<void> {
  const { handoffId } = req.params;
  const { includeChanges = true } = req.query;

  try {
    // 1. Get current handoff to find patient
    const handoffResult = await db.query<DBHandoff>(
      'SELECT * FROM handoffs WHERE id = $1 AND facility_id = $2',
      [handoffId, req.user!.facilityId]
    );

    if (handoffResult.rows.length === 0) {
      throw new NotFoundError('handoff', handoffId);
    }

    const handoff = handoffResult.rows[0];
    const patientId = handoff.patient_id;

    // 2. Get patient details
    const patientResult = await db.query<DBPatient>(
      'SELECT * FROM patients WHERE id = $1',
      [patientId]
    );

    if (patientResult.rows.length === 0) {
      throw new NotFoundError('patient', patientId);
    }

    const patient = patientResult.rows[0];

    // 3. Get all SBAR reports for this patient, ordered by version
    const versionsResult = await db.query<any>(
      `SELECT
        sr.*,
        h.id as handoff_id,
        s.first_name,
        s.last_name,
        s.role
      FROM sbar_reports sr
      JOIN handoffs h ON sr.handoff_id = h.id
      LEFT JOIN staff s ON h.from_staff_id = s.id
      WHERE sr.patient_id = $1 AND h.facility_id = $2
      ORDER BY sr.version ASC`,
      [patientId, req.user!.facilityId]
    );

    const versions = versionsResult.rows;

    // 4. Build version tree
    const initialVersion = versions.find(v => v.is_initial);
    const updateVersions = versions.filter(v => !v.is_initial);
    const currentVersion = versions[versions.length - 1];

    // 5. Calculate days since initial
    let daysSinceInitial = 0;
    if (initialVersion && currentVersion) {
      const initial = new Date(initialVersion.created_at);
      const current = new Date(currentVersion.created_at);
      daysSinceInitial = Math.floor((current.getTime() - initial.getTime()) / (1000 * 60 * 60 * 24));
    }

    // 6. Format versions for response
    const formattedVersions = versions.map((v, index) => {
      const changeCount = v.changes_since_last_version
        ? (Array.isArray(v.changes_since_last_version) ? v.changes_since_last_version.length : 0)
        : null;

      // Create summary from first 80 chars of situation
      const summary = v.situation
        ? (v.situation.length > 80 ? v.situation.substring(0, 77) + '...' : v.situation)
        : 'No summary available';

      return {
        version: v.version,
        id: v.id,
        handoffId: v.handoff_id,
        isLatest: index === versions.length - 1,
        isInitial: v.is_initial,
        createdAt: v.created_at,
        createdBy: v.first_name && v.last_name
          ? `${v.first_name} ${v.last_name}${v.role ? ` (${v.role})` : ''}`
          : 'Unknown',
        summary,
        changeCount
      };
    });

    res.status(200).json({
      success: true,
      data: {
        patient: {
          id: patient.id,
          firstName: patient.first_name,
          lastName: patient.last_name,
          mrn: patient.mrn,
          dateOfBirth: patient.date_of_birth,
          gender: patient.gender
        },
        versions: formattedVersions,
        versionTree: {
          initial: initialVersion?.id || null,
          updates: updateVersions.map(v => v.id),
          current: currentVersion?.id || null
        },
        totalVersions: versions.length,
        daysSinceInitial
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
 * GET /v1/sbar/:id/compare
 * Compare two SBAR versions to see what changed
 */
export async function compareSbar(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const { compareWith } = req.query;

  try {
    if (!compareWith) {
      throw new ValidationError('compareWith query parameter is required');
    }

    // Fetch both SBAR versions
    const result = await db.query<DBSbarReport>(
      `SELECT * FROM sbar_reports
       WHERE id IN ($1, $2)
       ORDER BY version ASC`,
      [compareWith, id]
    );

    if (result.rows.length !== 2) {
      throw new NotFoundError('sbar_report', 'One or both SBAR versions not found');
    }

    const [fromSbar, toSbar] = result.rows;

    // Verify they're for the same patient
    if (fromSbar.patient_id !== toSbar.patient_id) {
      throw new ValidationError('Cannot compare SBAR reports from different patients');
    }

    // Verify facility access
    const facilityCheck = await db.query(
      `SELECT h.facility_id FROM handoffs h
       WHERE h.id IN ($1, $2)`,
      [fromSbar.handoff_id, toSbar.handoff_id]
    );

    if (facilityCheck.rows.length === 0 ||
        facilityCheck.rows.some(r => r.facility_id !== req.user!.facilityId)) {
      throw new NotFoundError('sbar_report', 'Access denied');
    }

    // Calculate comparison metadata
    const fromDate = new Date(fromSbar.created_at);
    const toDate = new Date(toSbar.created_at);
    const daysSpan = Math.floor((toDate.getTime() - fromDate.getTime()) / (1000 * 60 * 60 * 24));
    const versionSpan = toSbar.version - fromSbar.version;

    // Compare sections
    const changes: any[] = [];

    // Helper function to detect section changes
    const compareSection = (sectionName: string, fromText: string, toText: string) => {
      if (fromText !== toText) {
        // Simple change detection - in production you'd use diff algorithms
        const changeLength = Math.abs(toText.length - fromText.length);
        const significance = changeLength > 100 ? 'high' : changeLength > 30 ? 'medium' : 'low';

        changes.push({
          section: sectionName,
          changeType: toText.length > fromText.length ? 'expanded' : 'condensed',
          from: fromText.substring(0, 150) + (fromText.length > 150 ? '...' : ''),
          to: toText.substring(0, 150) + (toText.length > 150 ? '...' : ''),
          significance
        });
      }
    };

    compareSection('situation', fromSbar.situation, toSbar.situation);
    compareSection('background', fromSbar.background, toSbar.background);
    compareSection('assessment', fromSbar.assessment, toSbar.assessment);
    compareSection('recommendation', fromSbar.recommendation, toSbar.recommendation);

    // Add changes from toSbar's tracked changes
    if (toSbar.changes_since_last_version && Array.isArray(toSbar.changes_since_last_version)) {
      toSbar.changes_since_last_version.forEach(change => {
        changes.push({
          section: change.section || 'unknown',
          field: change.field || 'general',
          changeType: change.type || 'update',
          from: change.previousValue || 'N/A',
          to: change.newValue || 'N/A',
          significance: 'high',
          timestamp: change.timestamp
        });
      });
    }

    // Determine improvement trend
    const qualityDiff = (toSbar.completeness_score || 0) - (fromSbar.completeness_score || 0);
    const improvementTrend = qualityDiff > 0.05 ? 'positive' : qualityDiff < -0.05 ? 'negative' : 'stable';

    res.status(200).json({
      success: true,
      data: {
        comparison: {
          fromVersion: {
            id: fromSbar.id,
            version: fromSbar.version,
            date: fromSbar.created_at,
            isInitial: fromSbar.is_initial
          },
          toVersion: {
            id: toSbar.id,
            version: toSbar.version,
            date: toSbar.created_at,
            isInitial: toSbar.is_initial
          },
          versionSpan,
          daysSpan
        },
        changes,
        summary: {
          totalChanges: changes.length,
          improvementTrend,
          qualityScoreChange: {
            completeness: (toSbar.completeness_score || 0) - (fromSbar.completeness_score || 0),
            readability: (toSbar.readability_score || 0) - (fromSbar.readability_score || 0)
          },
          clinicalSignificance: changes.length > 0
            ? `${changes.length} change${changes.length > 1 ? 's' : ''} detected over ${daysSpan} day${daysSpan !== 1 ? 's' : ''} and ${versionSpan} version${versionSpan !== 1 ? 's' : ''}.`
            : 'No significant changes detected.'
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
 * PUT /v1/sbar/:id
 * Edit SBAR report
 */
export async function updateSbar(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const { situation, background, assessment, recommendation, editSummary, section } = req.body;

  try {
    // Validate at least one section is being updated
    if (!situation && !background && !assessment && !recommendation) {
      throw new ValidationError('At least one section must be provided for update');
    }

    // Fetch current SBAR to verify access and get current data
    const currentResult = await db.query<DBSbarReport>(
      `SELECT sr.*, h.facility_id
       FROM sbar_reports sr
       JOIN handoffs h ON sr.handoff_id = h.id
       WHERE sr.id = $1`,
      [id]
    );

    if (currentResult.rows.length === 0) {
      throw new NotFoundError('sbar_report', id);
    }

    const currentSbar = currentResult.rows[0];

    // Verify facility access
    if (currentSbar.facility_id !== req.user!.facilityId) {
      throw new NotFoundError('sbar_report', 'Access denied');
    }

    // Get staff details for audit log
    const staffResult = await db.query(
      'SELECT first_name, last_name, role FROM staff WHERE id = $1',
      [req.user!.userId]
    );

    const staff = staffResult.rows[0];
    const staffName = staff ? `${staff.first_name} ${staff.last_name}` : 'Unknown';

    // Build edit history entry
    const editHistoryEntry = {
      editedAt: new Date().toISOString(),
      editedBy: {
        id: req.user!.userId,
        name: staffName,
        role: staff?.role || 'unknown'
      },
      editSummary: editSummary || 'Manual edit',
      changes: [] as any[]
    };

    // Track what changed
    if (situation && situation !== currentSbar.situation) {
      editHistoryEntry.changes.push({
        section: 'situation',
        previousValue: currentSbar.situation.substring(0, 100) + '...',
        newValue: situation.substring(0, 100) + '...'
      });
    }
    if (background && background !== currentSbar.background) {
      editHistoryEntry.changes.push({
        section: 'background',
        previousValue: currentSbar.background.substring(0, 100) + '...',
        newValue: background.substring(0, 100) + '...'
      });
    }
    if (assessment && assessment !== currentSbar.assessment) {
      editHistoryEntry.changes.push({
        section: 'assessment',
        previousValue: currentSbar.assessment.substring(0, 100) + '...',
        newValue: assessment.substring(0, 100) + '...'
      });
    }
    if (recommendation && recommendation !== currentSbar.recommendation) {
      editHistoryEntry.changes.push({
        section: 'recommendation',
        previousValue: currentSbar.recommendation.substring(0, 100) + '...',
        newValue: recommendation.substring(0, 100) + '...'
      });
    }

    // Append to existing edit history
    const existingHistory = currentSbar.edit_history || [];
    const newEditHistory = [...existingHistory, editHistoryEntry];

    // Build UPDATE query dynamically
    const updates: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    if (situation) {
      updates.push(`situation = $${paramIndex++}`);
      values.push(situation);
    }
    if (background) {
      updates.push(`background = $${paramIndex++}`);
      values.push(background);
    }
    if (assessment) {
      updates.push(`assessment = $${paramIndex++}`);
      values.push(assessment);
    }
    if (recommendation) {
      updates.push(`recommendation = $${paramIndex++}`);
      values.push(recommendation);
    }

    // Always update edit_history and updated_at
    updates.push(`edit_history = $${paramIndex++}`);
    values.push(JSON.stringify(newEditHistory));
    updates.push(`updated_at = NOW()`);

    // Add WHERE clause
    values.push(id);

    // Execute update
    const updateQuery = `
      UPDATE sbar_reports
      SET ${updates.join(', ')}
      WHERE id = $${paramIndex}
      RETURNING *
    `;

    const updateResult = await db.query<DBSbarReport>(updateQuery, values);
    const updatedSbar = updateResult.rows[0];

    res.status(200).json({
      success: true,
      data: {
        id: updatedSbar.id,
        version: updatedSbar.version,
        situation: updatedSbar.situation,
        background: updatedSbar.background,
        assessment: updatedSbar.assessment,
        recommendation: updatedSbar.recommendation,
        editSummary,
        editedBy: {
          id: req.user!.userId,
          name: staffName,
          role: staff?.role || 'unknown'
        },
        editedAt: new Date().toISOString(),
        updatedAt: updatedSbar.updated_at,
        editHistory: newEditHistory
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
 * POST /v1/sbar/:id/export
 * Export SBAR report to various formats
 */
export async function exportSbar(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const {
    format,
    includePatientPhoto = false,
    includeVitalSigns = true,
    includeChangeHistory = true,
    includeAllVersions = false
  } = req.body;

  try {
    // Validate format
    const validFormats = ['pdf', 'docx', 'txt', 'json'];
    if (!format || !validFormats.includes(format)) {
      throw new ValidationError(`Format must be one of: ${validFormats.join(', ')}`);
    }

    // Fetch SBAR report with all related data
    const result = await db.query<any>(
      `SELECT
        sr.*,
        h.id as handoff_id,
        h.handoff_type,
        h.priority,
        h.facility_id,
        p.id as patient_id,
        p.first_name,
        p.last_name,
        p.mrn,
        p.date_of_birth,
        p.gender,
        f.name as facility_name
      FROM sbar_reports sr
      JOIN handoffs h ON sr.handoff_id = h.id
      JOIN patients p ON sr.patient_id = p.id
      JOIN facilities f ON h.facility_id = f.id
      WHERE sr.id = $1`,
      [id]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('sbar_report', id);
    }

    const sbar = result.rows[0];

    // Verify facility access
    if (sbar.facility_id !== req.user!.facilityId) {
      throw new NotFoundError('sbar_report', 'Access denied');
    }

    // Build export data
    const exportData: any = {
      report: {
        id: sbar.id,
        version: sbar.version,
        isInitial: sbar.is_initial,
        generatedAt: sbar.created_at,
        exportedAt: new Date().toISOString(),
        exportedBy: req.user!.userId
      },
      patient: {
        firstName: sbar.first_name,
        lastName: sbar.last_name,
        fullName: `${sbar.first_name} ${sbar.last_name}`,
        mrn: sbar.mrn,
        dateOfBirth: sbar.date_of_birth,
        gender: sbar.gender
      },
      facility: {
        name: sbar.facility_name
      },
      handoff: {
        type: sbar.handoff_type,
        priority: sbar.priority
      },
      sbar: {
        situation: sbar.situation,
        background: sbar.background,
        assessment: sbar.assessment,
        recommendation: sbar.recommendation
      },
      qualityMetrics: {
        completenessScore: sbar.completeness_score,
        readabilityScore: sbar.readability_score,
        adherenceToIPassFramework: sbar.adherence_to_ipass_framework,
        criticalInfoPresent: sbar.critical_info_present
      },
      aiGeneration: {
        model: sbar.ai_model_used,
        tokens: sbar.total_tokens,
        processingDuration: sbar.generation_duration_ms
      }
    };

    // Optionally include change history
    if (includeChangeHistory && sbar.changes_since_last_version) {
      exportData.changeHistory = sbar.changes_since_last_version;
    }

    // Optionally include all versions
    if (includeAllVersions) {
      const versionsResult = await db.query<DBSbarReport>(
        `SELECT * FROM sbar_reports
         WHERE patient_id = $1
         ORDER BY version ASC`,
        [sbar.patient_id]
      );

      exportData.allVersions = versionsResult.rows.map(v => ({
        version: v.version,
        isInitial: v.is_initial,
        createdAt: v.created_at,
        situation: v.situation,
        background: v.background,
        assessment: v.assessment,
        recommendation: v.recommendation
      }));
    }

    // Generate file name
    const timestamp = Date.now();
    const patientName = `${sbar.last_name}_${sbar.first_name}`.replace(/[^a-zA-Z0-9_-]/g, '_');
    const fileName = `SBAR_${patientName}_MRN${sbar.mrn}_v${sbar.version}_${timestamp}.${format}`;
    const exportId = `export_${timestamp}_${Math.random().toString(36).substr(2, 9)}`;

    // TODO: In production, generate actual file using PDF/DOCX library
    // For now, we'll simulate the export preparation
    // const fileBuffer = await generateExportFile(exportData, format);
    // const uploadResult = await storageService.uploadFile({
    //   fileName,
    //   fileBuffer,
    //   contentType: getContentType(format),
    //   metadata: {
    //     'export-id': exportId,
    //     'sbar-id': id,
    //     'patient-mrn': sbar.mrn
    //   }
    // }, req.user!.facilityId, sbar.handoff_id);
    // const presignedUrl = await storageService.getPresignedUrl(uploadResult.fileKey, { expiresIn: 3600 });

    // For MVP, return export data structure
    const mockUrl = `https://eclipselink-production.r2.cloudflarestorage.com/exports/sbar-reports/${fileName}?signature=mock`;

    // Calculate estimated file size based on format and content
    const contentSize = JSON.stringify(exportData).length;
    const estimatedFileSize = format === 'pdf' ? contentSize * 2 :
                              format === 'docx' ? contentSize * 1.5 :
                              format === 'json' ? contentSize :
                              contentSize * 0.8;

    res.status(200).json({
      success: true,
      data: {
        exportId,
        format,
        downloadUrl: mockUrl, // In production: presignedUrl
        expiresAt: new Date(Date.now() + 3600 * 1000).toISOString(),
        expiresIn: 3600,
        fileSize: Math.floor(estimatedFileSize),
        fileName,
        exportData: format === 'json' ? exportData : undefined, // Return raw data for JSON exports
        options: {
          includePatientPhoto,
          includeVitalSigns,
          includeChangeHistory,
          includeAllVersions
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
 * Helper: Generate request ID
 */
function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
