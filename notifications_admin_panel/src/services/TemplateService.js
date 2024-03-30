import axios from 'axios';

export const createTemplate = async (templateData) => {
    try {
      const response = await axios.post('http://notifications-admin-service/api/api/v1/templates', templateData);
      console.log(response.data);
    } catch (error) {
      console.error('Error creating template:', error);
    }
  };

export const getAllTemplates = async () => {
  try {
    const response = await axios.get('http://notifications-admin-service/api/api/v1/templates');
    return response.data;
  } catch (error) {
    console.error('Error fetching templates:', error);
    return [];
  }
};
