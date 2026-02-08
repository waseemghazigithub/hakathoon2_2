'use client';

import React from 'react';
import { Task } from '../../lib/types';
import { Button } from '../ui/button';

interface TaskItemProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
  onEdit: () => void;
}

const TaskItem = ({ task, onToggle, onDelete, onEdit }: TaskItemProps) => {
  return (
    <div className={`flex items-start p-4 rounded-lg border ${task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'} shadow-sm hover:shadow-md transition-shadow`}>
      <input
        type="checkbox"
        checked={task.completed}
        onChange={onToggle}
        className="mt-1 h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
      />

      <div className="ml-3 flex-1 min-w-0">
        <p className={`text-sm font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
          {task.title}
        </p>
        {task.description && (
          <p className={`text-sm ${task.completed ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
            {task.description}
          </p>
        )}
        <div className="mt-2 flex items-center text-xs text-gray-500">
          <span>Created: {new Date(task.createdAt).toLocaleDateString()}</span>
          {task.updatedAt !== task.createdAt && (
            <span className="ml-2">Updated: {new Date(task.updatedAt).toLocaleDateString()}</span>
          )}
        </div>
      </div>

      <div className="ml-4 flex space-x-2">
        <Button variant="ghost" size="sm" onClick={onEdit}>
          Edit
        </Button>
        <Button variant="danger" size="sm" onClick={onDelete}>
          Delete
        </Button>
      </div>
    </div>
  );
};

export { TaskItem };