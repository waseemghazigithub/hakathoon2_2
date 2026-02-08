'use client';

import React from 'react';
import { Header } from './header';

interface AppShellProps {
  children: React.ReactNode;
  showHeader?: boolean;
  showSidebar?: boolean;
}

const AppShell = ({ children, showHeader = true, showSidebar = true }: AppShellProps) => {
  return (
    <div className="flex flex-col min-h-screen">
      {showHeader && <Header />}

      <div className="flex flex-1">
        {showSidebar && (
          <aside className="hidden md:block w-64 bg-white border-r border-gray-200 p-4">
            <nav className="space-y-1">
              <a href="/dashboard" className="block px-4 py-2 text-sm font-medium text-primary-600 bg-primary-50 rounded-md">
                Dashboard
              </a>
              <a href="/dashboard/tasks" className="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-md">
                Tasks
              </a>
              <a href="#" className="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-md">
                Projects
              </a>
              <a href="#" className="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-md">
                Calendar
              </a>
              <a href="#" className="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-md">
                Settings
              </a>
              <div className="pt-4 mt-6 border-t border-gray-100">
                <button
                  onClick={() => {
                    localStorage.removeItem('token');
                    window.location.href = '/auth/login';
                  }}
                  className="w-full flex items-center px-4 py-2 text-sm font-semibold text-red-600 hover:bg-red-50 rounded-md transition-colors"
                >
                  <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </button>
              </div>
            </nav>
          </aside>
        )}

        <main className="flex-1 p-6 md:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export { AppShell };