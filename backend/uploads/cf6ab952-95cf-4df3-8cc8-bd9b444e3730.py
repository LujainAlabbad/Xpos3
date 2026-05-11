from datetime import datetime
from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False, unique=True)
    icon       = db.Column(db.String(50), nullable=True)   # icon name e.g. "wrench"
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    providers  = db.relationship("ProviderProfile", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category {self.name}>"