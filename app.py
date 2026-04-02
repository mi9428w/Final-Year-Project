import streamlit as st
import random
import pandas as pd
import requests

st.set_page_config(page_title="Customer Recommendation Simulation")

st.title("Customer Basket Recommendation Simulation")

st.write("This simulation shows how customer data can be used to recommend additional products and increase sales.")

# Loading real customer dataset
customer_data = pd.read_csv("customer_data.csv")

#Selecting random customer from dataset
sample_customer = customer_data.sample(1)

customer_id = sample_customer["customer_unique_id"].values[0]
propensity_score = sample_customer["propensity_score"].values[0]
segment = sample_customer["propensity_segment"].values[0]

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

    response = requests.post(
        "http://127.0.0.1:5000/recommend",
        json={
            "basket": basket,
            "segment": segment
        }
    )

    result = response.json()

    st.subheader("Recommendation Result")

    st.markdown(f"*Basket Items:* {', '.join(result['basket'])}")
    st.markdown(f"*Candidate Products:* {', '.join(result['candidate_products'])}")
    st.markdown(f"*Final Recommended Product:* {result['recommended_product']}")
    st.markdown(f"*Business Action:* {result['business_action']}")