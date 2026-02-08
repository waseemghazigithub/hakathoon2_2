import React from 'react';
import { Card } from '../ui/card';

interface AuthCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

const AuthCard = ({ title, subtitle, children, footer }: AuthCardProps) => {
  return (
    <div className="w-full max-w-md mx-auto card-glass p-8 md:p-10">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight lg:text-5xl">{title}</h1>
        {subtitle && <p className="mt-4 text-lg text-slate-600 font-medium">{subtitle}</p>}
      </div>

      <div className="space-y-6">
        {children}
      </div>

      {footer && (
        <div className="mt-8 text-center text-sm text-slate-500 border-t border-slate-100 pt-6">
          {footer}
        </div>
      )}
    </div>
  );
};

export { AuthCard };