"""
Database initialization script for the Biometric Voting System.
This script creates the necessary database tables.
"""

from modules.database import Database

def init_database():
    """Initialize the database with required tables"""
    print("Initializing database...")
    
    # Create database connection
    db = Database()
    
    # Connect to database
    if db.connect():
        print("Connected to database successfully")
        
        # Create tables
        if db.create_tables():
            print("Database tables created successfully")
        else:
            print("Failed to create database tables")
        
        # Disconnect from database
        db.disconnect()
        print("Disconnected from database")
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    init_database()