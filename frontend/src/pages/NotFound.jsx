import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/common/Button';
import './NotFound.css';

const NotFound = () => {
  return (
    <div className="not-found-page">
      <div className="not-found-content">
        <div className="error-code">404</div>
        <h1>Page Not Found</h1>
        <p>
          The page you're looking for doesn't exist or has been moved.
        </p>
        <div className="not-found-actions">
          <Link to="/dashboard">
            <Button>Go to Dashboard</Button>
          </Link>
          <Link to="/">
            <Button variant="secondary">Go to Home</Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;