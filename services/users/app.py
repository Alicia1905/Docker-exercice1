from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, username, email FROM users")

    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username,email,password_hash) VALUES (%s,%s,%s)",
        (data["username"], data["email"], data["password"])
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"message":"user created"}

@app.route("/users/login", methods=["POST"])
def login():

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE email=%s AND password_hash=%s",
        (data["email"], data["password"])
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return {"message":"login ok"}

    return {"message":"invalid credentials"},401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)