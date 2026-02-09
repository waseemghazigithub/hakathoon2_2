import { Task, TaskResponse, AuthResponse, DashboardStats } from './types';

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// Utility function to get JWT token
const getToken = (): string | null => {
  // In a real app, this would come from Better Auth
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

// Utility function to create headers with JWT test
const getAuthHeaders = (): HeadersInit => {
  const token = getToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};

// Centralized API function with error handling
const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  // Ensure we don't have double slashes if API_BASE_URL has a trailing slash
  const base = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${base}${path}`;
  
  const config: RequestInit = {
    headers: getAuthHeaders(),
    ...options,
  };

  try {
    const response = await fetch(url, config);

    if (response.status === 401) {
      localStorage.removeItem('token');
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/login';
      }
      throw new Error('Session expired. Please log in again.');
    }

    const data = await response.json().catch(() => ({}));
    
    if (!response.ok) {
      throw new Error(data.error || data.message || `Server Error: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error(`❌ API request failed: ${url}`, error);
    // If it's a TypeError, it's usually a network error (like CORS or offline)
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new Error('Cannot connect to the backend. Please check if the API URL is correct and backend is running.');
    }
    throw error;
  }
};

// AUTHENTICATION FUNCTIONS
export const login = async (email: string, password: string): Promise<AuthResponse> => {
  return apiRequest<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
};

export const register = async (email: string, password: string, name: string): Promise<AuthResponse> => {
  return apiRequest<AuthResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password, name }),
  });
};

// TASK MANAGEMENT FUNCTIONS
export const getTasks = async (): Promise<TaskResponse> => {
  return apiRequest<TaskResponse>('/tasks', {
    method: 'GET',
  });
};

export const createTask = async (taskData: { title: string; description?: string }): Promise<TaskResponse> => {
  return apiRequest<TaskResponse>('/tasks', {
    method: 'POST',
    body: JSON.stringify(taskData),
  });
};

export const updateTask = async (id: string, taskData: Partial<Task>): Promise<TaskResponse> => {
  return apiRequest<TaskResponse>(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  });
};

export const deleteTask = async (id: string): Promise<{ success: boolean; message: string }> => {
  return apiRequest<{ success: boolean; message: string }>(`/tasks/${id}`, {
    method: 'DELETE',
  });
};

export const toggleTaskCompletion = async (id: string): Promise<TaskResponse> => {
  return apiRequest<TaskResponse>(`/tasks/${id}/toggle-complete`, {
    method: 'PATCH',
  });
};

export const getDashboardStats = async (): Promise<DashboardStats> => {
  return apiRequest<DashboardStats>('/tasks/stats', {
    method: 'GET',
  });
};

// Generic error handler
export const handleApiError = (error: any): string => {
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred';
};