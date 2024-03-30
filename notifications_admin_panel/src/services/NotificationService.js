import axios from 'axios';

export const sendNotification = async (notificationData) => {
  try {
    const response = await axios.post('http://notifications-admin-service/api/api/v1/notifications', notificationData);
    console.log(response.data);
  } catch (error) {
    console.error('Error sending notification:', error);
  }
};


