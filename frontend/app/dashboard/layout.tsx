'use client';

import React, { useEffect, useState } from 'react';
import { AppShell } from '../../components/layout/app-shell';
import { ProtectedRoute } from '../../components/layout/protected-route';
import { ChatWidget } from '../../components/chat/ChatWidget';
import { getAuthToken } from '../../lib/auth';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    setToken(getAuthToken());
  }, []);

  return (
    <ProtectedRoute>
      <AppShell>
        {children}
      </AppShell>
      {token && <ChatWidget token={token} />}
    </ProtectedRoute>
  );
}