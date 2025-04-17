import streamlit as st

st.set_page_config(page_title="Leen Dashboards", layout="wide")

# Title for the app 
st.title("Leen Dashboards")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a Dashboard", ("API Usage", "Integration Health", "Customer Insights"))

# Display the selected page
if page == "API Usage":
    import api_usage
elif page == "Integration Health":
    import integration_health
elif page == "Customer Insights":
    import customer_insights
