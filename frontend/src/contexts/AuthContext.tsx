import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User as FirebaseUser
} from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { auth, db } from '../config/firebase';
import { apiService } from '../services/api';

interface User {
  id: string;
  email: string;
  name: string;
  role: 'youth_worker' | 'admin';
  createdAt: Date;
  lastLogin: Date;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string, role: string) => Promise<void>;
  logout: () => Promise<void>;
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

  // Function to get or create user document
  const getOrCreateUserDocument = async (firebaseUser: FirebaseUser, userData?: Partial<User>) => {
    const userRef = doc(db, 'users', firebaseUser.uid);
    const userSnap = await getDoc(userRef);

    if (userSnap.exists()) {
      // Update last login
      const existingData = userSnap.data() as User;
      await setDoc(userRef, {
        ...existingData,
        lastLogin: new Date()
      }, { merge: true });
      
      return {
        ...existingData,
        id: firebaseUser.uid,
        lastLogin: new Date()
      };
    } else if (userData) {
      // Create new user document
      const newUser: User = {
        id: firebaseUser.uid,
        email: firebaseUser.email!,
        name: userData.name || '',
        role: (userData.role as 'youth_worker' | 'admin') || 'youth_worker',
        createdAt: new Date(),
        lastLogin: new Date()
      };
      
      await setDoc(userRef, newUser);
      return newUser;
    }
    
    throw new Error('No user data available');
  };

  useEffect(() => {
    console.log('Setting up auth state listener');
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      try {
        if (firebaseUser) {
          console.log('Auth state changed:', firebaseUser);
          // Get the ID token
          const idToken = await firebaseUser.getIdToken();
          console.log('Got ID token');
          
          // Set the token in the API service
          apiService.setToken(idToken);
          
          // Get or update user document
          const userData = await getOrCreateUserDocument(firebaseUser);
          setUser(userData);
        } else {
          console.log('No firebase user');
          setUser(null);
          apiService.clearAuth();
        }
      } catch (error) {
        console.error('Error in auth state change:', error);
        setUser(null);
        apiService.clearAuth();
      } finally {
        setLoading(false);
      }
    });

    return () => {
      console.log('Cleaning up auth state listener');
      unsubscribe();
    };
  }, []);

  const login = async (email: string, password: string) => {
    try {
      console.log('Attempting login');
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const idToken = await userCredential.user.getIdToken();
      apiService.setToken(idToken);
      const userData = await getOrCreateUserDocument(userCredential.user);
      setUser(userData);
    } catch (error: any) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string, name: string, role: string) => {
    try {
      console.log('Attempting registration');
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      
      // Get token and set it
      const idToken = await userCredential.user.getIdToken();
      apiService.setToken(idToken);
      
      // Create user document in Firestore
      const userData = await getOrCreateUserDocument(userCredential.user, { name, role });
      setUser(userData);
    } catch (error: any) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      console.log('Attempting logout');
      await signOut(auth);
      setUser(null);
      apiService.clearAuth();
    } catch (error: any) {
      console.error('Logout error:', error);
      throw error;
    }
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
      {children}
    </AuthContext.Provider>
  );
};
