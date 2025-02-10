import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Event } from '../types';
import { apiService } from '../services/api';
import EventModal from '../components/EventModal';
import { motion } from 'framer-motion';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [events, setEvents] = useState<Event[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchEvents = async () => {
    try {
      const data = await apiService.getEvents();
      setEvents(data);
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

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
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
              <p>Location: {event.location}</p>
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
  );
};

export default Dashboard;
