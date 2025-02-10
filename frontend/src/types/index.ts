export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'volunteer';
  createdAt?: string;
  updatedAt?: string;
}

export interface Event {
  id?: string;
  title: string;
  description: string;
  date: string;
  location: string;
  required_workers: number;
  registered_users: string[];
  createdBy: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
}
