from werkzeug.security import generate_password_hash, check_password_hash
import random
import string


class AuthManager:

    def __init__(self, db):
        self.db = db

    # ---------------- GENERATE VOTER ID ----------------
    def generate_voter_id(self):

        while True:
            voter_id = "VOTE" + ''.join(
                random.choices(string.digits, k=6)
            )

            existing = self.db.get_user_by_voter_id(voter_id)

            if not existing:
                return voter_id

    # ---------------- REGISTER ----------------
    def register_user(self, name, age, password, pin):

        voter_id = self.generate_voter_id()

        password_hash = generate_password_hash(password)
        pin_hash = generate_password_hash(pin)

        self.db.insert_user(
            name=name,
            age=age,
            voter_id=voter_id,
            password_hash=password_hash,
            pin_hash=pin_hash
        )

        return True, "Registration successful", voter_id

    # ---------------- LOGIN ----------------
    def login_user(self, voter_id, password, pin):

        user = self.db.get_user_by_voter_id(voter_id)

        if not user:
            return False, "User not found", None

        # password check
        if not check_password_hash(
            user["password_hash"],
            password
        ):
            return False, "Invalid password", None

        # pin check
        if not check_password_hash(
            user["pin_hash"],
            pin
        ):
            return False, "Invalid PIN", None

        return True, "Login successful", user