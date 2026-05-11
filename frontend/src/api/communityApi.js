import axios from './axios';

export const communityAPI = {
  getFeed: async () => {
    const response = await axios.get('/community/feed');
    return response.data;
  },
  
  getTrending: async () => {
    const response = await axios.get('/community/trending');
    return response.data;
  },
};