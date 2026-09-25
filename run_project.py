"""
Helper script to set up and run the Biometric Voting System project.
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install required Python packages"""
    print("Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask==2.3.3"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python==8.1.0"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def initialize_database():
    """Initialize the database tables"""
    print("Initializing database tables...")
    try:
        # Import and run the database initialization
        from init_db import init_database
        init_database()
        print("Database initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def run_application():
    """Run the Flask application"""
    print("Starting the Biometric Voting System...")
    try:
        # Set Flask environment variables
        os.environ['FLASK_APP'] = 'app.py'
        os.environ['FLASK_ENV'] = 'development'
        
        # Run the Flask application
        subprocess.call([sys.executable, "app.py"])
        return True
    except Exception as e:
        print(f"Error running application: {e}")
        return False

def main():
    """Main function to set up and run the project"""
    print("=" * 50)
    print("Biometric Based Secure Voting System")
    print("=" * 50)
    print("This script will help you set up and run the project.")
    print()
    
    # Check if user wants to install dependencies
    choice = input("Do you want to install dependencies? (y/n): ").lower().strip()
    if choice == 'y':
        if not install_dependencies():
            print("Failed to install dependencies. Please install them manually.")
            return
    
    # Check if user wants to initialize database
    choice = input("Do you want to initialize the database? (y/n): ").lower().strip()
    if choice == 'y':
        if not initialize_database():
            print("Failed to initialize database. Please check your MySQL setup.")
            return
    
    # Ask user if they want to run the application
    choice = input("Do you want to start the application? (y/n): ").lower().strip()
    if choice == 'y':
        print("\nStarting the application...")
        print("Access the application at: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the application.")
        run_application()
    else:
        print("Setup completed. You can run the application later with 'python app.py'")

if __name__ == "__main__":
    main()