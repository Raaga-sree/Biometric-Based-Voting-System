from modules.database import Database
from datetime import datetime, date

class VotingSystem:
    def __init__(self, db):
        self.db = db
    
    def create_election(self, name, start_date, end_date):
        try:
            if not self.db.connect():
                return False, "Database connection failed", None
            
            election_id = self.db.insert_election(name, start_date, end_date)
            self.db.disconnect()
            
            if election_id:
                return True, "Election created successfully", election_id
            else:
                return False, "Failed to create election", None
                
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, f"Election creation error: {str(e)}", None
    
    def get_active_elections(self):
        try:
            if not self.db.connect():
                return False, "Database connection failed", []
            
            elections = self.db.get_all_elections()
            print("Elections:", elections)
            print("Type:", type(elections))
            active_elections = []
            today = date.today()
            
            for election in elections:
                start_date = election["start_date"]
                end_date = election["end_date"]
                
                if isinstance(start_date, datetime):
                    start_date = start_date.date()
                if isinstance(end_date, datetime):
                    end_date = end_date.date()

                if start_date <= today <= end_date:
                    active_elections.append(election)
            
            self.db.disconnect()
            return True, "Elections retrieved successfully", active_elections
            
        except Exception as e:
                self.db.disconnect()
                return False, f"Error retrieving elections: {str(e)}", []

    def get_all_elections(self):
        try:
          if not self.db.connect():
            return False, "Database connection failed", []

          cursor = self.db.conn.cursor(dictionary=True)
          cursor.execute("SELECT * FROM elections")
          elections = cursor.fetchall()

          cursor.close()
          self.db.disconnect()

          return True, "Success", elections

        except Exception as e:
           if self.db.conn:
              self.db.disconnect()
        return False, str(e), []

    
    def add_candidate(self, name, party, election_id):
        try:
            if not self.db.connect():
                return False, "Database connection failed", None
            
            cursor = self.db.conn.cursor()
            query = "INSERT INTO candidates (name, party, election_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, party, election_id))
            self.db.conn.commit()
            candidate_id = cursor.lastrowid
            
            cursor.close()
            self.db.disconnect()
            
            if candidate_id:
                return True, "Candidate added successfully", candidate_id
            else:
                return False, "Failed to add candidate", None
                
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, f"Error adding candidate: {str(e)}", None
    
    def get_candidates_by_election(self, election_id):
        try:
            if not self.db.connect():
                return False, "Database connection failed", []
            
            cursor = self.db.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM candidates WHERE election_id = %s", (election_id,))
            candidates = cursor.fetchall()
            
            cursor.close()
            self.db.disconnect()
            return True, "Candidates retrieved successfully", candidates
            
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, f"Error retrieving candidates: {str(e)}", []
    

    def has_user_voted(self, user_id, election_id):
        try:
            cursor = self.db.get_cursor()
            cursor.execute(
                "SELECT id FROM votes WHERE user_id=%s AND election_id=%s",
                (user_id, election_id)
            )
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Exception as e:
            return False, str(e), None

    def cast_vote(self, user_id, candidate_id, election_id):
        try:
            if self.has_user_voted(user_id, election_id):
                return False, "Already voted", None

            cursor = self.db.get_cursor()
            cursor.execute(
                "INSERT INTO votes(user_id, candidate_id, election_id) VALUES(%s, %s, %s)",
                (user_id, candidate_id, election_id)
            )
            self.db.conn.commit()
            cursor.close()

            return True, "Vote cast successfully", None

        except Exception as e:
            return False, str(e), None
        

    def get_election_results(self, election_id):
        try:
            if not self.db.connect():
                return False, "Database connection failed", {}
            
            cursor = self.db.conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT COUNT(*) AS total_votes FROM votes WHERE election_id=%s",
                (election_id,)
            )
            total_votes = cursor.fetchone()['total_votes']

            #Get vote count per candidate
            query = """
            SELECT c.id, c.name, c.party,
                   COUNT(v.id) AS vote_count
            FROM candidates c
            LEFT JOIN votes v ON c.id = v.candidate_id
            WHERE c.election_id = %s
            GROUP BY c.id
            ORDER BY vote_count DESC
            """

            cursor.execute(query, (election_id,))
            results = cursor.fetchall()

            candidates_list = []

            #calculate percentage
            for row in results:
                if total_votes > 0:
                    row['percentage'] = round(
                    (row['vote_count'] / total_votes) * 100,2
                    )
                else:
                    row['percentage'] = 0
                candidates_list.append(row)
            winner = candidates_list[0] if candidates_list else None

            cursor.close()
            self.db.disconnect()

            return True,{
                "total_votes": total_votes,
                "candidates": candidates_list,
                "winner": winner
            }
        except Exception as e:
            return False, str(e)

            
    def get_all_candidates(self):
        try:
           if not self.db.connect():
              return False, "Database connection failed", []

           cursor = self.db.conn.cursor(dictionary=True)
           cursor.execute("""
            SELECT 
                c.id,
                c.name,
                c.party,
                e.name AS election_name
            FROM candidates c
            JOIN elections e ON c.election_id = e.id
        """)
           candidates = cursor.fetchall()

           cursor.close()
           self.db.disconnect()
           return True, "Candidates retrieved successfully", candidates

        except Exception as e:
           if self.db.conn:
              self.db.disconnect()
           return False, f"Error retrieving candidates: {str(e)}", []

    def get_election_by_id(self, election_id):
        try:
            if not self.db.connect():
                return False, "Database connection failed", None

            cursor = self.db.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM elections WHERE id=%s", (election_id))
            election = cursor.fetchone()

            cursor.close()
            self.db.disconnect()

            return True, "Success", election
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, str(e), None

    def update_election(self, election_id, name, start_date, end_date):
        try:
           print("Inside update function ")

           if not self.db.connect():
             print("DB connection failed")
             return False, "Database connection failed"

           print("DB connected")

           cursor = self.db.conn.cursor()
           cursor.execute("""
              UPDATE elections 
              SET name=%s, start_date=%s, end_date=%s
              WHERE id=%s
           """, (name, start_date, end_date, election_id))

           self.db.conn.commit()

           print("Rows affected:", cursor.rowcount)

           cursor.close()
           self.db.disconnect()

           return True, "Election updated successfully"

        except Exception as e:
           print("ERROR:", e)
           if self.db.conn:
              self.db.disconnect()
           return False, str(e)

    def delete_election(self, election_id):
        try:
           if not self.db.connect():
              return False, "Database connection failed"

           cursor = self.db.conn.cursor()
           cursor.execute("DELETE FROM elections WHERE id=%s", (election_id,))
           self.db.conn.commit()

           cursor.close()
           self.db.disconnect()

           return True, "Election deleted successfully"

        except Exception as e:
           if self.db.conn:
             self.db.disconnect()
           return False, str(e)
    
    def delete_candidate(self, candidate_id):
        print("INSIDE DELETE FUNCTION")
        try:
            if not self.db.connect():
                return False, "Database connection failed"
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM  votes WHERE candidate_id=%s", (candidate_id,))
            print("Votes deleted:", cursor.rowcount)

            cursor.execute("DELETE FROM candidates WHERE id=%s", (candidate_id,))
            print("Candidates deleted:", cursor.rowcount)

            self.db.conn.commit()

            cursor.close()
            self.db.disconnect()
            return True, "Candidate deleted successfully"
        
        except Exception as e:
            if self.db.conn:
                self.db.disconnect()
            return False, str(e)


    def update_candidate(self, candidate_id, name, party, election_id):
            try:
                if not self.db.connect():
                    return False, "Database connection failed"

                cursor = self.db.conn.cursor()
                cursor.execute("""
                     UPDATE candidates
                     SET name=%s, party=%s, election_id=%s
                     WHERE id=%s
                """, (name, party, election_id, candidate_id))
                self.db.conn.commit()
                cursor.close()
                self.db.disconnect()

                return True, "Candidate updated successfully"
            except Exception as e:
                if self.db.conn:
                    self.db.disconnect()
                return False, str(e)   

                
    


