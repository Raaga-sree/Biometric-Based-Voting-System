"""
Test script for the Biometric Voting System modules.
This script tests the functionality of various modules.
"""

from modules.auth import AuthManager
from modules.biometric import BiometricAuth
from modules.voting import VotingSystem

def test_auth_module():
    """Test the authentication module"""
    print("Testing Auth module...")
    auth = AuthManager()
    
    # Test password hashing
    password = "test_password"
    hashed = auth.hash_password(password)
    print(f"Hashed password: {hashed[:20]}...")
    
    # Test password verification
    is_valid = auth.verify_password(hashed, password)
    print(f"Password verification: {'Success' if is_valid else 'Failed'}")
    
    is_invalid = auth.verify_password(hashed, "wrong_password")
    print(f"Wrong password verification: {'Failed' if not is_invalid else 'Error'}")

def test_biometric_module():
    """Test the biometric module"""
    print("\nTesting Biometric module...")
    bio = BiometricAuth()
    
    # Test face capture simulation
    face_data = bio.simulate_face_capture()
    print(f"Face data: {face_data[:20]}...")
    
    # Test fingerprint capture simulation
    fingerprint_data = bio.simulate_fingerprint_capture()
    print(f"Fingerprint data: {fingerprint_data[:20]}...")
    
    # Test verification
    is_match = bio.verify_biometric(face_data, face_data)
    print(f"Biometric verification (same data): {'Success' if is_match else 'Failed'}")
    
    is_not_match = bio.verify_biometric(face_data, fingerprint_data)
    print(f"Biometric verification (different data): {'Failed' if not is_not_match else 'Error'}")

def test_voting_module():
    """Test the voting module"""
    print("\nTesting Voting module...")
    voting = VotingSystem()
    
    # Test election creation
    result = voting.create_election(
        "Test Election", 
        "2025-12-01", 
        "2025-12-15"
    )
    
    # Handle both cases: with and without database connection
    if len(result) == 3:
        success, message, election_id = result
    else:
        success, message = result
        election_id = None
    
    print(f"Election creation: {message}")
    
    if success and election_id:
        print(f"Created election with ID: {election_id}")
        
        # Test adding candidate
        result = voting.add_candidate(
            "Test Candidate", 
            "Test Party", 
            election_id
        )
        
        # Handle both cases: with and without database connection
        if len(result) == 3:
            success, message, candidate_id = result
        else:
            success, message = result
            candidate_id = None
        
        print(f"Candidate addition: {message}")
        
        if success and candidate_id:
            print(f"Added candidate with ID: {candidate_id}")

def main():
    """Run all tests"""
    print("Running tests for Biometric Voting System modules...\n")
    
    test_auth_module()
    test_biometric_module()
    test_voting_module()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()