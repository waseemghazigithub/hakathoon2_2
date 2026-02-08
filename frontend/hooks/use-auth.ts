import { useState, useEffect } from 'react';
import { User, AuthState } from '../lib/types';
import { getCurrentUser, isAuthenticated, clearAuth } from '../lib/auth';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        if (isAuthenticated()) {
          const user = getCurrentUser();
          setAuthState({
            user: user || null,
            loading: false,
            error: null,
          });
        } else {
          setAuthState({
            user: null,
            loading: false,
            error: null,
          });
        }
      } catch (error) {
        setAuthState({
          user: null,
          loading: false,
          error: (error as Error).message || 'Error checking auth status',
        });
      }
    };

    checkAuthStatus();

    // Listen for storage changes (e.g., from other tabs)
    const handleStorageChange = () => {
      checkAuthStatus();
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const login = async (userData: User, token: string) => {
    try {
      localStorage.setItem('token', token);
      localStorage.setItem('currentUser', JSON.stringify(userData));

      setAuthState({
        user: userData,
        loading: false,
        error: null,
      });
    } catch (error) {
      setAuthState({
        user: null,
        loading: false,
        error: (error as Error).message || 'Login failed',
      });
    }
  };

  const logout = async () => {
    try {
      clearAuth();

      setAuthState({
        user: null,
        loading: false,
        error: null,
      });
    } catch (error) {
      setAuthState(prev => ({
        ...prev,
        error: (error as Error).message || 'Logout failed',
      }));
    }
  };

  const register = async (userData: User, token: string) => {
    try {
      localStorage.setItem('token', token);
      localStorage.setItem('currentUser', JSON.stringify(userData));

      setAuthState({
        user: userData,
        loading: false,
        error: null,
      });
    } catch (error) {
      setAuthState({
        user: null,
        loading: false,
        error: (error as Error).message || 'Registration failed',
      });
    }
  };

  return {
    ...authState,
    login,
    logout,
    register,
    isAuthenticated: !!authState.user,
  };
};