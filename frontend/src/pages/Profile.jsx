import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { useNotification } from '../hooks/useNotification';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import './Profile.css';

const Profile = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { showNotification } = useNotification();
  
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  
  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    });
  };
  
  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      showNotification('Passwords do not match', 'error');
      return;
    }
    
    if (passwordData.newPassword.length < 8) {
      showNotification('Password must be at least 8 characters', 'error');
      return;
    }
    
    // TODO: Implement password change API call
    showNotification('Password change coming soon', 'info');
    setShowChangePassword(false);
    setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
  };
  
  const handleDeleteAccount = () => {
    // TODO: Implement account deletion API call
    showNotification('Account deletion coming soon', 'info');
    setShowDeleteModal(false);
  };
  
  return (
    <div className="profile-page">
      <div className="container">
        <div className="profile-header">
          <h1>Profile Settings</h1>
          <p>Manage your account information and preferences</p>
        </div>
        
        <div className="profile-content">
          <Card title="👤 Account Information">
            <div className="profile-info">
              <div className="info-row">
                <label>Username</label>
                <div className="info-value">{user?.username || 'N/A'}</div>
              </div>
              
              <div className="info-row">
                <label>Email</label>
                <div className="info-value">{user?.email || 'N/A'}</div>
              </div>
              
              <div className="info-row">
                <label>Member Since</label>
                <div className="info-value">
                  {user?.created_at 
                    ? new Date(user.created_at).toLocaleDateString() 
                    : 'N/A'}
                </div>
              </div>
            </div>
          </Card>
          
          <Card title="🔒 Security">
            <div className="security-section">
              {!showChangePassword ? (
                <Button onClick={() => setShowChangePassword(true)}>
                  Change Password
                </Button>
              ) : (
                <form onSubmit={handlePasswordSubmit} className="password-form">
                  <div className="form-group">
                    <label className="form-label">Current Password</label>
                    <input
                      type="password"
                      name="currentPassword"
                      className="form-input"
                      value={passwordData.currentPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label className="form-label">New Password</label>
                    <input
                      type="password"
                      name="newPassword"
                      className="form-input"
                      value={passwordData.newPassword}
                      onChange={handlePasswordChange}
                      required
                      minLength={8}
                    />
                  </div>
                  
                  <div className="form-group">
                    <label className="form-label">Confirm New Password</label>
                    <input
                      type="password"
                      name="confirmPassword"
                      className="form-input"
                      value={passwordData.confirmPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </div>
                  
                  <div className="form-actions">
                    <Button type="submit">Update Password</Button>
                    <Button 
                      variant="secondary" 
                      type="button"
                      onClick={() => {
                        setShowChangePassword(false);
                        setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
                      }}
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              )}
            </div>
          </Card>
          
          <Card title="⚠️ Danger Zone">
            <div className="danger-section">
              <div className="danger-info">
                <h3>Delete Account</h3>
                <p>
                  Once you delete your account, there is no going back. 
                  All your scans and data will be permanently deleted.
                </p>
              </div>
              <Button variant="danger" onClick={() => setShowDeleteModal(true)}>
                Delete Account
              </Button>
            </div>
          </Card>
        </div>
      </div>
      
      {/* Delete Account Modal */}
      {showDeleteModal && (
        <div className="modal-overlay" onClick={() => setShowDeleteModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>⚠️ Delete Account</h2>
            <p>
              Are you absolutely sure you want to delete your account? 
              This action cannot be undone.
            </p>
            <div className="modal-actions">
              <Button variant="danger" onClick={handleDeleteAccount}>
                Yes, Delete My Account
              </Button>
              <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;