import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { scanAPI } from '../api/scanApi';
import { formatDate } from '../utils/formatters';
import Spinner from '../components/common/Spinner';
import Card from '../components/common/Card';
import './Dashboard.css';

const Dashboard = () => {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, high: 0, medium: 0, low: 0 });
  
  useEffect(() => {
    fetchScans();
  }, []);
  
  const fetchScans = async () => {
    try {
      const data = await scanAPI.getUserScans();
      setScans(data.scans || []);
      calculateStats(data.scans || []);
    } catch (error) {
      console.error('Failed to fetch scans:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const calculateStats = (scansData) => {
    const total = scansData.length;
    let high = 0, medium = 0, low = 0;
    
    scansData.forEach(scan => {
      if (scan.severity_summary) {
        high += scan.severity_summary.high || 0;
        medium += scan.severity_summary.medium || 0;
        low += scan.severity_summary.low || 0;
      }
    });
    
    setStats({ total, high, medium, low });
  };
  
  if (loading) {
    return <Spinner />;
  }
  
  return (
    <div className="dashboard-page">
      <div className="container">
        <div className="dashboard-header">
          <h1>Dashboard</h1>
          <Link to="/scan" className="btn btn-primary">
            + New Scan
          </Link>
        </div>
        
        <div className="stats-grid">
          <Card className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-info">
              <h3>{stats.total}</h3>
              <p>Total Scans</p>
            </div>
          </Card>
          
          <Card className="stat-card stat-high">
            <div className="stat-icon">🔴</div>
            <div className="stat-info">
              <h3>{stats.high}</h3>
              <p>High Severity</p>
            </div>
          </Card>
          
          <Card className="stat-card stat-medium">
            <div className="stat-icon">🟡</div>
            <div className="stat-info">
              <h3>{stats.medium}</h3>
              <p>Medium Severity</p>
            </div>
          </Card>
          
          <Card className="stat-card stat-low">
            <div className="stat-icon">🟢</div>
            <div className="stat-info">
              <h3>{stats.low}</h3>
              <p>Low Severity</p>
            </div>
          </Card>
        </div>
        
        <Card title="Recent Scans">
          {scans.length === 0 ? (
            <div className="empty-state">
              <p>No scans yet. Upload your first Python file to get started!</p>
              <Link to="/scan" className="btn btn-primary">
                Start Scanning
              </Link>
            </div>
          ) : (
            <div className="scans-table">
              <table>
                <thead>
                  <tr>
                    <th>Filename</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Vulnerabilities</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {scans.map(scan => (
                    <tr key={scan.id}>
                      <td>{scan.filename}</td>
                      <td>
                        <span className={`status-badge status-${scan.status}`}>
                          {scan.status}
                        </span>
                      </td>
                      <td>{formatDate(scan.created_at)}</td>
                      <td>
                        {scan.severity_summary && (
                          <div className="severity-badges">
                            {scan.severity_summary.high > 0 && (
                              <span className="severity-badge high">
                                {scan.severity_summary.high} High
                              </span>
                            )}
                            {scan.severity_summary.medium > 0 && (
                              <span className="severity-badge medium">
                                {scan.severity_summary.medium} Med
                              </span>
                            )}
                            {scan.severity_summary.low > 0 && (
                              <span className="severity-badge low">
                                {scan.severity_summary.low} Low
                              </span>
                            )}
                          </div>
                        )}
                      </td>
                      <td>
                        {scan.status === 'completed' && (
                          <Link 
                            to={`/report/${scan.id}`} 
                            className="btn btn-small btn-primary"
                          >
                            View Report
                          </Link>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;