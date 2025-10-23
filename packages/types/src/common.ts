/**
 * Common types and utilities
 */

export type Nullable<T> = T | null;

export type Optional<T> = T | undefined;

export type UUID = string;

export type Timestamp = Date | string;

export interface PaginationParams {
  page?: number;
  limit?: number;
  sort?: string;
  order?: 'asc' | 'desc';
}

export interface FilterParams {
  search?: string;
  status?: string;
  facility_id?: string;
  date_from?: string;
  date_to?: string;
}

export interface ListResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}
