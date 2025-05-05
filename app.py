import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Weighsight")
# populate this via Google Calendar
formatted_dates = [
    "2025-01-01", "2025-01-08", "2025-01-15", "2025-01-22",
    "2025-01-29", "2025-02-05", "2025-02-12", "2025-02-19",
    "2025-02-26", "2025-03-05", "2025-03-12", "2025-03-19",
    "2025-03-26", "2025-04-02", "2025-04-09", "2025-04-16",
    "2025-04-23", "2025-04-30", "2025-05-07"
]
# populate this via Google Calendar
formatted_weights = [
    "120 lbs", "125 lbs", "120 lbs", "135 lbs",
    "130 lbs", "128 lbs", "126 lbs", "129 lbs",
    "127 lbs", "124 lbs", "123 lbs", "122 lbs",
    "125 lbs", "121 lbs", "120 lbs", "119 lbs",
    "118 lbs", "117 lbs", "116 lbs"
]

data = pd.DataFrame({
    "date": formatted_dates,
    "weight": formatted_weights,
    "week": [f"Week {i+1}" for i in range(len(formatted_dates))]
})

trace = go.Scatter(
    x=data["week"],
    y=data["weight"],
    mode="lines",
    line=dict(color="#00ff00", width=3, shape="spline"),    
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

# find min & max weights along with the date
min_weight, max_weight = 1000, -1
min_date, max_date = "", ""
min_week, max_week = -1, -1

for index, weight in enumerate(formatted_weights):
    weight = float(weight.replace("lbs", "").replace("kg", "").strip())        
    
    if weight < min_weight:
        min_weight = weight
        min_date = formatted_dates[index]
        min_week = index

    if weight > max_weight:
        max_weight = weight
        max_date = formatted_dates[index]
        max_week = index

st.write(f"Overall, you weighed at most {max_weight} lbs (week {max_week + 1}) and at minimum {min_weight} lbs (week {min_week + 1}).")

# month with most weight gain

# month with least weight gain

# month with most weight loss

# month with least weight loss

# overall average weight gain rate

# overall average weight loss rate 

# month-by-month average weight gain rate 

# month-by-month average weight loss rate 

# feed this data into CGPT with a propmpt to get concise analysis