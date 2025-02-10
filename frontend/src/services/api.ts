import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { Event, User } from '../types';
import { auth } from '../config/firebase';

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    this.api.interceptors.request.use(
      async (config) => {
        // Get current user from Firebase Auth
        const user = auth.currentUser;
        if (user) {
          // Get fresh token
          const token = await user.getIdToken(true);
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Sign out from Firebase if token is invalid
          await auth.signOut();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string | null) {
    this.token = token;
  }

  clearAuth() {
    this.token = null;
  }

  async get<T = any>(url: string): Promise<AxiosResponse<T>> {
    return this.api.get<T>(url);
  }

  async post<T = any>(url: string, data: any): Promise<AxiosResponse<T>> {
    return this.api.post<T>(url, data);
  }

  async put<T = any>(url: string, data: any): Promise<AxiosResponse<T>> {
    return this.api.put<T>(url, data);
  }

  async delete<T = any>(url: string): Promise<AxiosResponse<T>> {
    return this.api.delete<T>(url);
  }

  async login(email: string, password: string) {
    try {
      const response = await this.post('/auth/login', { email, password });
      const { token, user } = response.data;
      this.setToken(token);
      return user;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }

  async register(email: string, password: string, name: string, role: string) {
    try {
      const response = await this.post('/auth/register', { 
        email, 
        password, 
        name,
        role
      });
      const { token, user } = response.data;
      this.setToken(token);
      return user;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  }

  async logout() {
    this.setToken(null);
  }

  async getCurrentUser() {
    const response = await this.get('/auth/me');
    return response.data;
  }

  async getEvents() {
    return this.get('/events');
  }

  async getEvent(id: string) {
    return this.get(`/events/${id}`);
  }

  async createEvent(eventData: Partial<Event>) {
    return this.post('/events', eventData);
  }

  async updateEvent(eventId: string, eventData: Partial<Event>) {
    return this.put(`/events/${eventId}`, eventData);
  }

  async deleteEvent(eventId: string) {
    return this.delete(`/events/${eventId}`);
  }

  async registerForEvent(eventId: string) {
    return this.post(`/events/${eventId}/register`, {});
  }

  async unregisterFromEvent(eventId: string) {
    return this.delete(`/events/${eventId}/register`);
  }
}

export const apiService = new ApiService();
