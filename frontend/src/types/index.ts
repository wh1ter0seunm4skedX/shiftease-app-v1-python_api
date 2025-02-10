export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  created_at?: string;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<{ success: boolean }>;
  register: (email: string, password: string, name: string, role: string) => Promise<{ success: boolean }>;
  logout: () => Promise<void>;
  loading: boolean;
}

export interface Event {
  id: string;
  title: string;
  description: string;
  date: string;
  capacity: number;
  registered_workers: string[];
  created_by: string;
  created_at: string;
  updated_at?: string;
}
