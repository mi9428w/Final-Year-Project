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
    propensity_score = float(data.get("propensity_score", 0.5))

    candidate_products = []

    for item in basket:
        if item in basket_rules:
            candidate_products.extend(basket_rules[item])

    candidate_products = list(set(candidate_products))

    if len(candidate_products) == 0:
        recommendation = "No recommendation available"
        action = "No action"
        scored_products = []
    else:
        scored_products = []

        for product in candidate_products:
            score = propensity_score

            # Segment influence
            if segment == "High":
                score += 0.2
            elif segment == "Medium":
                score += 0.1

            # Product preference
            if "Premium" in product or "Watch" in product:
                score += 0.1

            # Combine ML propensity score with rule-based score
            score = propensity_score * 0.6 + score * 0.4

            # Add small random noise to break ties
            score += random.uniform(0, 0.05)

            scored_products.append((product, score))

        best_product = sorted(scored_products, key=lambda x: x[1], reverse=True)[0][0]

        if segment == "Low":
            recommendation = "Discount " + best_product
            action = "Offer discount to increase conversion"
        elif segment == "High":
            recommendation = best_product
            action = "Upsell premium product to increase basket value"
        else:
            recommendation = best_product
            action = "Recommend related product"

    return jsonify({
        "basket": basket,
        "segment": segment,
        "propensity_score": propensity_score,
        "candidate_products": candidate_products,
        "scored_products": scored_products,
        "recommended_product": recommendation,
        "business_action": action
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)