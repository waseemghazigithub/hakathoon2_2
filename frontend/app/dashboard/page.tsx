'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { getDashboardStats } from '../../lib/api';
import { DashboardStats } from '../../lib/types';

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStats() {
      try {
        setLoading(true);
        const data = await getDashboardStats();
        setStats(data);
      } catch (err) {
        console.error('Failed to fetch dashboard stats:', err);
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    }
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="p-6 bg-red-50 text-red-700 rounded-lg">
        <p>{error || 'Something went wrong'}</p>
        <Button
          variant="secondary"
          onClick={() => window.location.reload()}
          className="mt-4"
        >
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <Button variant="primary">
          <a href="/dashboard/tasks">View Tasks</a>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card title="Total Tasks" className="bg-gradient-to-br from-primary-50 to-primary-100 border-none shadow-premium transition-all hover:shadow-hover">
          <div className="text-4xl font-extrabold text-primary-700">{stats.totalTasks}</div>
          <p className="text-sm font-medium text-gray-600 mt-2">
            {stats.completedTasks} completed, {stats.pendingTasks} pending
          </p>
        </Card>

        <Card title="Completed Tasks" className="bg-gradient-to-br from-emerald-50 to-emerald-100 border-none shadow-premium transition-all hover:shadow-hover">
          <div className="text-4xl font-extrabold text-emerald-700">{stats.completedTasks}</div>
          <p className="text-sm font-medium text-gray-600 mt-2">{stats.completionRate}% completion rate</p>
        </Card>

        <Card title="Pending Tasks" className="bg-gradient-to-br from-amber-50 to-amber-100 border-none shadow-premium transition-all hover:shadow-hover">
          <div className="text-4xl font-extrabold text-amber-700">{stats.pendingTasks}</div>
          <p className="text-sm font-medium text-gray-600 mt-2">Need attention</p>
        </Card>
      </div>

      <div className="mt-8">
        <Card title="Recent Activity" className="border-none shadow-premium">
          {stats.recentActivity.length > 0 ? (
            <ul className="divide-y divide-gray-100">
              {stats.recentActivity.map((activity) => (
                <li key={activity.id} className="py-4 first:pt-0 last:pb-0">
                  <div className="flex space-x-4 items-center">
                    <div className="flex-shrink-0">
                      <div className={`h-10 w-10 rounded-full flex items-center justify-center ${activity.completed ? 'bg-emerald-100 text-emerald-700' : 'bg-primary-100 text-primary-700'
                        }`}>
                        {activity.completed ? (
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                          </svg>
                        ) : (
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                          </svg>
                        )}
                      </div>
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-semibold text-gray-900 truncate">
                        {activity.completed ? 'Completed' : 'Created'}: "{activity.title}"
                      </p>
                      <p className="text-xs text-gray-500 font-medium">
                        {new Date(activity.createdAt).toLocaleDateString()} at {new Date(activity.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                    <div>
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider ${activity.completed ? 'bg-emerald-50 text-emerald-700' : 'bg-primary-50 text-primary-700'
                        }`}>
                        {activity.completed ? 'Done' : 'New'}
                      </span>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500 font-medium">No recent activity</p>
              <Button variant="primary" className="mt-4">
                <a href="/dashboard/tasks">Create your first task</a>
              </Button>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}