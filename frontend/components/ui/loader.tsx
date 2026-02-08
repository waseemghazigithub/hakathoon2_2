'use client';

import React from 'react';

interface LoaderProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'spinner' | 'dots';
  className?: string;
}

const Loader = ({ size = 'md', variant = 'spinner', className = '' }: LoaderProps) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  if (variant === 'spinner') {
    return (
      <div className={`inline-block ${sizeClasses[size]} animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite] ${className}`} role="status">
        <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">Loading...</span>
      </div>
    );
  }

  if (variant === 'dots') {
    return (
      <div className={`flex items-center justify-center space-x-1 ${className}`}>
        <div className={`${sizeClasses.sm} h-2 w-2 rounded-full bg-current opacity-75`}></div>
        <div className={`${sizeClasses.sm} h-2 w-2 rounded-full bg-current opacity-75`}></div>
        <div className={`${sizeClasses.sm} h-2 w-2 rounded-full bg-current opacity-75`}></div>
      </div>
    );
  }

  return null;
};

export { Loader };

interface SkeletonProps {
  className?: string;
}

const Skeleton = ({ className = '' }: SkeletonProps) => {
  return (
    <div className={`animate-pulse rounded-md bg-muted ${className}`} />
  );
};

export { Skeleton };