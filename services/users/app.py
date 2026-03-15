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


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
    rows = cur.fetchall()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "created_at": str(row[3])
        })

    cur.close()
    conn.close()

    return jsonify(users), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, email, created_at FROM users WHERE id = %s",
        (user_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"message": "user not found"}), 404

    user = {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "created_at": str(row[3])
    }

    return jsonify(user), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"message": "invalid json"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, username, email, created_at
            """,
            (username, email, password)
        )
        row = cur.fetchone()
        conn.commit()

        user = {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "created_at": str(row[3])
        }

        return jsonify({
            "message": "user created",
            "user": user
        }), 201

    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"message": "database error", "error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "invalid json"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    existing_user = cur.fetchone()

    if not existing_user:
        cur.close()
        conn.close()
        return jsonify({"message": "user not found"}), 404

    cur.execute(
        """
        UPDATE users
        SET username = %s, email = %s, password_hash = %s
        WHERE id = %s
        RETURNING id, username, email, created_at
        """,
        (username, email, password, user_id)
    )

    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    updated_user = {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "created_at": str(row[3])
    }

    return jsonify({
        "message": "user updated",
        "user": updated_user
    }), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    existing_user = cur.fetchone()

    if not existing_user:
        cur.close()
        conn.close()
        return jsonify({"message": "user not found"}), 404

    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "user deleted"}), 200


@app.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "invalid json"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, email FROM users WHERE email = %s AND password_hash = %s",
        (email, password)
    )
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return jsonify({"message": "invalid credentials"}), 401

    return jsonify({
        "message": "login ok",
        "user": {
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)