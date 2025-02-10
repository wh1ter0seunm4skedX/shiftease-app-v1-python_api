import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { Event, User } from '../types';

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    // Initialize token from localStorage
    this.token = localStorage.getItem('token');

    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` })
      },
      withCredentials: false
    });

    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
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
        const originalRequest = error.config;

        // Handle 401 errors
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            // Try to refresh the token
            const response = await this.post('/auth/refresh', {});
            const newToken = response.data.token;
            
            if (newToken) {
              this.setToken(newToken);
              originalRequest.headers.Authorization = `Bearer ${newToken}`;
              return this.api(originalRequest);
            }
          } catch (refreshError) {
            // If refresh fails, clear auth and redirect to login
            this.clearAuth();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('token', token);
      this.api.defaults.headers.common.Authorization = `Bearer ${token}`;
    } else {
      this.clearAuth();
    }
  }

  clearAuth() {
    this.token = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete this.api.defaults.headers.common.Authorization;
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
