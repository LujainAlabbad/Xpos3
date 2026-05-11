import React, { createContext, useState, useEffect } from 'react';
import { authAPI } from '../api/authApi';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    verifyAuth();
  }, []);
  
  const verifyAuth = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        const data = await authAPI.verifyToken();
        // Get user data from localStorage or fetch from API
        const userData = JSON.parse(localStorage.getItem('user') || '{}');
        setUser(userData);
      }
    } catch (error) {
      console.error('Auth verification failed:', error);
      localStorage.clear();
    } finally {
      setLoading(false);
    }
  };
  
  const login = async (credentials) => {
    const data = await authAPI.login(credentials);
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    setUser(data.user);
    return data;
  };
  
  const register = async (userData) => {
    const data = await authAPI.register(userData);
    return data;
  };
  
  const logout = () => {
    localStorage.clear();
    setUser(null);
  };
  
  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, verifyAuth }}>
      {children}
    </AuthContext.Provider>
  );
};