import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="API Usage Dashboard", layout="wide")

st.title("📊 API Usage Dashboard")


PRODUCTS = [
    'Snyk', 'CrowdStrike', 'GitHub', 'GitLab', 'Bitbucket',
    'Jira', 'ServiceNow', 'AWS Security Hub', 'Azure DevOps', 'Okta'
]


@st.cache_data
def generate_data():
    dates = pd.date_range(end=datetime.today(), periods=30)
    data = []
    for date in dates:
        for product in PRODUCTS:
            data.append({
                'date': date,
                'product': product,
                'calls': np.random.randint(500, 3000),
                'errors': np.random.randint(0, 200),
                'latency': np.random.normal(250, 50),
                'retries': np.random.randint(0, 100),
                'rate_limited': np.random.randint(0, 20),
            })
    return pd.DataFrame(data)

df = generate_data()


st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=7))
end_date = st.sidebar.date_input("End Date", datetime.today())
selected_products = st.sidebar.multiselect("Select Products", PRODUCTS, default=PRODUCTS)

filtered_df = df[
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['product'].isin(selected_products))
]


st.subheader("📈 Volume of API Calls Over Time")
volume_chart = filtered_df.groupby('date')['calls'].sum()
st.line_chart(volume_chart)

st.subheader("📊 Volume of API Calls by Product")
product_volume = filtered_df.pivot_table(index='date', columns='product', values='calls', aggfunc='sum')
st.bar_chart(product_volume)

st.subheader("🚨 Error Volume by Product")
error_volume = filtered_df.pivot_table(index='date', columns='product', values='errors', aggfunc='sum')
st.bar_chart(error_volume)

st.subheader("📡 Average Latency by Day (ms)")
latency_chart = filtered_df.groupby('date')['latency'].mean()
st.line_chart(latency_chart)

st.subheader("🔁 Retry Rate by Day")
retry_chart = filtered_df.groupby('date')['retries'].mean()
st.line_chart(retry_chart)

st.subheader("⛔ Rate Limiting Events")
rate_limited_chart = filtered_df.groupby('date')['rate_limited'].sum()
st.line_chart(rate_limited_chart)
