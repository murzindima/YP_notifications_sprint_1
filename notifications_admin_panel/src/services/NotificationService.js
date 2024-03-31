import axios from 'axios';

const getAuthToken = () => localStorage.getItem('authToken');

const getAxiosInstanceWithAuth = () => {
  const token = getAuthToken();
  return axios.create({
    baseURL: 'http://notifications-admin-service/api/api/v1/',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
};

export const sendNotification = async (notificationData) => {
  const api = getAxiosInstanceWithAuth();
  try {
    const response = await api.post('notifications/', notificationData);
    console.log(response.data);
  } catch (error) {
    console.error('Error sending notification:', error);
  }
};
