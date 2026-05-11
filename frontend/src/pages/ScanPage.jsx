import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { scanAPI } from '../api/scanApi';
import { useNotification } from '../hooks/useNotification';
import { useWebSocket } from '../hooks/useWebSocket';
import { validateFile } from '../utils/validators';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import './ScanPage.css';

const ScanPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  const [activeScanId, setActiveScanId] = useState(null);
  const [scanStatus, setScanStatus] = useState('');

  const { showNotification } = useNotification();
  const navigate = useNavigate();

  // Poll scan status after upload — redirects automatically when done
  useWebSocket(activeScanId, (finalStatus) => {
    if (finalStatus === 'completed') {
      showNotification('Scan complete! Loading report...', 'success');
      navigate(`/report/${activeScanId}`);
    } else {
      setError('Scan failed. Please try again.');
      setUploading(false);
      setScanStatus('');
    }
  });
  
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };
  
  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };
  
  const handleFileSelect = (file) => {
    setError('');
    
    const validation = validateFile(file);
    if (!validation.valid) {
      setError(validation.error);
      return;
    }
    
    setSelectedFile(file);
  };
  
  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }
    
    setUploading(true);
    setUploadProgress(0);
    
    try {
      const result = await scanAPI.uploadScan(selectedFile, (progressEvent) => {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(progress);
      });

      // Start polling for scan completion
      setScanStatus('Analysing code in isolated container...');
      setActiveScanId(result.scan.id);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
      showNotification('Upload failed', 'error');
      setUploading(false);
    }
  };
  
  const handleRemoveFile = () => {
    setSelectedFile(null);
    setError('');
    setUploadProgress(0);
  };
  
  return (
    <div className="scan-page">
      <div className="container">
        <div className="scan-header">
          <h1>New Security Scan</h1>
          <p>Upload your Python file to analyze for security vulnerabilities</p>
        </div>
        
        <div className="scan-content">
          <Card>
            {error && <div className="alert alert-error">{error}</div>}
            
            <div
              className={`upload-zone ${dragActive ? 'drag-active' : ''} ${selectedFile ? 'has-file' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              {selectedFile ? (
                <div className="file-preview">
                  <div className="file-icon">📄</div>
                  <div className="file-info">
                    <h3>{selectedFile.name}</h3>
                    <p>{(selectedFile.size / 1024).toFixed(2)} KB</p>
                  </div>
                  {!uploading && (
                    <button onClick={handleRemoveFile} className="remove-file">
                      ✕
                    </button>
                  )}
                </div>
              ) : (
                <div className="upload-prompt">
                  <div className="upload-icon">📁</div>
                  <h3>Drag & drop your Python file here</h3>
                  <p>or</p>
                  <label htmlFor="file-input" className="btn btn-secondary">
                    Browse Files
                  </label>
                  <input
                    id="file-input"
                    type="file"
                    accept=".py"
                    onChange={handleFileInput}
                    style={{ display: 'none' }}
                  />
                  <p className="upload-hint">Only .py files up to 10MB are supported</p>
                </div>
              )}
            </div>
            
            {uploading && (
              <div className="progress-container">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: activeScanId ? '100%' : `${uploadProgress}%` }}
                  ></div>
                </div>
                <p className="progress-text">
                  {activeScanId ? scanStatus : `${uploadProgress}% Uploaded`}
                </p>
              </div>
            )}
            
            <div className="scan-actions">
              <Button
                onClick={handleUpload}
                disabled={!selectedFile}
                loading={uploading}
                className="btn-large"
              >
                Start Security Scan
              </Button>
            </div>
          </Card>
          
          <Card title="What happens next?" className="info-card">
            <div className="scan-steps">
              <div className="scan-step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>File Upload</h4>
                  <p>Your Python file is securely uploaded to our server</p>
                </div>
              </div>
              
              <div className="scan-step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>Security Analysis</h4>
                  <p>Bandit engine scans your code in an isolated environment</p>
                </div>
              </div>
              
              <div className="scan-step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>Report Generation</h4>
                  <p>AI-powered explanations and fixes are generated for each vulnerability</p>
                </div>
              </div>
              
              <div className="scan-step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h4>Results Ready</h4>
                  <p>View your detailed security report with actionable recommendations</p>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ScanPage;