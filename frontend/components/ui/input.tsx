'use client';

import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className = '', ...props }, ref) => {
    const baseClasses = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm';
    const errorClasses = error ? 'border-danger-500 focus:border-danger-500 focus:ring-danger-500' : '';

    const combinedClasses = `${baseClasses} ${errorClasses} ${className}`;

    return (
      <div className="space-y-2">
        {label && (
          <label htmlFor={props.id} className="block text-sm font-semibold text-slate-700 ml-1">
            {label}
          </label>
        )}
        <div className="relative group">
          <input
            ref={ref}
            className={`input-modern ${error ? 'border-red-400 focus:ring-red-400/50 focus:border-red-400/50' : ''} ${className}`}
            {...props}
          />
        </div>
        {(helperText || error) && (
          <p className={`mt-1 text-xs font-medium ${error ? 'text-red-500' : 'text-slate-500'} ml-1`}>
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };