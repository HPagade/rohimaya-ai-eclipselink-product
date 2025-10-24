import axios, { AxiosInstance, AxiosError } from 'axios';

interface APIConfig {
  baseURL: string;
  timeout?: number;
}

interface TokenStorage {
  accessToken: string | null;
  refreshToken: string | null;
}

class EclipseLinkAPI {
  private client: AxiosInstance;
  private tokens: TokenStorage = {
    accessToken: null,
    refreshToken: null,
  };

  constructor(config: APIConfig) {
    this.client = axios.create({
      baseURL: config.baseURL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1',
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.tokens.accessToken) {
          config.headers.Authorization = `Bearer ${this.tokens.accessToken}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        // Handle 401 - try to refresh token
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            await this.refreshAccessToken();
            return this.client(originalRequest);
          } catch (refreshError) {
            this.handleAuthFailure();
            return Promise.reject(refreshError);
          }
        }

        // Handle 429 - rate limit
        if (error.response?.status === 429) {
          const retryAfter = error.response.headers['retry-after'] || 60;
          await this.delay(parseInt(retryAfter as string) * 1000);
          return this.client(originalRequest);
        }

        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', {
      email,
      password,
    });

    this.tokens.accessToken = response.data.data.tokens.accessToken;
    this.tokens.refreshToken = response.data.data.tokens.refreshToken;

    // Store in localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('accessToken', this.tokens.accessToken);
      localStorage.setItem('refreshToken', this.tokens.refreshToken!);
    }

    return response.data.data.user;
  }

  async register(data: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    role: string;
    facilityId: string;
  }) {
    const response = await this.client.post('/auth/register', data);
    return response.data.data;
  }

  async refreshAccessToken() {
    if (!this.tokens.refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await this.client.post('/auth/refresh', {
      refreshToken: this.tokens.refreshToken,
    });

    this.tokens.accessToken = response.data.data.accessToken;
    this.tokens.refreshToken = response.data.data.refreshToken;

    if (typeof window !== 'undefined') {
      localStorage.setItem('accessToken', this.tokens.accessToken);
      localStorage.setItem('refreshToken', this.tokens.refreshToken!);
    }
  }

  async logout() {
    try {
      await this.client.post('/auth/logout', {
        refreshToken: this.tokens.refreshToken,
      });
    } finally {
      this.tokens.accessToken = null;
      this.tokens.refreshToken = null;
      if (typeof window !== 'undefined') {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }
    }
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data.data;
  }

  // Handoffs
  async createHandoff(data: any) {
    const response = await this.client.post('/handoffs', data);
    return response.data.data;
  }

  async getHandoffs(params?: any) {
    const response = await this.client.get('/handoffs', { params });
    return response.data.data;
  }

  async getHandoff(handoffId: string) {
    const response = await this.client.get(`/handoffs/${handoffId}`);
    return response.data.data;
  }

  async updateHandoff(handoffId: string, data: any) {
    const response = await this.client.put(`/handoffs/${handoffId}`, data);
    return response.data.data;
  }

  async completeHandoff(handoffId: string, completionNotes: string) {
    const response = await this.client.post(`/handoffs/${handoffId}/complete`, {
      completionNotes,
    });
    return response.data.data;
  }

  // Voice Recording
  async uploadVoiceRecording(
    handoffId: string,
    audioBlob: Blob,
    duration: number,
    onProgress?: (progress: number) => void
  ) {
    const formData = new FormData();
    formData.append('handoffId', handoffId);
    formData.append('audio', audioBlob, 'recording.webm');
    formData.append('duration', duration.toString());

    const response = await this.client.post('/voice/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    });

    return response.data.data;
  }

  async getVoiceStatus(recordingId: string) {
    const response = await this.client.get(`/voice/${recordingId}/status`);
    return response.data.data;
  }

  async pollVoiceStatus(
    recordingId: string,
    onUpdate?: (status: any) => void
  ): Promise<any> {
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes max

    const getDelay = (attempt: number): number => {
      if (attempt < 15) return 2000; // 2s for first 30s
      if (attempt < 24) return 5000; // 5s for next 45s
      if (attempt < 36) return 10000; // 10s for next 2min
      return 15000; // 15s after that
    };

    while (attempts < maxAttempts) {
      const status = await this.getVoiceStatus(recordingId);

      if (onUpdate) {
        onUpdate(status);
      }

      if (status.status === 'transcribed' || status.status === 'failed') {
        return status;
      }

      attempts++;
      await this.delay(getDelay(attempts));
    }

    throw new Error('Voice processing timeout after 5 minutes');
  }

  // Patients
  async getPatients(params?: any) {
    const response = await this.client.get('/patients', { params });
    return response.data.data;
  }

  async getPatient(patientId: string) {
    const response = await this.client.get(`/patients/${patientId}`);
    return response.data.data;
  }

  async getPatientHandoffs(patientId: string, params?: any) {
    const response = await this.client.get(`/patients/${patientId}/handoffs`, {
      params,
    });
    return response.data.data;
  }

  // SBAR
  async getSbar(handoffId: string) {
    const response = await this.client.get(`/sbar/${handoffId}`);
    return response.data.data;
  }

  async getSbarVersions(handoffId: string) {
    const response = await this.client.get(`/sbar/${handoffId}/versions`);
    return response.data.data;
  }

  async updateSbar(sbarId: string, data: any) {
    const response = await this.client.put(`/sbar/${sbarId}`, data);
    return response.data.data;
  }

  async exportSbar(sbarId: string, format: 'pdf' | 'docx' | 'txt') {
    const response = await this.client.post(`/sbar/${sbarId}/export`, {
      format,
    });
    return response.data.data;
  }

  // Utilities
  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private handleAuthFailure() {
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  }

  // Set tokens (for hydrating from localStorage)
  setTokens(accessToken: string, refreshToken: string) {
    this.tokens.accessToken = accessToken;
    this.tokens.refreshToken = refreshToken;
  }
}

// Export singleton instance
export const api = new EclipseLinkAPI({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1',
});

// Hydrate tokens from localStorage on init
if (typeof window !== 'undefined') {
  const accessToken = localStorage.getItem('accessToken');
  const refreshToken = localStorage.getItem('refreshToken');
  if (accessToken && refreshToken) {
    api.setTokens(accessToken, refreshToken);
  }
}
