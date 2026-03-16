"""
Project 1 — Restaurant Billing System
Flask Backend
Run: python restaurant_app.py  →  http://localhost:5001
"""

from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

# ── Data: menu stored as a tuple ──────────────────────────────
MENU_ITEMS = ("Burger", "Pizza", "Sandwich", "Fries", "Drink")


def get_item_price(item: str) -> int | None:
    """Assign price with if/elif/else as per assignment requirements."""
    if item == "Burger":
        return 250
    elif item == "Pizza":
        return 500
    elif item == "Sandwich":
        return 200
    elif item == "Fries":
        return 150
    elif item == "Drink":
        return 100
    else:
        return None   # item not in menu


def apply_discount(total: float) -> tuple[float, float]:
    """
    Discount rules:
      total > 1000  → 10 %
      500 ≤ total ≤ 1000 → 5 %
      total < 500   → 0 %
    Returns (discount_amount, final_bill).
    """
    if total > 1000:
        discount = total * 0.10
    elif total >= 500:
        discount = total * 0.05
    else:
        discount = 0.0
    return round(discount, 2), round(total - discount, 2)


# ── API Routes ────────────────────────────────────────────────

@app.route("/api/order", methods=["POST"])
def order():
    data     = request.get_json()
    item     = data.get("item", "").strip().title()
    quantity = data.get("quantity", 0)

    # Validate against menu tuple
    if item not in MENU_ITEMS:
        return jsonify({"error": "Sorry! This item is not available in our restaurant."}), 400

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Please enter a valid quantity (positive integer)."}), 400

    price            = get_item_price(item)
    original_bill    = price * quantity
    discount, final  = apply_discount(original_bill)

    return jsonify({
        "item":          item,
        "quantity":      quantity,
        "unit_price":    price,
        "original_bill": original_bill,
        "discount":      discount,
        "final_bill":    final,
    })


@app.route("/api/menu", methods=["GET"])
def menu():
    return jsonify({"menu": list(MENU_ITEMS)})


@app.route("/")
def index():
    return send_from_directory(".", "restaurant.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
