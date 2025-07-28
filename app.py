import streamlit as st
import numpy as np
import pandas as pd

# ------------------- Page Setup -------------------
st.set_page_config(page_title="Pricing Scenario Simulator", layout="centered")
st.title("📊 Pricing Scenario Simulator with Elasticity")
st.markdown("""
This app simulates how changes in price and demand elasticity affect revenue.

**Formula Used:**

- New Price = Current Price × (1 + % Price Change)
- Quantity Change % = Elasticity × % Price Change
- New Quantity = Current Quantity × (1 + Quantity Change %)
- New Revenue = New Price × New Quantity
""")

# ------------------- Sidebar Inputs -------------------
st.sidebar.header("🔧 Input Parameters")

current_sales = st.sidebar.number_input("Current Sales ($)", value=183000.0, step=1000.0)
current_units = st.sidebar.number_input("Current Units Sold", value=8451, step=1)
elasticity = st.sidebar.number_input("Price Elasticity of Demand", value=-1.3, step=0.1)

price_change_range = st.sidebar.slider("Select Price Change Range (%)", -30, 30, (-10, 10), step=1)

# ------------------- Calculations -------------------
current_price = current_sales / current_units
scenarios = []

for pct in range(price_change_range[0], price_change_range[1] + 1):
    price_change = pct / 100
    new_price = current_price * (1 + price_change)
    quantity_change_pct = elasticity * price_change
    new_quantity = current_units * (1 + quantity_change_pct)
    new_revenue = new_price * new_quantity
    revenue_diff = new_revenue - current_sales

    scenarios.append({
        "Price Change (%)": pct,
        "New Price ($)": round(new_price, 2),
        "New Quantity": int(round(new_quantity)),
        "New Revenue ($)": round(new_revenue, 2),
        "Revenue Change ($)": round(revenue_diff, 2)
    })

df = pd.DataFrame(scenarios)

# ------------------- Results Table -------------------
st.subheader("📈 Simulation Results Table")
st.dataframe(df, use_container_width=True)

# ------------------- Charts -------------------
st.subheader("📊 Revenue vs Price Change (%)")
st.line_chart(df.set_index("Price Change (%)")[["New Revenue ($)", "Revenue Change ($)"]])

# ------------------- Optional Download -------------------
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name='pricing_simulation.csv',
    mime='text/csv'
)
