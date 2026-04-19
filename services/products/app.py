from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Clavier", "price": 49.99, "stock": 10},
    {"id": 2, "name": "Souris", "price": 19.99, "stock": 25}
]

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    for product in products:
        if product["id"] == id:
            return jsonify(product)
    return jsonify({"error": "Produit non trouvé"}), 404

@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"],
        "stock": data["stock"]
    }

    products.append(new_product)
    return jsonify(new_product), 201

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    for product in products:
        if product["id"] == id:
            data = request.get_json()
            product["name"] = data.get("name", product["name"])
            product["price"] = data.get("price", product["price"])
            product["stock"] = data.get("stock", product["stock"])
            return jsonify(product)
    return jsonify({"error": "Produit non trouvé"}), 404

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    for product in products:
        if product["id"] == id:
            products.remove(product)
            return jsonify({"message": "Produit supprimé"})
    return jsonify({"error": "Produit non trouvé"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)