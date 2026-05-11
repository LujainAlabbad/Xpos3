import axios from './axios';

export const authAPI = {
  register: async (userData) => {
    const response = await axios.post('/auth/register', userData);
    return response.data;
  },
  
  login: async (credentials) => {
    const response = await axios.post('/auth/login', credentials);
    return response.data;
  },
  
  logout: async () => {
    const response = await axios.post('/auth/logout');
    return response.data;
  },
  
  verifyToken: async () => {
    const response = await axios.get('/auth/verify');
    return response.data;
  },
};