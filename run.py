#!/usr/bin/env python3
"""
Main script to run the complete insect monitoring system.
This script starts the Flask backend application with integrated frontend.
"""

import subprocess
import sys
import os
import time
import signal

# Global variables to track processes
processes = []

def signal_handler(sig, frame):
    """Handle CTRL+C gracefully"""
    print("\n\nShutting down application...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
            print(f"Process {process.pid} stopped")
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"Process {process.pid} killed")
        except Exception as e:
            print(f"Error stopping process {process.pid}: {e}")
    
    print("Application stopped. Goodbye!")
    sys.exit(0)

def start_application():
    """Start the Flask application"""
    print("Starting Flask application...")
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "insect_monitoring_system", "backend")
    
    if not os.path.exists(backend_dir):
        print(f"Error: Backend directory not found at {backend_dir}")
        return None
        
    try:
        # Start Flask process
        # Let the child process inherit stdout/stderr so logs are visible
        # and the pipes do not fill up (which can cause the process to exit).
        flask_process = subprocess.Popen([
            sys.executable, "-m", "flask", "run",
            "--host=127.0.0.1", "--port=5000", "--no-reload"
        ], cwd=backend_dir, stdout=None, stderr=None,
        env=dict(os.environ, FLASK_APP="app.main"))
        
        processes.append(flask_process)
        print("✓ Flask application started with PID:", flask_process.pid)
        print("  Application will be available at: http://127.0.0.1:5000")
        return flask_process
    except Exception as e:
        print(f"✗ Error starting Flask application: {e}")
        return None

def monitor_processes():
    """Monitor running processes and exit if any stops unexpectedly"""
    while True:
        time.sleep(1)
        for process in processes:
            if process.poll() is not None:
                print(f"\n⚠ Process {process.pid} has stopped unexpectedly")
                # If any process stops, terminate all others
                signal_handler(signal.SIGINT, None)
                return

def main():
    print("=" * 60)
    print("INSECT MONITORING SYSTEM - PYTHON/FLASK APPLICATION")
    print("=" * 60)
    print("Tech Stack: Python, Flask, Machine Learning, HTML, CSS, JavaScript")
    print("=" * 60)
    
    # Start Flask application
    flask_process = start_application()
    if not flask_process:
        print("✗ Failed to start Flask application. Exiting.")
        return
    
    print("\n" + "=" * 60)
    print("APPLICATION STARTED SUCCESSFULLY!")
    print("=" * 60)
    print("Access the application at: http://127.0.0.1:5000")
    print("=" * 60)
    print("Press CTRL+C to stop the application")
    print("=" * 60)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Monitor processes
    try:
        monitor_processes()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()