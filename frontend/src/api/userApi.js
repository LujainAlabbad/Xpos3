import axios from './axios';

export const userAPI = {
  getProfile: async () => {
    const response = await axios.get('/users/profile');
    return response.data;
  },
  
  updateProfile: async (profileData) => {
    const response = await axios.put('/users/profile', profileData);
    return response.data;
  },
  
  deleteAccount: async () => {
    const response = await axios.delete('/users/account');
    return response.data;
  },
};