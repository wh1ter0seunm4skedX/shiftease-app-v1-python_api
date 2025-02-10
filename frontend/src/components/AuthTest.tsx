import React, { useState } from 'react';
import { auth } from '../config/firebase';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { apiService } from '../services/api';

const AuthTest = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      console.log('Attempting sign up...');
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log('Sign up successful, getting ID token...');
      const idToken = await userCredential.user.getIdToken();
      console.log('Got ID token, testing backend...');
      
      // Test the backend authentication
      const response = await apiService.get('/auth/test-auth');
      setMessage(`Sign up successful!\nUser ID: ${userCredential.user.uid}\nBackend test: ${JSON.stringify(response.data)}`);
    } catch (error: any) {
      console.error('Sign up error:', error);
      setMessage(`Error: ${error.code} - ${error.message}`);
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
      console.log('Got ID token, testing backend...');
      
      // Test the backend authentication
      const response = await apiService.get('/auth/test-auth');
      setMessage(`Sign in successful!\nUser ID: ${userCredential.user.uid}\nBackend test: ${JSON.stringify(response.data)}`);
    } catch (error: any) {
      console.error('Sign in error:', error);
      setMessage(`Error: ${error.code} - ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSignOut = async () => {
    try {
      console.log('Attempting sign out...');
      await signOut(auth);
      setMessage('Signed out successfully');
    } catch (error: any) {
      console.error('Sign out error:', error);
      setMessage(`Error: ${error.code} - ${error.message}`);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Firebase Auth Test</h2>
      
      <form onSubmit={handleSignUp} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            required
          />
        </div>
        
        <div className="flex space-x-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
          >
            Sign Up
          </button>
          
          <button
            type="button"
            onClick={handleSignIn}
            disabled={loading}
            className="flex-1 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50"
          >
            Sign In
          </button>
          
          <button
            type="button"
            onClick={handleSignOut}
            className="flex-1 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Sign Out
          </button>
        </div>
      </form>
      
      {message && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <pre className="whitespace-pre-wrap break-words">{message}</pre>
        </div>
      )}

      <div className="mt-4 text-sm text-gray-600">
        <p>Current Firebase Config:</p>
        <pre className="whitespace-pre-wrap break-words bg-gray-100 p-2 rounded mt-1">
          {JSON.stringify({
            apiKey: auth.app.options.apiKey,
            authDomain: auth.app.options.authDomain,
            projectId: auth.app.options.projectId
          }, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default AuthTest;
