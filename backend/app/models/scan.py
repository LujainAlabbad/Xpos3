"""
Scan model for storing vulnerability scan results
"""
from app.extensions import db
from datetime import datetime

class Scan(db.Model):
    __tablename__ = 'scans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_hash = db.Column(db.String(64))  # no unique constraint — same file may be scanned multiple times
    status = db.Column(db.String(20), default='pending')  # pending, scanning, completed, failed
    bandit_report = db.Column(db.JSON)
    llm_insights = db.Column(db.JSON)
    severity_summary = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Scan {self.filename} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'status': self.status,
            'severity_summary': self.severity_summary,
            'created_at': self.created_at.isoformat() + 'Z',
            'completed_at': self.completed_at.isoformat() + 'Z' if self.completed_at else None
        }