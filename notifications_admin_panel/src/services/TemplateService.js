import axios from 'axios';

const getAuthToken = () => localStorage.getItem('authToken');

const getAxiosInstanceWithAuth = () => {
  const token = getAuthToken();
  return axios.create({
    baseURL: 'http://notifications-admin-service/api/api/v1/',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
};

export const createTemplate = async (templateData) => {
    const api = getAxiosInstanceWithAuth();
    try {
      const response = await api.post('templates/', templateData);
      console.log(response.data);
    } catch (error) {
      console.error('Error creating template:', error);
    }
};

export const getAllTemplates = async () => {
  const api = getAxiosInstanceWithAuth();
  try {
    const response = await api.get('templates/');
    return response.data;
  } catch (error) {
    console.error('Error fetching templates:', error);
    return [];
  }
};
