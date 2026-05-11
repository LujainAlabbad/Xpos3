import React, { createContext, useState, useCallback } from 'react';

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notification, setNotification] = useState(null);
  
  const showNotification = useCallback((message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  }, []);
  
  const hideNotification = useCallback(() => {
    setNotification(null);
  }, []);
  
  return (
    <NotificationContext.Provider value={{ notification, showNotification, hideNotification }}>
      {children}
      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
          <button onClick={hideNotification}>×</button>
        </div>
      )}
    </NotificationContext.Provider>
  );
};