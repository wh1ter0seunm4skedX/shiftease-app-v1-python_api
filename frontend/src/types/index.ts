export interface User {
  id: string;
  email: string;
  name: string;
  role: 'youth_worker' | 'admin';
  created_at: Date;
  last_login?: Date;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string, role: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

export interface Event {
  id?: string;
  title: string;
  description: string;
  date: string | Date;
  required_workers: number;
  registered_users: string[];
  created_at: string | Date;
  created_by?: string;
}
