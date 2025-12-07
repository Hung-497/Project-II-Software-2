from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to your database
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",  # your MySQL password
        database="demogame"
    )

# Endpoint to submit score
@app.route("/submit-score", methods=["POST"])
def submit_score():
    data = request.json
    player_name = data.get("player_name")
    score = data.get("score")  # could be tries_used

    if not player_name or score is None:
        return jsonify({"error": "Missing player_name or score"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leaderboard (player_name, score) VALUES (%s, %s)",
        (player_name, score)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Score submitted successfully"}), 200

# Endpoint to get leaderboard
@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # fewer tries - better score
    cursor.execute("SELECT player_name, score FROM leaderboard ORDER BY score ASC LIMIT 10")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
