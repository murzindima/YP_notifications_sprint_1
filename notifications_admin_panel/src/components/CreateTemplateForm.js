import React, { useState } from 'react';
import { createTemplate } from '../services/TemplateService';

function CreateTemplateForm() {
  const [name, setName] = useState('');
  const [template, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createTemplate({ name, template: template });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Template Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <textarea
        placeholder="Template Content"
        value={template}
        onChange={(e) => setContent(e.target.value)}
      />
      <button type="submit">Create Template</button>
    </form>
  );
}

export default CreateTemplateForm;
