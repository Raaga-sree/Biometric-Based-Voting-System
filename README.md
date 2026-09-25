# Biometric Based Secure Voting System

This is a web-based voting system that uses biometric authentication to ensure secure and transparent elections. The system uses face recognition and fingerprint simulation for voter verification and prevents duplicate or unauthorized voting.

## Features

- **User Management**: Voter registration, login, and authentication
- **Biometric Authentication**: Face recognition and fingerprint simulation
- **Secure Voting**: One vote per user per election with duplicate prevention
- **Admin Panel**: Election and candidate management with voting statistics
- **Database Storage**: MySQL database for storing users, votes, candidates, and elections

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Biometric Libraries**: OpenCV, face_recognition
- **Database**: MySQL

## Project Structure

```
project/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/             # CSS, JavaScript, and images
│   ├── css/
│   ├── js/
│   └── images/
└── modules/            # Application modules
    ├── auth.py         # Authentication module
    ├── biometric.py    # Biometric authentication module
    ├── database.py     # Database operations module
    ├── voting.py       # Voting system module
    └── admin.py        # Admin panel module
```

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up MySQL database and configure connection in `modules/database.py`
4. Run the application:
   ```
   python app.py
   ```

## Usage

1. **Voter Registration**: Users can register with their personal details, username, password, and PIN
2. **Voter Login**: Registered users can log in with their credentials
3. **Biometric Authentication**: Users must complete biometric verification before voting
4. **Voting**: Users can view active elections and cast their votes
5. **Admin Panel**: Administrators can manage elections, candidates, and view voting statistics

## Security Measures

- Multi-factor authentication (Username/Password + PIN + Biometrics)
- Prevention of duplicate voting
- Secure password hashing with salt
- Vote locking after successful submission
- Database integrity with foreign key relationships

## Modules

### 1. User Management Module
- User registration with personal details
- Secure login using username/password
- PIN generation and validation
- Session management

### 2. Biometric Authentication Module
- Face image capture using webcam
- Face encoding and verification
- Fingerprint authentication (simulated)
- Multi-factor authentication

### 3. Voting Module
- Display active elections
- Candidate selection
- Vote casting with confirmation
- Prevention of duplicate voting

### 4. Admin Module
- Admin login authentication
- Add and delete elections
- Add and remove candidates
- Monitor live voting results

### 5. Database Module
- Users Table: User registration and authentication data
- Votes Table: Vote records
- Elections Table: Election details
- Candidates Table: Candidate information

## Future Enhancements

- Integration with actual fingerprint scanning hardware
- Real-time face recognition during voting
- Blockchain integration for vote immutability
- Mobile application development
- Advanced analytics and reporting

## License

This project is for educational purposes only.