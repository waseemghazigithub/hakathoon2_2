'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { TaskForm } from '../../../../components/ui/form/task-form';
import { Card } from '../../../../components/ui/card';
import { Button } from '../../../../components/ui/button';
import { createTask } from '../../../../lib/api';

export default function CreateTaskPage() {
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (data: { title: string; description?: string }) => {
    try {
      setError(null);
      await createTask(data);
      router.push('/dashboard/tasks');
      router.refresh(); // Refresh to update the task list
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Create Task</h1>
        <Button variant="secondary" onClick={() => router.back()}>
          Cancel
        </Button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <Card>
        <TaskForm
          onSubmit={handleSubmit}
          onCancel={() => router.back()}
          submitLabel="Create Task"
        />
      </Card>
    </div>
  );
}