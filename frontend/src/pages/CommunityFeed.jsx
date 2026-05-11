import React, { useEffect, useState } from 'react';
import { communityAPI } from '../api/communityApi';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import './CommunityFeed.css';

const CommunityFeed = () => {
  const [feedData, setFeedData] = useState([]);
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchCommunityData();
  }, []);
  
  const fetchCommunityData = async () => {
    try {
      const [feedResponse, trendingResponse] = await Promise.all([
        communityAPI.getFeed(),
        communityAPI.getTrending(),
      ]);
      
      setFeedData(feedResponse.feed || []);
      setTrending(trendingResponse.trending || []);
    } catch (error) {
      console.error('Failed to fetch community data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return (
      <div className="community-loading">
        <Spinner size="large" />
        <p>Loading community insights...</p>
      </div>
    );
  }
  
  return (
    <div className="community-page">
      <div className="container">
        <div className="community-header">
          <h1>Community Feed</h1>
          <p>Learn from common vulnerabilities discovered by the community</p>
        </div>
        
        <div className="community-grid">
          <div className="main-feed">
            <Card title="🔥 Trending Vulnerabilities">
              {trending.length === 0 ? (
                <div className="empty-feed">
                  <p>No trending data available yet.</p>
                  <p className="empty-subtitle">
                    As more developers use Xpos3, we'll show common vulnerabilities here!
                  </p>
                </div>
              ) : (
                <div className="trending-list">
                  {trending.map((item, index) => (
                    <div key={index} className="trending-item">
                      <div className="trending-rank">#{index + 1}</div>
                      <div className="trending-info">
                        <h3>{item.vulnerability_type}</h3>
                        <p>{item.occurrence_count} occurrences</p>
                      </div>
                      <span className={`severity-tag ${item.severity.toLowerCase()}`}>
                        {item.severity}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </Card>
            
            <Card title="📊 Security Insights">
              <div className="insights-grid">
                <div className="insight-card">
                  <div className="insight-icon">🔒</div>
                  <h3>Input Validation</h3>
                  <p>Always validate and sanitize user input to prevent injection attacks</p>
                </div>
                
                <div className="insight-card">
                  <div className="insight-icon">🔑</div>
                  <h3>Secret Management</h3>
                  <p>Never hardcode API keys or passwords in your source code</p>
                </div>
                
                <div className="insight-card">
                  <div className="insight-icon">🛡️</div>
                  <h3>SQL Injection</h3>
                  <p>Use parameterized queries to prevent SQL injection vulnerabilities</p>
                </div>
                
                <div className="insight-card">
                  <div className="insight-icon">⚠️</div>
                  <h3>Error Handling</h3>
                  <p>Implement proper error handling to avoid information disclosure</p>
                </div>
              </div>
            </Card>
          </div>
          
          <div className="sidebar">
            <Card title="📚 Learning Resources">
              <div className="resources-list">
                <a href="https://owasp.org/www-project-top-ten/" target="_blank" rel="noopener noreferrer" className="resource-link">
                  <span className="resource-icon">📖</span>
                  <div>
                    <h4>OWASP Top 10</h4>
                    <p>Most critical web application security risks</p>
                  </div>
                </a>
                
                <a href="https://cwe.mitre.org/top25/" target="_blank" rel="noopener noreferrer" className="resource-link">
                  <span className="resource-icon">🎯</span>
                  <div>
                    <h4>CWE Top 25</h4>
                    <p>Most dangerous software weaknesses</p>
                  </div>
                </a>
                
                <a href="https://bandit.readthedocs.io/" target="_blank" rel="noopener noreferrer" className="resource-link">
                  <span className="resource-icon">🔍</span>
                  <div>
                    <h4>Bandit Docs</h4>
                    <p>Learn about Python security analysis</p>
                  </div>
                </a>
              </div>
            </Card>
            
            <Card title="💡 Quick Tips">
              <div className="tips-list">
                <div className="tip-item">
                  <span className="tip-icon">✅</span>
                  <p>Scan your code regularly during development</p>
                </div>
                <div className="tip-item">
                  <span className="tip-icon">✅</span>
                  <p>Address high-severity issues first</p>
                </div>
                <div className="tip-item">
                  <span className="tip-icon">✅</span>
                  <p>Keep your dependencies up to date</p>
                </div>
                <div className="tip-item">
                  <span className="tip-icon">✅</span>
                  <p>Review AI-generated fixes carefully</p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CommunityFeed;