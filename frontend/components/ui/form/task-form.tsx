'use client';

import React, { useState } from 'react';
import { Input } from '../input';
import { Button } from '../button';
import { FormErrors } from '../../../lib/types';

interface TaskFormProps {
  initialData?: {
    id?: string;
    title: string;
    description?: string;
    completed?: boolean;
  };
  onSubmit: (data: { title: string; description?: string }) => void;
  onCancel?: () => void;
  submitLabel?: string;
}

const TaskForm = ({ initialData, onSubmit, onCancel, submitLabel = 'Save Task' }: TaskFormProps) => {
  const [formData, setFormData] = useState({
    title: initialData?.title || '',
    description: initialData?.description || ''
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
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
    setIsSubmitting(true);
    setErrors({});

    try {
      // Validate form
      const newErrors: FormErrors = {};
      if (!formData.title.trim()) newErrors.title = 'Title is required';

      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        setIsSubmitting(false);
        return;
      }

      // Submit form data
      await onSubmit({
        title: formData.title.trim(),
        description: formData.description.trim() || undefined
      });
    } catch (error) {
      setErrors({ general: 'An unexpected error occurred' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {errors.general && (
        <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm">
          {errors.general}
        </div>
      )}

      <Input
        label="Title"
        id="title"
        name="title"
        type="text"
        value={formData.title}
        onChange={handleChange}
        error={errors.title}
        placeholder="Task title"
        required
      />

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          placeholder="Task description (optional)"
        />
        {errors.description && (
          <p className="mt-1 text-sm text-danger-600">{errors.description}</p>
        )}
      </div>

      <div className="flex justify-end space-x-3 pt-2">
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" variant="primary" isLoading={isSubmitting}>
          {submitLabel}
        </Button>
      </div>
    </form>
  );
};

export { TaskForm };