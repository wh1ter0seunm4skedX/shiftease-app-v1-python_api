import React, { useState, useEffect } from 'react';
import { Event } from '../types';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';

interface EventModalProps {
  isOpen: boolean;
  onClose: () => void;
  event?: Event | null;
  onSuccess: () => void;
}

const EventModal: React.FC<EventModalProps> = ({
  isOpen,
  onClose,
  event,
  onSuccess,
}) => {
  const { user } = useAuth();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [date, setDate] = useState('');
  const [requiredWorkers, setRequiredWorkers] = useState(1);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (event) {
      setTitle(event.title);
      setDescription(event.description);
      setDate(new Date(event.date).toISOString().split('T')[0]);
      setRequiredWorkers(event.required_workers);
    } else {
      setTitle('');
      setDescription('');
      setDate('');
      setRequiredWorkers(1);
    }
  }, [event]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    setError('');
    setLoading(true);

    try {
      const eventData = {
        title,
        description,
        date: new Date(date).toISOString(),
        required_workers: requiredWorkers,
        created_by: user.id,
      };

      if (event?.id) {
        await apiService.put(`/events/${event.id}`, eventData);
      } else {
        await apiService.post('/events', eventData);
      }

      onSuccess();
      onClose();
    } catch (error: any) {
      console.error('Failed to save event:', error);
      setError(error.message || 'Failed to save event');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            {event ? 'Edit Event' : 'Create New Event'}
          </h3>
          <form onSubmit={handleSubmit} className="mt-4">
            <div className="mb-4">
              <label
                htmlFor="title"
                className="block text-sm font-medium text-gray-700"
              >
                Title
              </label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div className="mb-4">
              <label
                htmlFor="description"
                className="block text-sm font-medium text-gray-700"
              >
                Description
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
                rows={3}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div className="mb-4">
              <label
                htmlFor="date"
                className="block text-sm font-medium text-gray-700"
              >
                Date
              </label>
              <input
                type="date"
                id="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div className="mb-4">
              <label
                htmlFor="requiredWorkers"
                className="block text-sm font-medium text-gray-700"
              >
                Required Workers
              </label>
              <input
                type="number"
                id="requiredWorkers"
                value={requiredWorkers}
                onChange={(e) => setRequiredWorkers(parseInt(e.target.value))}
                required
                min="1"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            {error && (
              <div className="mb-4 text-sm text-red-600">{error}</div>
            )}

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Saving...' : event ? 'Update' : 'Create'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EventModal;