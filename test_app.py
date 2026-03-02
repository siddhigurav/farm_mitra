#!/usr/bin/env python3
"""
Test script to verify the Flask application functionality.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'insect_monitoring_system', 'backend'))

def test_flask_app():
    """Test that the Flask app can be imported and has the expected routes"""
    try:
        from app.main import app
        
        # Create a test client
        with app.test_client() as client:
            # Test the main route
            response = client.get('/')
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
            
            # Test the health check route
            response = client.get('/api/health')
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
            
            # Test the stats route
            response = client.get('/api/stats')
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
            
        print("✓ All Flask app tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Flask application...")
    success = test_flask_app()
    if success:
        print("All tests passed! The application is ready to run.")
    else:
        print("Some tests failed. Please check the application.")
        sys.exit(1)