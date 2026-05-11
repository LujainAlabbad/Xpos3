import React from 'react';
import { Link } from 'react-router-dom';
import './Landing.css';

const Landing = () => {
  return (
    <div className="landing-page">
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">
              Secure Your Python Code with <span className="highlight">Xpos3</span>
            </h1>
            <p className="hero-description">
              An accessible vulnerability scanner designed for novice developers. 
              Identify security flaws, understand risks, and learn how to fix them.
            </p>
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-large">
                Get Started Free
              </Link>
              <Link to="/login" className="btn btn-outline btn-large">
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </section>
      
      <section className="features">
        <div className="container">
          <h2 className="section-title">Why Choose Xpos3?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Automated Scanning</h3>
              <p>Upload your Python code and get instant security analysis powered by Bandit</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📚</div>
              <h3>Educational Reports</h3>
              <p>Understand vulnerabilities with clear explanations and actionable fixes</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🛡️</div>
              <h3>Industry Standards</h3>
              <p>Detect OWASP Top 10 and CWE Top 25 vulnerabilities</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3>Community Learning</h3>
              <p>Learn from common vulnerabilities found by other developers</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Landing;