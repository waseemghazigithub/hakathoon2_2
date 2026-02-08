'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Input } from '../../../components/ui/input';
import { Button } from '../../../components/ui/button';
import { AuthCard } from '../../../components/auth/auth-card';
import { register as registerUser } from '../../../lib/api';
import { FormErrors } from '../../../lib/types';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
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
      if (!formData.name) newErrors.name = 'Name is required';
      if (!formData.email) newErrors.email = 'Email is required';
      if (!formData.password) newErrors.password = 'Password is required';
      if (formData.password.length < 6) newErrors.password = 'Password must be at least 6 characters';
      if (formData.password !== formData.confirmPassword) newErrors.confirmPassword = 'Passwords do not match';

      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        setIsLoading(false);
        return;
      }

      // Attempt registration
      const response = await registerUser(
        formData.email,
        formData.password,
        formData.name
      );

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
        setErrors({ general: response.error || 'Registration failed' });
      }
    } catch (error) {
      setErrors({ general: 'An unexpected error occurred' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthCard
      title="Create Account"
      subtitle="Join our community today"
    >
      <div className="flex justify-center mb-4">
        <div className="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center shadow-xl shadow-primary-500/30 transform rotate-6">
          <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
        </div>
      </div>

      {errors.general && (
        <div className="mb-6 p-4 bg-red-50/50 backdrop-blur-sm border border-red-100 text-red-600 rounded-xl text-sm font-medium animate-shake">
          {errors.general}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <Input
          label="Full name"
          id="name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
          error={errors.name}
          placeholder="John Doe"
          required
        />

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

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
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

          <Input
            label="Confirm Password"
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={errors.confirmPassword}
            placeholder="••••••••"
            required
          />
        </div>

        <div className="flex items-start px-1">
          <div className="flex items-center h-6">
            <input
              id="terms"
              name="terms"
              type="checkbox"
              className="h-4.5 w-4.5 text-primary-600 focus:ring-primary-500 border-slate-300 rounded-lg cursor-pointer transition-all"
              required
            />
          </div>
          <div className="ml-3 text-sm">
            <label htmlFor="terms" className="font-medium text-slate-600 cursor-pointer">
              By joining, you agree to our <a href="#" className="font-bold text-primary-600 hover:text-primary-500">Terms</a> and <a href="#" className="font-bold text-primary-600 hover:text-primary-500">Privacy Policy</a>
            </label>
          </div>
        </div>

        <Button
          type="submit"
          variant="primary"
          className="w-full h-14 text-base mt-2"
          isLoading={isLoading}
        >
          Create Free Account
        </Button>
      </form>

      <div className="mt-8 text-center">
        <p className="text-sm text-slate-500 font-medium">
          Already have an account?{' '}
          <Link href="/auth/login" className="font-bold text-primary-600 hover:text-primary-500 transition-colors">
            Sign in here
          </Link>
        </p>
      </div>
    </AuthCard>
  );
}