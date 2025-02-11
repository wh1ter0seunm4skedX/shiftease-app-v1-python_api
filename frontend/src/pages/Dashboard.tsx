import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Event } from '../types';
import { apiService } from '../services/api';
import EventModal from '../components/EventModal';
import { motion } from 'framer-motion';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [events, setEvents] = useState<Event[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchEvents = async () => {
    try {
      const response = await apiService.getEvents();
      setEvents(response.data);
    } catch (err) {
      setError('Failed to fetch events');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleCreateEvent = () => {
    setSelectedEvent(null);
    setIsModalOpen(true);
  };

  const handleEditEvent = (event: Event) => {
    setSelectedEvent(event);
    setIsModalOpen(true);
  };

  const handleModalSuccess = () => {
    fetchEvents();
    setIsModalOpen(false);
  };

  const handleRegister = async (eventId: string) => {
    try {
      await apiService.registerForEvent(eventId);
      fetchEvents();
    } catch (err) {
      setError('Failed to register for event');
      console.error(err);
    }
  };

  const handleUnregister = async (eventId: string) => {
    try {
      await apiService.unregisterFromEvent(eventId);
      fetchEvents();
    } catch (err) {
      setError('Failed to unregister from event');
      console.error(err);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Failed to log out:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome, {user?.name}!
          </h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">
              Role: {user?.role === 'youth_worker' ? 'Youth Worker' : 'Admin'}
            </span>
            <button
              onClick={handleLogout}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">Events Dashboard</h1>
            {user?.role === 'admin' && (
              <button
                onClick={handleCreateEvent}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >
                Create Event
              </button>
            )}
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((event) => (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-lg shadow-md p-6"
              >
                <h2 className="text-xl font-semibold mb-2">{event.title}</h2>
                <p className="text-gray-600 mb-4">{event.description}</p>
                <div className="text-sm text-gray-500 mb-4">
                  <p>Date: {new Date(event.date).toLocaleDateString()}</p>
                  <p>
                    Workers: {event.registered_users.length} / {event.required_workers}
                  </p>
                </div>
                <div className="flex justify-between items-center">
                  {user?.role === 'admin' && (
                    <button
                      onClick={() => handleEditEvent(event)}
                      className="text-blue-500 hover:text-blue-700"
                    >
                      Edit
                    </button>
                  )}
                  {event.registered_users.includes(user?.id || '') ? (
                    <button
                      onClick={() => handleUnregister(event.id!)}
                      className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                    >
                      Unregister
                    </button>
                  ) : (
                    <button
                      onClick={() => handleRegister(event.id!)}
                      className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                      disabled={event.registered_users.length >= event.required_workers}
                    >
                      Register
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </div>

          <EventModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            event={selectedEvent}
            onSuccess={handleModalSuccess}
          />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
