// User type definition
export interface User {
  id: string;
  email: string;
  name?: string;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Task type definition
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
  userId: string;
}

// Design system token type
export interface DesignSystemToken {
  name: string;
  value: string;
  category: 'color' | 'spacing' | 'typography' | 'radius' | 'shadow';
}

// UI state type
export interface UIState {
  loading: boolean;
  error?: string;
  toast: ToastMessage[];
  modal: ModalState;
}

// Toast message type
export interface ToastMessage {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}

// Modal state type
export interface ModalState {
  isOpen: boolean;
  type: string;
  props: Record<string, any>;
}

// API response types
export interface TaskResponse {
  success: boolean;
  data: Task | Task[];
  message?: string;
  error?: string;
}

export interface AuthResponse {
  success: boolean;
  user?: User;
  error?: string;
  token?: string;
}

export interface RecentActivity {
  id: string;
  title: string;
  completed: boolean;
  createdAt: string;
  type: string;
}

export interface DashboardStats {
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
  completionRate: number;
  recentActivity: RecentActivity[];
}

// Form validation errors
export interface FormErrors {
  [key: string]: string;
}