import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Mock Funnel Data Generation
# -----------------------------
stages = [
    "Website Visit",
    "Demo Call",
    "Integration Connected",
    "Usage - Month 1",
    "Usage - Month 6"
]

# Simulated drop-off data
funnel_data = pd.DataFrame({
    "stage": stages,
    "users": [1000, 600, 400, 250, 120]
})

# -----------------------------
# Streamlit UI Section
# -----------------------------

st.title("📈 Customer Insights Dashboard")

# Funnel Chart Section
st.subheader("🔄 Customer Journey Funnel (Vertical)")
fig_funnel = px.funnel(funnel_data, y="users", x="stage",
                       title="Customer Journey from Website Visit to Month 6 Usage", orientation="h")
fig_funnel.update_layout(yaxis=dict(categoryorder='total ascending'))
st.plotly_chart(fig_funnel, use_container_width=True)

# Breakdown Table
st.subheader("📊 Stage-by-Stage Breakdown")
st.dataframe(funnel_data.set_index("stage"))

st.markdown("---")
st.caption("Funnel visualization to understand drop-off and engagement through the customer journey.")