'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '../../../components/ui/button';
import { TaskList } from '../../../components/tasks/task-list';
import { Modal } from '../../../components/ui/modal';
import { TaskForm } from '../../../components/ui/form/task-form';
import { getTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '../../../lib/api';
import { Task } from '../../../lib/types';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [sort, setSort] = useState<'newest' | 'oldest'>('newest');
  const router = useRouter();

  // Load tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await getTasks();
      // Handle both wrapped and direct responses
      const taskList = Array.isArray(data) ? data : (data as any).data || [];
      setTasks(taskList as Task[]);
      setError(null);
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (data: { title: string; description?: string }) => {
    try {
      const response = await createTask(data);
      // Handle both wrapped and direct responses
      const newTask = (response as any).data || response;
      setTasks([newTask as Task, ...tasks]);
      setShowCreateModal(false);
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
    }
  };

  const handleUpdateTask = async (data: { title: string; description?: string }) => {
    if (!editingTask) return;

    try {
      const response = await updateTask(editingTask.id, data);
      // Handle both wrapped and direct responses
      const updatedTask = (response as any).data || response;
      setTasks(tasks.map(t => t.id === editingTask.id ? updatedTask as Task : t));
      setShowEditModal(false);
      setEditingTask(null);
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;

    try {
      await deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const handleToggleTask = async (id: string) => {
    try {
      const response = await toggleTaskCompletion(id);
      // Handle both wrapped and direct responses
      const updatedTask = (response as any).data || response;
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask as Task : task
      ));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error toggling task:', err);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowEditModal(true);
  };

  // Filter tasks based on selection
  const filteredTasks = tasks
    .filter(task => {
      if (filter === 'active') return !task.completed;
      if (filter === 'completed') return task.completed;
      return true;
    })
    .sort((a, b) => {
      if (sort === 'newest') {
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
      } else {
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
      }
    });

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
          <p className="text-gray-600 mt-1">Manage your tasks and boost productivity</p>
        </div>

        <Button
          variant="primary"
          onClick={() => setShowCreateModal(true)}
        >
          + New Task
        </Button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="flex items-center space-x-2">
          <label className="text-sm font-medium text-gray-700">Filter:</label>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as 'all' | 'active' | 'completed')}
            className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <label className="text-sm font-medium text-gray-700">Sort:</label>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as 'newest' | 'oldest')}
            className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          >
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
          </select>
        </div>
      </div>

      <TaskList
        tasks={filteredTasks}
        onToggle={handleToggleTask}
        onDelete={handleDeleteTask}
        onEdit={handleEditTask}
      />

      {/* Create Task Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Task"
      >
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowCreateModal(false)}
          submitLabel="Create Task"
        />
      </Modal>

      {/* Edit Task Modal */}
      {editingTask && (
        <Modal
          isOpen={showEditModal}
          onClose={() => {
            setShowEditModal(false);
            setEditingTask(null);
          }}
          title="Edit Task"
        >
          <TaskForm
            initialData={{
              id: editingTask.id,
              title: editingTask.title,
              description: editingTask.description
            }}
            onSubmit={handleUpdateTask}
            onCancel={() => {
              setShowEditModal(false);
              setEditingTask(null);
            }}
            submitLabel="Update Task"
          />
        </Modal>
      )}
    </div>
  );
}