from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from modules.database import Database
from modules.auth import AuthManager
from modules.voting import VotingSystem
from modules.biometric import BiometricAuth
from modules.admin import AdminSystem

from deepface import DeepFace
import os
import base64

import csv
from io import StringIO
from flask import Response

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "local-development-secret")

# ---------------- INIT ----------------

db = Database()
auth = AuthManager(db)
voting = VotingSystem(db)
biometric = BiometricAuth()
admin_system = AdminSystem(db)
FACE_DIR = os.path.join(app.root_path, "static", "faces")

if not os.path.exists(FACE_DIR):
    os.makedirs(FACE_DIR)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        data = request.get_json()

        name = data.get("name")
        age = data.get("age")
        password = data.get("password")
        pin = data.get("pin")

        success, message, voter_id = auth.register_user(
            name,
            age,
            password,
            pin
        )

        if success:
            return jsonify({
                "success": True,
                "message": message,
                "voter_id": voter_id
            })

        return jsonify({
            "success": False,
            "message": message
        })

        

    return render_template("register.html")

@app.route("/registration_success/<voter_id>")
def registration_success(voter_id):
    return render_template(
        "registration_success.html",
        voter_id=voter_id
    )


# ---------------- FACE REGISTRATION ----------------

@app.route("/face_register/<voter_id>")
def face_register(voter_id):
    return render_template("face_capture.html", voter_id=voter_id)


@app.route("/save_face/<voter_id>", methods=["POST"])
def save_face(voter_id):
    face_data = request.form.get("face_data")
    success, result = biometric.save_face(
        voter_id,
        face_data
    )
    print("SUCCESS = ", success)
    print("RESULT = ", result)
    if not success:
        print("Inside duplicate block")


        db.delete_user(voter_id)
        flash(result, "error")
        return redirect(url_for("register"))
    print("Success block")

    flash("Face registered successfully", "success")
    return redirect(url_for("login_page"))
       



# ---------------- LOGIN ----------------

@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/login_auth", methods=["POST"])
def login():

    data = request.get_json()

    voter_id = data.get("voter_id")
    password = data.get("password")
    pin = data.get("pin")
    face_data = data.get("face_data")

    # STEP 1 → NORMAL LOGIN
    success, message, user = auth.login_user(
        voter_id,
        password,
        pin
    )

    if not success:
        return jsonify({
            "success": False,
            "message": message
        })

    # STEP 2 → CHECK FACE
    if not face_data:
        return jsonify({
            "success": False,
            "message": "Face not captured"
        })

    verified = biometric.verify_face(
    voter_id,
    face_data
    )

    if verified:

      session["user_id"] = user["id"]
      session["voter_id"] = voter_id

      return jsonify({
        "success": True,
        "message": "Login successful"
      })

    return jsonify({
      "success": False,
      "message": "Face verification failed"
    })
# ---------------- VOTING ----------------
@app.route("/vote")
def vote_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    success, msg, elections = voting.get_active_elections()

    if not success:
        return msg

    if not elections:
        return render_template(
            "vote.html",
            candidates=[],
            election_id=None
        )

    # Take the first active election
    active_election = elections[0]

    success, msg, candidates = voting.get_candidates_by_election(
        active_election["id"]
    )

    return render_template(
        "vote.html",
        candidates=candidates,
        election_id=active_election["id"],
        active_election_name=active_election["name"]
    )



@app.route("/cast_vote", methods=["POST"])
def cast_vote():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    

    user_id = session["user_id"]
    candidate_id = request.form.get("candidate_id")
    election_id = request.form.get("election_id")

    print("Candidate:", candidate_id)
    print("Election:", election_id)
    print("User:", session["user_id"])

    success, msg, _ = voting.cast_vote(
        session["user_id"],
        candidate_id,
        election_id
    )
    if success:
        return redirect(url_for("vote_success"))

    flash(msg, "error")
    return redirect(url_for("vote_page"))


@app.route("/vote_success")
def vote_success():
    return render_template("vote_success.html")     

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login_page"))

# ---------------- ADMIN ROUTES ----------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        success, message = admin_system.admin_login(
            username,
            password
        )
        print("Username:", username)
        print("Password:", password)
        print("Success:", success)
        print("Message:", message)
        if success:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

        return render_template("admin_login.html", error = message)

    return render_template("admin_login.html")

@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    # ---------- HANDLE FORMS ----------
    if request.method == "POST":

        action = request.form.get("action")

        # Add Election
        if action == "add_election":

            name = request.form["name"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]

            success, msg, election_id = voting.create_election(
                name,
                start_date,
                end_date
            )

            print("Election:", success, msg)

        # Add Candidate
        elif action == "add_candidate":

            candidate_name = request.form["candidate_name"]
            party_name = request.form["party_name"]
            election_id = request.form["election_id"]

            success, msg, candidate_id = voting.add_candidate(
                candidate_name,
                party_name,
                election_id
            )

            print("Candidate:", success, msg)

        return redirect(url_for("admin_dashboard"))

    # ---------- LOAD DATA ----------
    success_e, msg_e, elections = voting.get_all_elections()
    success_c, msg_c, candidates = voting.get_all_candidates()

    return render_template(
        "admin_dashboard.html",
        elections=elections,
        candidates=candidates
    )
@app.route("/edit_election/<int:id>", methods=["GET", "POST"])
def edit_election(id):

    if request.method == "POST":
        name = request.form.get("name")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        voting.update_election(
            id,
            name,
            start_date,
            end_date
        )

        return redirect(url_for("admin_dashboard"))

    success, msg, election = voting.get_election_by_id(id)

    return render_template(
        "edit_election.html",
        election=election
    )

@app.route("/delete_election/<int:id>", methods=["POST"])
def delete_election(id):
    voting.delete_election(id)
    return redirect(url_for("admin_dashboard"))

@app.route("/edit_candidate/<int:id>", methods=["GET", "POST"])
def edit_candidate(id):

    if request.method == "POST":

        name = request.form.get("name")
        party = request.form.get("party")
        election_id = int(request.form.get("election_id"))

        voting.update_candidate(
            id,
            name,
            party,
            election_id
        )

        return redirect(url_for("admin_dashboard"))

    success, msg, candidates = voting.get_all_candidates()

    candidate = next(
        (c for c in candidates if c["id"] == id),
        None
    )

    success_e, msg_e, elections = voting.get_all_elections()

    return render_template(
        "edit_candidate.html",
        candidate=candidate,
        elections=elections
    )

@app.route("/delete_candidate/<int:id>", methods=["POST"])
def delete_candidate(id):

    voting.delete_candidate(id)

    return redirect(url_for("admin_dashboard"))



@app.route("/view_statistics/<int:election_id>")
def view_statistics(election_id):

    success, data = voting.get_election_results(election_id)

    if success:
        return render_template(
            "statistics.html",
            total_votes=data["total_votes"],
            candidates=data["candidates"],
            winner=data["winner"]
        )

    return redirect(url_for("admin_dashboard"))

@app.route("/export_statistics/<int:election_id>")
def export_statistics(election_id):

    success, data = voting.get_election_results(election_id)

    if not success:
        return redirect(url_for("admin_dashboard"))

    si = StringIO()
    cw = csv.writer(si)

    cw.writerow([
        "Candidate",
        "Party",
        "Votes",
        "Percentage"
    ])

    for c in data["candidates"]:
        cw.writerow([
            c["name"],
            c["party"],
            c["vote_count"],
            f"{c['percentage']}%"
        ])

    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename=election_{election_id}_results.csv"
        }
    )
# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)


