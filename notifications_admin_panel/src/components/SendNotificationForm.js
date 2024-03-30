import React, { useState } from 'react';
import { sendNotification } from '../services/NotificationService';

function SendNotificationForm() {
  const [templateId, setTemplateId] = useState('');
  const [recipients, setRecipients] = useState('');
  const [context, setContext] = useState('{}');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await sendNotification({
      template_id: templateId,
      recipients: recipients.split(','),
      context: JSON.parse(context)
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Template ID"
        value={templateId}
        onChange={(e) => setTemplateId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Recipients (comma-separated)"
        value={recipients}
        onChange={(e) => setRecipients(e.target.value)}
      />
      <textarea
        placeholder="Context (JSON)"
        value={context}
        onChange={(e) => setContext(e.target.value)}
      />
      <button type="submit">Send Notification</button>
    </form>
  );
}

export default SendNotificationForm;
