import React, { useState } from 'react';
import { sendNotification } from '../services/NotificationService';

function SendNotificationForm() {
  const [templateId, setTemplateId] = useState('');
  const [recipients, setRecipients] = useState('');
  const [context, setContext] = useState('{}');
  const [notificationType, setNotificationType] = useState('email');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dataToSend = {
      template_id: templateId,
      recipients: recipients.split(',').map(recipient => recipient.trim()),
      context: JSON.parse(context),
      notification_type: notificationType
    };
    await sendNotification(dataToSend);
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
      <select
        value={notificationType}
        onChange={(e) => setNotificationType(e.target.value)}
      >
        <option value="email">Email</option>
        <option value="sms">SMS</option>
        <option value="sms">Push</option>
      </select>
      <button type="submit">Send Notification</button>
    </form>
  );
}

export default SendNotificationForm;
