import axios from './axios';

export const scanAPI = {
  uploadScan: async (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post('/scans/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress,
    });
    return response.data;
  },
  
  getUserScans: async () => {
    const response = await axios.get('/scans/');
    return response.data;
  },
  
  getScanReport: async (scanId) => {
    const response = await axios.get(`/scans/${scanId}`);
    return response.data;
  },
  
  getScanStatus: async (scanId) => {
    const response = await axios.get(`/scans/${scanId}/status`);
    return response.data;
  },
  
  deleteScan: async (scanId) => {
    const response = await axios.delete(`/scans/${scanId}`);
    return response.data;
  },
};