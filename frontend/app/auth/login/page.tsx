'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Input } from '../../../components/ui/input';
import { Button } from '../../../components/ui/button';
import { AuthCard } from '../../../components/auth/auth-card';
import { login } from '../../../lib/api';
import { FormErrors } from '../../../lib/types';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrors({});

    try {
      // Validate form
      const newErrors: FormErrors = {};
      if (!formData.email) newErrors.email = 'Email is required';
      if (!formData.password) newErrors.password = 'Password is required';

      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        setIsLoading(false);
        return;
      }

      // Attempt login
      const response = await login(formData.email, formData.password);

      if (response.success && response.token) {
        // Store token and user info (in a real app, use better auth provider)
        localStorage.setItem('token', response.token);
        if (response.user) {
          localStorage.setItem('currentUser', JSON.stringify(response.user));
        }

        // Redirect to dashboard
        router.push('/dashboard');
        router.refresh(); // Refresh to update auth state
      } else {
        setErrors({ general: response.error || 'Login failed' });
      }
    } catch (error) {
      setErrors({ general: 'An unexpected error occurred' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthCard
      title="Welcome Back"
      subtitle="Sign in to your account"
    >
      <div className="flex justify-center mb-4">
        <div className="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center shadow-xl shadow-primary-500/30 transform -rotate-6">
          <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
      </div>

      {errors.general && (
        <div className="mb-6 p-4 bg-red-50/50 backdrop-blur-sm border border-red-100 text-red-600 rounded-xl text-sm font-medium animate-shake">
          {errors.general}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <Input
          label="Email address"
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="name@example.com"
          required
        />

        <Input
          label="Password"
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="••••••••"
          required
        />

        <div className="flex items-center justify-between px-1">
          <div className="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4.5 w-4.5 text-primary-600 focus:ring-primary-500 border-slate-300 rounded-lg cursor-pointer transition-all"
            />
            <label htmlFor="remember-me" className="ml-2.5 block text-sm font-medium text-slate-600 cursor-pointer">
              Remember me
            </label>
          </div>

          <div className="text-sm">
            <a href="#" className="font-bold text-primary-600 hover:text-primary-500 transition-colors">
              Forgot password?
            </a>
          </div>
        </div>

        <Button
          type="submit"
          variant="primary"
          className="w-full h-14 text-base"
          isLoading={isLoading}
        >
          Sign In
        </Button>
      </form>

      <div className="mt-8 text-center">
        <p className="text-sm text-slate-500 font-medium">
          Don't have an account?{' '}
          <Link href="/auth/register" className="font-bold text-primary-600 hover:text-primary-500 transition-colors">
            Create one for free
          </Link>
        </p>
      </div>
    </AuthCard>
  );
}