import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "orders-db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "orders_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://products-service:5000")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/orders", methods=["GET"])
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, user_id, product_id, quantity, total_price, status, created_at
        FROM orders
        ORDER BY id ASC
    """)
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(orders), 200


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, user_id, product_id, quantity, total_price, status, created_at
        FROM orders
        WHERE id = %s
    """, (order_id,))
    order = cur.fetchone()
    cur.close()
    conn.close()

    if not order:
        return jsonify({"error": "Commande introuvable"}), 404

    return jsonify(order), 200


@app.route("/orders/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, user_id, product_id, quantity, total_price, status, created_at
        FROM orders
        WHERE user_id = %s
        ORDER BY id ASC
    """, (user_id,))
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(orders), 200


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Body JSON manquant"}), 400

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if user_id is None or product_id is None or quantity is None:
        return jsonify({"error": "user_id, product_id et quantity sont obligatoires"}), 400

    if quantity <= 0:
        return jsonify({"error": "quantity doit être > 0"}), 400

    # Vérifier le produit dans Products
    try:
        product_response = requests.get(f"{PRODUCTS_SERVICE_URL}/products/{product_id}", timeout=5)
    except requests.RequestException:
        return jsonify({"error": "Impossible de contacter products-service"}), 502

    if product_response.status_code != 200:
        return jsonify({"error": "Produit introuvable"}), 404

    product = product_response.json()
    stock = product.get("stock")
    price = product.get("price")

    if stock is None or price is None:
        return jsonify({"error": "Réponse produit invalide"}), 502

    if stock < quantity:
        return jsonify({"error": "Stock insuffisant"}), 400

    total_price = round(float(price) * int(quantity), 2)
    new_stock = stock - quantity

    # Décrémenter le stock dans Products
    try:
        update_response = requests.put(
            f"{PRODUCTS_SERVICE_URL}/products/{product_id}",
            json={"stock": new_stock},
            timeout=5
        )
    except requests.RequestException:
        return jsonify({"error": "Impossible de mettre à jour le stock"}), 502

    if update_response.status_code not in (200, 204):
        return jsonify({"error": "Échec mise à jour stock"}), 502

    # Créer la commande
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orders (user_id, product_id, quantity, total_price, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, user_id, product_id, quantity, total_price, status, created_at
    """, (user_id, product_id, quantity, total_price, "created"))
    new_order = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_order), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003) 