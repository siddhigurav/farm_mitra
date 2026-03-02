#!/usr/bin/env python3
"""
Script to initialize and run the Insect Monitoring System instance.
This script handles environment setup and application initialization.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python 3.8+ is installed"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        return False
    print(f"✓ Python version {sys.version} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    backend_dir = Path("insect_monitoring_system/backend")
    requirements_path = backend_dir / "requirements.txt"
    
    if not requirements_path.exists():
        print(f"Error: Requirements file not found at {requirements_path}")
        return False
    
    try:
        # Install requirements directly using the current Python environment
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    except FileNotFoundError as e:
        print(f"Error: Could not find pip executable: {e}")
        return False

def initialize_database():
    """Initialize the database (placeholder for actual implementation)"""
    print("Initializing database...")
    # In a real implementation, this would:
    # 1. Create database tables
    # 2. Apply migrations if needed
    # 3. Insert initial data
    print("✓ Database initialized (placeholder)")
    return True

def setup_ml_models():
    """Setup ML models (placeholder for actual implementation)"""
    print("Setting up ML models...")
    # In a real implementation, this would:
    # 1. Download pre-trained models if needed
    # 2. Verify model files exist
    # 3. Initialize model loading
    print("✓ ML models setup (placeholder)")
    return True

def validate_setup():
    """Run validation tests to ensure everything is working"""
    print("Running validation tests...")
    try:
        # Run the existing test script
        result = subprocess.run([sys.executable, "test_app.py"], 
                              capture_output=True, text=True, check=True)
        print("✓ Validation tests passed")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("✗ Validation tests failed:")
        print(e.stdout)
        print(e.stderr)
        return False

def start_application():
    """Start the application using the run.py script"""
    print("Starting application...")
    try:
        # Run the existing run script
        subprocess.run([sys.executable, "run.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}")
        return False

def main():
    """Main initialization function"""
    print("=" * 60)
    print("INSECT MONITORING SYSTEM - INSTANCE INITIALIZATION")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("Failed to initialize database")
        sys.exit(1)
    
    # Setup ML models
    if not setup_ml_models():
        print("Failed to setup ML models")
        sys.exit(1)
    
    # Validate setup
    if not validate_setup():
        print("Setup validation failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("INSTANCE INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("To start the application, run: python run.py")
    print("Or use this script with: python initialize_instance.py --start")
    print("=" * 60)
    
    # Check if we should start the application
    if "--start" in sys.argv:
        start_application()

if __name__ == "__main__":
    main()