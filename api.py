from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Recommendation rules based on basket items
basket_rules = {
    "Shoes": ["Socks", "Shoe Cleaner", "Bag"],
    "Watch": ["Bracelet", "Premium Wallet", "Sunglasses"],
    "Bag": ["Wallet", "Sunglasses"],
    "T-shirt": ["Cap", "Jeans"],
    "Headphones": ["Bluetooth Speaker", "Laptop Bag"],
    "Sunglasses": ["Cap", "Watch"],
    "Laptop Bag": ["Mouse", "Headphones"],
    "Wallet": ["Belt", "Watch"]
}

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json

    basket = data.get("basket", [])
    segment = data.get("segment", "Medium")

    candidate_products = []

    for item in basket:
        if item in basket_rules:
            candidate_products.extend(basket_rules[item])

    candidate_products = list(set(candidate_products))

    if len(candidate_products) == 0:
        recommendation = "No recommendation available"
        action = "No action"
    else:
        if segment == "High":
            recommendation = random.choice(candidate_products)
            action = "Upsell premium product to increase basket value"
        elif segment == "Medium":
            recommendation = random.choice(candidate_products)
            action = "Recommend related product"
        else:
            recommendation = "Discount " + random.choice(candidate_products)
            action = "Offer discount to increase conversion"

    return jsonify({
        "basket": basket,
        "segment": segment,
        "candidate_products": candidate_products,
        "recommended_product": recommendation,
        "business_action": action
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)