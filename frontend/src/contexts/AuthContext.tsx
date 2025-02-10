import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, AuthContextType } from '../types';
import { apiService } from '../services/api';

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string, role: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      apiService.setToken(token);
      apiService.get('/auth/me')
        .then(response => {
          setUser(response.data);
        })
        .catch(() => {
          localStorage.removeItem('token');
          apiService.setToken(null);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const response = await apiService.post('/auth/login', { email, password });
    const { token, user } = response.data;
    localStorage.setItem('token', token);
    apiService.setToken(token);
    setUser(user);
  };

  const register = async (email: string, password: string, name: string, role: string) => {
    const response = await apiService.post('/auth/register', {
      email,
      password,
      name,
      role
    });
    const { token, user } = response.data;
    localStorage.setItem('token', token);
    apiService.setToken(token);
    setUser(user);
  };

  const logout = async () => {
    localStorage.removeItem('token');
    apiService.setToken(null);
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
