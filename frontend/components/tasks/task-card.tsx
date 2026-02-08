import React from 'react';
import { Card } from '../ui/card';

interface TaskCardProps {
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
  children?: React.ReactNode;
}

const TaskCard = ({ title, description, completed, createdAt, updatedAt, children }: TaskCardProps) => {
  return (
    <Card className={`transition-all duration-200 ${completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}`}>
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={completed}
          readOnly
          className="mt-1 h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
        />

        <div className="ml-3 flex-1 min-w-0">
          <h3 className={`text-sm font-medium ${completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
            {title}
          </h3>
          {description && (
            <p className={`text-sm ${completed ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
              {description}
            </p>
          )}

          <div className="mt-2 flex items-center text-xs text-gray-500">
            <span>Created: {new Date(createdAt).toLocaleDateString()}</span>
            {updatedAt !== createdAt && (
              <span className="ml-2">Updated: {new Date(updatedAt).toLocaleDateString()}</span>
            )}
          </div>
        </div>
      </div>

      {children && <div className="mt-4 pt-4 border-t border-gray-200">{children}</div>}
    </Card>
  );
};

export { TaskCard };