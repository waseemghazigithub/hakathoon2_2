import React from 'react';
import { Button } from '../ui/button';
import Link from 'next/link';

interface EmptyStateProps {
  title: string;
  description: string;
  actionText?: string;
  actionLink?: string;
  icon?: React.ReactNode;
}

const EmptyState = ({
  title,
  description,
  actionText,
  actionLink,
  icon
}: EmptyStateProps) => {
  return (
    <div className="text-center py-12">
      {icon || (
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      )}
      <h3 className="mt-2 text-sm font-medium text-gray-900">{title}</h3>
      <p className="mt-1 text-sm text-gray-500">{description}</p>
      {actionText && actionLink && (
        <div className="mt-6">
          <Link href={actionLink}>
            <Button variant="primary">
              {actionText}
            </Button>
          </Link>
        </div>
      )}
    </div>
  );
};

export { EmptyState };