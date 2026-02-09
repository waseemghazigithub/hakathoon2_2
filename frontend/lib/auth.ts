import { User, AuthState } from './types';

// Initialize Better Auth client
// This is a simplified mock for demonstration purposes
// In a real implementation, you would use the actual Better Auth client

// Mock authentication functions
export const getCurrentUser = (): User | null => {
  if (typeof window === 'undefined') return null;

  const userData = localStorage.getItem('currentUser');
  if (!userData) return null;

  try {
    return JSON.parse(userData);
  } catch {
    return null;
  }
};

export const setUser = (user: User): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('currentUser', JSON.stringify(user));
  }
};

export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token);
  }
};

export const clearAuth = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
  }
};

export const isAuthenticated = (): boolean => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  return !!token;
};

export const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
};

// Mock auth state context
// AuthState moved to types.ts

export const initialAuthState: AuthState = {
  user: null,
  loading: false,
  error: null,
};