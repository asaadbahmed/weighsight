import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

st.title("Weighsight")
# populate this via Google Calendar
dates = [
    "2025-01-01", "2025-01-08", "2025-01-15", "2025-01-22",
    "2025-01-29", "2025-02-05", "2025-02-12", "2025-02-19",
    "2025-02-26", "2025-03-05", "2025-03-12", "2025-03-19",
    "2025-03-26", "2025-04-02", "2025-04-09", "2025-04-16",
    "2025-04-23", "2025-04-30", "2025-05-07"
]
# populate this via Google Calendar
weights = [
    "120 lbs", "125 lbs", "120 lbs", "135 lbs",
    "130 lbs", "128 lbs", "126 lbs", "129 lbs",
    "127 lbs", "124 lbs", "123 lbs", "122 lbs",
    "125 lbs", "121 lbs", "120 lbs", "119 lbs",
    "118 lbs", "117 lbs", "116 lbs"
]

data = pd.DataFrame({
    "date": dates,
    "weight": weights,
    "week": [f"Week {i+1}" for i in range(len(dates))]
})

trace = go.Scatter(
    x=data["week"],
    y=data["weight"],
    mode="lines+markers",
    line=dict(color="#00ff00", width=3, shape="spline"),
    marker=dict(color="#00ff00", size=6),
    fill="tozeroy",
    fillcolor="rgba(30, 215, 96, 0.15)",
    hovertemplate="<b>Date:</b> %{customdata|%b %d, %Y}<br><b>Weight:</b> %{y}<extra></extra>",
    customdata=data["date"]
)

fig = go.Figure(data=[trace])
fig.update_layout(
    template="plotly_white",
    plot_bgcolor="#191414",
    paper_bgcolor="#121212",
    title="2025 Weight Graph",
    title_font_size=24,
    font=dict(family="Helvetica", size=14, color="white"),
    xaxis_title="<b>Date</b>",
    yaxis_title="<b>Weight (lbs)</b>",
    xaxis=dict(showspikes=False, color="white", showgrid=False),
    yaxis=dict(showspikes=False, gridcolor="#333", color="white", showgrid=False),
    hovermode="x unified",
    margin=dict(t=60, b=40, l=60, r=40)
)

# st.button("Connect your Google account", on_click=st.login)
# st.button("Logout", on_click=st.logout)
# st.write(st.user)
st.plotly_chart(fig, use_container_width=True)
# st.write(data)