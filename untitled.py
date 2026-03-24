import streamlit as st
import random

st.set_page_config(page_title="Customer Recommendation Simulation")

st.title("Customer Basket Recommendation Simulation")

st.write("This simulation shows how customer data can be used to recommend additional products and increase sales.")

# Fake customer info (based on your dataset result)
customer_id = "16a23480d3c92eb40e134844d52aa63e"
propensity_score = 0.86889
segment = "High"

# Product list
products = [
    "Shoes", "Bag", "Watch", "T-shirt",
    "Headphones", "Sunglasses", "Laptop Bag", "Wallet"
]

# Basket rules (cross-sell logic)
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

# Show customer info
st.subheader("Customer Information")
st.write("Customer ID:", customer_id)
st.write("Propensity Score:", propensity_score)
st.write("Customer Segment:", segment)

# Basket selection
st.subheader("Select Basket Items")
basket = st.multiselect("Choose products:", products, default=["Shoes", "Watch"])

# Button
if st.button("Generate Recommendation"):

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

    st.subheader("Recommendation Result")
    st.write("Basket:", basket)
    st.write("Candidate Products:", candidate_products)
    st.write("Recommended Product:", recommendation)
    st.write("Business Action:", action)