import axios from 'axios';
import { Event, User } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle unauthorized responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Auth endpoints
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    const { token, user } = response.data;
    localStorage.setItem('token', token);
    return user;
  },

  register: async (email: string, password: string, name: string) => {
    const response = await api.post('/auth/register', { email, password, name });
    const { token, user } = response.data;
    localStorage.setItem('token', token);
    return user;
  },

  logout: async () => {
    localStorage.removeItem('token');
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // Event endpoints
  getEvents: async () => {
    const response = await api.get('/api/events');
    return response.data;
  },

  getEvent: async (id: string) => {
    const response = await api.get(`/api/events/${id}`);
    return response.data;
  },

  createEvent: async (data: Partial<Event>) => {
    const response = await api.post('/api/events', data);
    return response.data;
  },

  updateEvent: async (id: string, data: Partial<Event>) => {
    const response = await api.put(`/api/events/${id}`, data);
    return response.data;
  },

  deleteEvent: async (id: string) => {
    await api.delete(`/api/events/${id}`);
  },

  registerForEvent: async (id: string) => {
    const response = await api.post(`/api/events/${id}/register`);
    return response.data;
  },

  unregisterFromEvent: async (id: string) => {
    const response = await api.post(`/api/events/${id}/unregister`);
    return response.data;
  }
};
