import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Drata Product Health Dashboard", layout="wide")
    
# -----------------------------
# Mock Data Generation Section
# -----------------------------
today = datetime.today()
dates = pd.date_range(end=today, periods=30)

# Sample 10 products from Leen
products = [
    "CrowdStrike", "Snyk", "Okta", "JumpCloud", "Tenable", 
    "Qualys", "GitHub", "Google Workspace", "Duo Security", "AWS GuardDuty"
]

# Security categories mapping
security_categories = {
    "CrowdStrike": "EDR",
    "Snyk": "VMS",
    "Okta": "IDP",
    "JumpCloud": "IDP",
    "Tenable": "VMS",
    "Qualys": "VMS",
    "GitHub": "DevOps",
    "Google Workspace": "Collaboration",
    "Duo Security": "IDP",
    "AWS GuardDuty": "EDR"
}

# Generate daily API calls by product
data = []
for date in dates:
    for product in products:
        calls = max(0, int(100 + 50 * (hash(product + str(date)) % 6)))
        errors = int(calls * 0.05 * (hash(product) % 4))
        time_to_sync = int(5 + hash(product + str(date)) % 30)  # in minutes
        data.append({
            "date": date,
            "product": product,
            "calls": calls,
            "errors": errors,
            "time_to_sync": time_to_sync,
            "category": security_categories[product]
        })

df = pd.DataFrame(data)

# -----------------------------
# Streamlit UI Section
# -----------------------------
st.set_page_config(page_title="Drata Product Health Dashboard", layout="wide")
st.title("📊 Drata Product Health Dashboard")

# Date filter
date_range = st.date_input("Select date range:", [dates.min(), dates.max()])
if len(date_range) == 2:
    df = df[(df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))]

# 1. Daily Calls Breakdown by Product
st.subheader("1️⃣ Daily API Calls by Product")
daily_calls = df.groupby(["date", "product"])["calls"].sum().reset_index()
fig_calls = px.bar(daily_calls, x="date", y="calls", color="product", title="API Call Volume per Product")
st.plotly_chart(fig_calls, use_container_width=True)

# 2. Top Erroring Product
st.subheader("2️⃣ Top Errors by Product")
top_errors = df.groupby("product")["errors"].sum().reset_index().sort_values(by="errors", ascending=False)
fig_errors = px.bar(top_errors, x="product", y="errors", title="Total Errors per Product", color="product")
st.plotly_chart(fig_errors, use_container_width=True)

# 3. Avg Time to First Sync
st.subheader("3️⃣ Average Time to First Sync (mins)")
time_to_sync = df.groupby("product")["time_to_sync"].mean().reset_index().sort_values(by="time_to_sync")
fig_sync = px.bar(time_to_sync, x="product", y="time_to_sync", title="Avg Time to First Sync by Product", color="product")
st.plotly_chart(fig_sync, use_container_width=True)

# 4. Usage by Security Category
st.subheader("4️⃣ Usage by Security Category")
category_usage = df.groupby(["date", "category"])["calls"].sum().reset_index()
fig_category = px.area(category_usage, x="date", y="calls", color="category", title="Daily Usage by Security Category")
st.plotly_chart(fig_category, use_container_width=True)

st.markdown("---")
st.caption("Dashboard built for Drata using Leen's Unified API usage insights.")
