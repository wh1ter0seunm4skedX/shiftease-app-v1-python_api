import React, { useState } from 'react';
import { auth } from '../config/firebase';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { apiService } from '../services/api';

const AuthTest = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      console.log('Attempting sign up...');
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log('Sign up successful, getting ID token...');
      const idToken = await userCredential.user.getIdToken();
      setToken(idToken);
      console.log('Got ID token, testing backend...');
      
      // Test the backend authentication
      const response = await apiService.get('/auth/test-auth');
      setMessage(`Sign up successful!\nUser ID: ${userCredential.user.uid}\nBackend test: ${JSON.stringify(response.data)}`);
    } catch (error: any) {
      console.error('Sign up error:', error);
      setMessage(`Error: ${error.code} - ${error.message}`);
      setToken('');
    } finally {
      setLoading(false);
    }
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      console.log('Attempting sign in...');
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      console.log('Sign in successful, getting ID token...');
      const idToken = await userCredential.user.getIdToken();
      setToken(idToken);
      console.log('Got ID token, testing backend...');
      
      // Test the backend authentication
      const response = await apiService.get('/auth/test-auth');
      setMessage(`Sign in successful!\nUser ID: ${userCredential.user.uid}\nBackend test: ${JSON.stringify(response.data)}`);
    } catch (error: any) {
      console.error('Sign in error:', error);
      setMessage(`Error: ${error.code} - ${error.message}`);
      setToken('');
    } finally {
      setLoading(false);
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut(auth);
      setMessage('Signed out successfully');
      setToken('');
    } catch (error: any) {
      console.error('Sign out error:', error);
      setMessage(`Error: ${error.code} - ${error.message}`);
    }
  };

  const copyToken = () => {
    if (token) {
      navigator.clipboard.writeText(token);
      alert('Token copied to clipboard!');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Auth Test
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div className="flex space-x-4">
              <button
                type="button"
                onClick={handleSignUp}
                disabled={loading}
                className="flex-1 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
              >
                Sign Up
              </button>
              <button
                type="button"
                onClick={handleSignIn}
                disabled={loading}
                className="flex-1 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                Sign In
              </button>
              <button
                type="button"
                onClick={handleSignOut}
                disabled={loading}
                className="flex-1 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
              >
                Sign Out
              </button>
            </div>
          </form>

          {message && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900">Response:</h3>
              <pre className="mt-2 whitespace-pre-wrap bg-gray-50 p-4 rounded-md text-sm">
                {message}
              </pre>
            </div>
          )}

          {token && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900">Firebase Token:</h3>
              <div className="mt-2 relative">
                <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded-md text-sm overflow-x-auto">
                  {token}
                </pre>
                <button
                  onClick={copyToken}
                  className="absolute top-2 right-2 px-3 py-1 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Copy
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthTest;
