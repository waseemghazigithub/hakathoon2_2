'use client';

import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  subtitle?: string;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ title, subtitle, children, className = '', ...props }, ref) => {
    const baseClasses = 'rounded-xl border bg-card text-card-foreground shadow';

    return (
      <div
        ref={ref}
        className={`${baseClasses} ${className}`}
        {...props}
      >
        {(title || subtitle) && (
          <div className="p-6 pb-0">
            {title && <h3 className="font-semibold leading-none tracking-tight">{title}</h3>}
            {subtitle && <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>}
          </div>
        )}
        <div className={`p-6 ${title || subtitle ? '' : ''}`}>
          {children}
        </div>
      </div>
    );
  }
);

Card.displayName = 'Card';

export { Card };