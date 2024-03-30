import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoginForm from './components/LoginForm';
import CreateTemplateForm from './components/CreateTemplateForm';
import SendNotificationForm from './components/SendNotificationForm';
import TemplateList from './components/TemplateList';

function App() {
  const [authToken, setAuthToken] = useState(localStorage.getItem('authToken') || '');

  useEffect(() => {
    if (authToken) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [authToken]);

  const handleLoginSuccess = (token) => {
    localStorage.setItem('authToken', token);
    setAuthToken(token);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setAuthToken('');
  };

  return (
    <div>
      <h1>Notifications Admin Panel</h1>
      {!authToken ? (
        <LoginForm onLoginSuccess={handleLoginSuccess} />
      ) : (
        <>
          <button onClick={handleLogout}>Logout</button>
          <CreateTemplateForm />
          <TemplateList />
          <SendNotificationForm />
        </>
      )}
    </div>
  );
}

export default App;
