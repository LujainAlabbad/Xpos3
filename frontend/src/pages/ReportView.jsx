import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { scanAPI } from '../api/scanApi';
import { downloadJSON } from '../utils/helpers';
import Spinner from '../components/common/Spinner';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import VulnerabilityCard from '../components/report/VulnerabilityCard';
import './ReportView.css';

const ReportView = () => {
  const { scanId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all'); // all, high, medium, low
  
  useEffect(() => {
    fetchReport();
  }, [scanId]);
  
  const fetchReport = async () => {
    try {
      const data = await scanAPI.getScanReport(scanId);
      setReport(data);
    } catch (err) {
      setError('Failed to load report');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleDownload = () => {
    if (report) {
      downloadJSON(report, `xpos3-report-${scanId}.json`);
    }
  };
  
  const getFilteredVulnerabilities = () => {
    if (!report?.bandit_report?.results) return [];

    const results = report.bandit_report.results;
    const indexed = results.map((vuln, idx) => ({ vuln, idx }));

    if (filter === 'all') return indexed;
    return indexed.filter(({ vuln }) =>
      vuln.issue_severity?.toLowerCase() === filter.toLowerCase()
    );
  };
  
  if (loading) {
    return (
      <div className="report-loading">
        <Spinner size="large" />
        <p>Loading security report...</p>
      </div>
    );
  }
  
  if (error || !report) {
    return (
      <div className="report-error">
        <div className="container">
          <Card>
            <h2>⚠️ Error Loading Report</h2>
            <p>{error || 'Report not found'}</p>
            <Button onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </Button>
          </Card>
        </div>
      </div>
    );
  }
  
  const vulnerabilities = getFilteredVulnerabilities();
  const summary = report.scan?.severity_summary || { high: 0, medium: 0, low: 0 };
  
  return (
    <div className="report-page">
      <div className="container">
        <div className="report-header">
          <div>
            <h1>Security Report</h1>
            <p className="report-filename">{report.scan?.filename}</p>
          </div>
          <div className="report-actions">
            <Button variant="secondary" onClick={handleDownload}>
              📥 Download JSON
            </Button>
            <Button onClick={() => navigate('/dashboard')}>
              ← Back to Dashboard
            </Button>
          </div>
        </div>
        
        <div className="summary-cards">
          <Card className="summary-card summary-total">
            <div className="summary-icon">📊</div>
            <div className="summary-info">
              <h3>{summary.high + summary.medium + summary.low}</h3>
              <p>Total Issues</p>
            </div>
          </Card>
          
          <Card className="summary-card summary-high">
            <div className="summary-icon">🔴</div>
            <div className="summary-info">
              <h3>{summary.high}</h3>
              <p>High Severity</p>
            </div>
          </Card>
          
          <Card className="summary-card summary-medium">
            <div className="summary-icon">🟡</div>
            <div className="summary-info">
              <h3>{summary.medium}</h3>
              <p>Medium Severity</p>
            </div>
          </Card>
          
          <Card className="summary-card summary-low">
            <div className="summary-icon">🟢</div>
            <div className="summary-info">
              <h3>{summary.low}</h3>
              <p>Low Severity</p>
            </div>
          </Card>
        </div>
        
        <Card>
          <div className="filter-bar">
            <h2>Vulnerabilities Found</h2>
            <div className="filter-buttons">
              <button
                className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                onClick={() => setFilter('all')}
              >
                All
              </button>
              <button
                className={`filter-btn ${filter === 'high' ? 'active' : ''}`}
                onClick={() => setFilter('high')}
              >
                High ({summary.high})
              </button>
              <button
                className={`filter-btn ${filter === 'medium' ? 'active' : ''}`}
                onClick={() => setFilter('medium')}
              >
                Medium ({summary.medium})
              </button>
              <button
                className={`filter-btn ${filter === 'low' ? 'active' : ''}`}
                onClick={() => setFilter('low')}
              >
                Low ({summary.low})
              </button>
            </div>
          </div>
          
          {vulnerabilities.length === 0 ? (
            <div className="no-vulnerabilities">
              <div className="success-icon">✅</div>
              <h3>No {filter !== 'all' ? filter + ' severity' : ''} vulnerabilities found!</h3>
              <p>Your code looks secure based on our analysis.</p>
            </div>
          ) : (
            <div className="vulnerabilities-list">
              {vulnerabilities.map(({ vuln, idx }) => {
                const llmKey = `${vuln.test_id}_${idx}`;
                return (
                  <VulnerabilityCard
                    key={idx}
                    vulnerability={vuln}
                    llmInsight={report.llm_insights?.[llmKey]}
                  />
                );
              })}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default ReportView;