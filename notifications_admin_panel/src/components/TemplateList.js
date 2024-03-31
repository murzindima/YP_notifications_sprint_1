import React, { useEffect, useState } from 'react';
import { getAllTemplates } from '../services/TemplateService';

function TemplateList() {
  const [templates, setTemplates] = useState([]);

  useEffect(() => {
    const fetchTemplates = async () => {
      const fetchedTemplates = await getAllTemplates();
      setTemplates(fetchedTemplates);
    };

    fetchTemplates();
  }, []);

  return (
    <div>
      <h2>Available Templates</h2>
      <ul>
        {templates.map((template) => (
          <li key={template.id}>
            <strong>ID:</strong> {template.id} <strong>Name:</strong> {template.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TemplateList;
