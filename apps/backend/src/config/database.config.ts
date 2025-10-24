/**
 * Database Configuration
 * PostgreSQL connection via pg Pool
 */

import { Pool, PoolClient, QueryResult, QueryResultRow } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

// Database connection configuration
const dbConfig = {
  connectionString: process.env.DATABASE_URL,
  // Connection pool settings
  max: 20, // Maximum number of clients in the pool
  idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
  connectionTimeoutMillis: 10000, // Return error after 10 seconds if can't connect
  // SSL configuration for production (Supabase requires SSL)
  ssl: process.env.NODE_ENV === 'production'
    ? { rejectUnauthorized: false }
    : false
};

/**
 * PostgreSQL connection pool
 * Singleton pattern for reusing connections
 */
class Database {
  private static instance: Database;
  private pool: Pool;

  private constructor() {
    this.pool = new Pool(dbConfig);

    // Log pool errors
    this.pool.on('error', (err) => {
      console.error('Unexpected database pool error:', err);
    });

    // Log successful connection
    this.pool.on('connect', () => {
      console.log('✅ New database connection established');
    });

    // Log removed connections
    this.pool.on('remove', () => {
      console.log('🔌 Database connection removed from pool');
    });
  }

  /**
   * Get singleton instance
   */
  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  /**
   * Execute a query with parameters
   * @param text SQL query string
   * @param params Query parameters
   * @returns Query result
   */
  public async query<T extends QueryResultRow = any>(
    text: string,
    params?: any[]
  ): Promise<QueryResult<T>> {
    const start = Date.now();
    try {
      const result = await this.pool.query<T>(text, params);
      const duration = Date.now() - start;

      // Log slow queries (> 100ms)
      if (duration > 100) {
        console.warn(`⚠️  Slow query (${duration}ms):`, text.substring(0, 100));
      }

      return result;
    } catch (error) {
      console.error('Database query error:', error);
      console.error('Query:', text);
      console.error('Params:', params);
      throw error;
    }
  }

  /**
   * Get a client from the pool for transaction support
   * Remember to release the client after use!
   */
  public async getClient(): Promise<PoolClient> {
    return await this.pool.connect();
  }

  /**
   * Execute multiple queries in a transaction
   * Automatically handles commit/rollback
   */
  public async transaction<T>(
    callback: (client: PoolClient) => Promise<T>
  ): Promise<T> {
    const client = await this.getClient();

    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  /**
   * Test database connection
   */
  public async healthCheck(): Promise<{
    status: 'healthy' | 'unhealthy';
    message: string;
    details?: any;
  }> {
    try {
      const result = await this.query('SELECT NOW() as current_time, version()');
      const poolStats = {
        total: this.pool.totalCount,
        idle: this.pool.idleCount,
        waiting: this.pool.waitingCount
      };

      return {
        status: 'healthy',
        message: 'Database connection successful',
        details: {
          currentTime: result.rows[0].current_time,
          version: result.rows[0].version,
          pool: poolStats
        }
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        message: `Database connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        details: { error }
      };
    }
  }

  /**
   * Get pool statistics
   */
  public getPoolStats() {
    return {
      total: this.pool.totalCount,
      idle: this.pool.idleCount,
      waiting: this.pool.waitingCount
    };
  }

  /**
   * Close all connections (for graceful shutdown)
   */
  public async close(): Promise<void> {
    console.log('🔒 Closing database connection pool...');
    await this.pool.end();
    console.log('✅ Database connection pool closed');
  }
}

// Export singleton instance
export const db = Database.getInstance();

// Export types for use in other files
export type { PoolClient, QueryResult, QueryResultRow } from 'pg';
