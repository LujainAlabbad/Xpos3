import React from 'react';
import './Button.css';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  disabled = false, 
  loading = false, 
  onClick, 
  type = 'button',
  className = ''
}) => {
  return (
    <button
      type={type}
      className={`btn btn-${variant} btn-${size} ${className} ${disabled || loading ? 'disabled' : ''}`}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? (
        <>
          <span className="btn-spinner"></span>
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;