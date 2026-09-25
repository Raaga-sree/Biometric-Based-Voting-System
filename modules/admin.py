from modules.database import Database
from modules.voting import VotingSystem

class AdminSystem:
    def __init__(self, db):
        self.db = db
        self.voting = VotingSystem(db)
    
    def admin_login(self, username, password):
        if username == "raagasree" and password == "admin123":
            return True, "Admin authentication successful"
        return False, "Invalid admin credentials"
    
    def get_voter_statistics(self):
        try:
            if not self.db.connect():
                return False, "Database connection failed", {}
            
            cursor = self.db.conn.cursor(dictionary=True)
            
            cursor.execute("SELECT COUNT(*) AS total_voters FROM users")
            total_voters = cursor.fetchone()['total_voters']
            
            cursor.execute("SELECT COUNT(DISTINCT user_id) AS voted_voters FROM votes")
            voted_voters = cursor.fetchone()['voted_voters']
            
            percentage = (voted_voters / total_voters * 100) if total_voters else 0
            
            stats = {
                "total_voters": total_voters,
                "voted_voters": voted_voters,
                "voting_percentage": round(percentage, 2)
            }
            
            cursor.close()
            self.db.disconnect()
            return True, "Statistics retrieved successfully", stats
            
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, f"Error retrieving statistics: {str(e)}", {}
    
    def get_all_users(self):
        try:
            if not self.db.connect():
                return False, "Database connection failed", []
            
            cursor = self.db.conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, username, voter_id, created_at FROM users")
            users = cursor.fetchall()
            
            cursor.close()
            self.db.disconnect()
            return True, "Users retrieved successfully", users
            
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, f"Error retrieving users: {str(e)}", []
    
    def delete_user(self, user_id):
        try:
            if not self.db.connect():
                return False, "Database connection failed"
            
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM votes WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db.conn.commit()
            
            rows = cursor.rowcount
            cursor.close()
            self.db.disconnect()
            
            return (True, "User deleted successfully") if rows else (False, "User not found")
                
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, f"Error deleting user: {str(e)}"
    
    def get_all_votes(self):
        try:
            if not self.db.connect():
                return False, "Database connection failed", []
            
            cursor = self.db.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT v.id, u.name AS voter_name, c.name AS candidate_name,
                       e.name AS election_name, v.vote_time
                FROM votes v
                JOIN users u ON v.user_id = u.id
                JOIN candidates c ON v.candidate_id = c.id
                JOIN elections e ON v.election_id = e.id
                ORDER BY v.vote_time DESC
            """)
            
            votes = cursor.fetchall()
            cursor.close()
            self.db.disconnect()
            return True, "Votes retrieved successfully", votes
            
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, f"Error retrieving votes: {str(e)}", []
