"""
Community statistics model for tracking common vulnerabilities
"""
from app.extensions import db
from datetime import datetime

class CommunityStats(db.Model):
    __tablename__ = 'community_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    vulnerability_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    occurrence_count = db.Column(db.Integer, default=1)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CommunityStats {self.vulnerability_type} - {self.occurrence_count}>'