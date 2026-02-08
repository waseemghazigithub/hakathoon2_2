'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '../ui/button';

const Header = () => {
  return (
    <header className="sticky top-0 z-10 bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-primary-600">UI Excellence</span>
            </Link>
            <nav className="ml-6 hidden md:flex space-x-4">
              <Link href="/dashboard" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                Dashboard
              </Link>
              <Link href="/dashboard/tasks" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                Tasks
              </Link>
            </nav>
          </div>

          <div className="flex items-center">
            <div className="flex-shrink-0 ml-4">
              <Button variant="primary" size="sm">
                <Link href="/dashboard/tasks/create">New Task</Link>
              </Button>
            </div>

            <div className="ml-4 relative flex-shrink-0">
              <Button variant="ghost" size="sm" className="text-gray-700">
                <span className="sr-only">Open user menu</span>
                <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                  <span className="text-primary-800 font-medium">U</span>
                </div>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export { Header };