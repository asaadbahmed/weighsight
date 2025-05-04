import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Weighsight")
dates = ["2025-01-01", "2025-01-08", "2025-01-15", "2025-01-22"] # populate this via Google Calendar
weights = ["120 lbs", "125 lbs", "120 lbs", "135 lbs"] # populate this via Google Calendar
data = pd.DataFrame({
    "date": pd.to_datetime(dates),
    "weight": weights,
    "week": [f"Week {i+1}" for i in range(len(dates))]
})

fig = px.line(
    data,
    x="week",
    y="weight",
    title="2025 Weight Graph",
    markers=True,
    line_shape="spline"
)

fig.update_traces(line=dict(color="#00ff00", width=3), marker=dict(color="#00ff00", size=5), 
    hovertemplate="<b>Date:</b> %{customdata|%b %d, %Y}<br><b>Weight:</b> %{y}<extra></extra>",
    customdata=data["date"])
fig.update_layout(
    template="plotly_white",
    title_font_size=22,
    xaxis_title="Week",
    yaxis_title="Weight (lbs)",
    font=dict(family="Helvetica", size=14),
    hovermode="x unified"
)

st.button("Connect your Google account", on_click=st.login)
st.button("Logout", on_click=st.logout)
st.plotly_chart(fig, use_container_width=True)
st.write(data)