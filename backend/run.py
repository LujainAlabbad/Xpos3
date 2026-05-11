"""
Application entry point for Flask development server
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.extensions import db

# Load environment variables
load_dotenv()

# Get environment from .env or default to 'development'
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask app
app = create_app(config_name)

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
    
    # Run the application
    print(f" Starting Xpos3 Backend on http://localhost:5000")
    print(f" Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(host='0.0.0.0', port=5000, debug=True)