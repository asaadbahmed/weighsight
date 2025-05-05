import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.title("Weighsight")
# populate this via Google Calendar
formatted_dates = [
    "2025-01-01", "2025-01-08", "2025-01-15", "2025-01-22",
    "2025-01-29", "2025-02-05", "2025-02-12", "2025-02-19",
    "2025-02-26", "2025-03-05", "2025-03-12", "2025-03-19",
    "2025-03-26", "2025-04-02", "2025-04-09", "2025-04-16",
    "2025-04-23", "2025-04-30", "2025-05-07", "2025-05-14"
]
# populate this via Google Calendar
formatted_weights = [
    "120 lbs", "125 lbs", "120 lbs", "135 lbs",
    "130 lbs", "128 lbs", "126 lbs", "129 lbs",
    "127 lbs", "124 lbs", "123 lbs", "122 lbs",
    "125 lbs", "121 lbs", "120 lbs", "119 lbs",
    "118 lbs", "117 lbs", "116 lbs", "120 lbs"
]
weights = [float(w.replace("lbs", "").replace("kg", "").strip()) for w in formatted_weights]
date_weight_pairs = list(zip(formatted_dates, weights)) # [week0=(date, weight), week1=(date, weight), ..., weekn=(date, weight)]
weight_by_month = [date_weight_pairs[i:i+4] for i in range(0, len(date_weight_pairs), 4)] # [month0=[week0=(date, weight), week1=(date, weight), ..., week4(date, weight)]
weight_by_month

data = pd.DataFrame({
    "date": formatted_dates,
    "weight": weights,
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
    xaxis_title="<b>Week</b>",
    yaxis_title="<b>Weight (lbs)</b>",
    xaxis=dict(showspikes=False, color="white", showgrid=False),
    yaxis=dict(showspikes=False, gridcolor="#333", color="white", showgrid=False, autorange=True),
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

for i, weight in enumerate(weights):
    if weight < min_weight:
        min_weight = weight
        min_date = formatted_dates[i]
        min_week = i

    if weight > max_weight:
        max_weight = weight
        max_date = formatted_dates[i]
        max_week = i

# calculate each month's weight delta
month_weight_deltas = [] # [month0=[week0=(date, weight), week1=(date, weight), ..., week4(date, weight)]
for month in weight_by_month:
    delta = month[3][1] - month[0][1]
    month_weight_deltas.append(delta)

# month with most weight gain
month_most_gain = (month_weight_deltas.index(max(month_weight_deltas)), max(month_weight_deltas))

# month with least weight gain
month_least_gain = tuple()
current_least_gain = 1000
for i, delta in enumerate(month_weight_deltas):
    if delta < 0:
        continue
    
    if delta == 0:
        month_least_gain = (i, delta)
        break

    if delta < current_least_gain:
        month_least_gain = (i, delta)
        current_least_gain = delta

# month with most weight loss
month_most_loss = (month_weight_deltas.index(min(month_weight_deltas)), min(month_weight_deltas))

# month with least weight loss
month_least_loss = tuple()
current_least_loss = -1000
for i, delta in enumerate(month_weight_deltas):
    if delta > 0:
        continue

    if delta > current_least_loss:
        month_least_loss = (i, delta)
        current_least_loss = delta

# average monthly weight rate
avg_monthly_rate = sum(month_weight_deltas) / len(month_weight_deltas)

# feed this data into CGPT with a prompt to get concise insights and place in insights section
st.header("Analysis 🔍")
analysis_message = f"You weighed a **maximum** of {max_weight} lbs (week {max_week + 1}) and a **minimum** of {min_weight} lbs (week {min_week + 1})."
analysis_message += f"\n\nYou **gained** the **most weight** in month {month_most_gain[0] + 1} of your journey ({month_most_gain[1]} lbs)."
analysis_message += f"\n\nYou **gained** the **least weight** in month {month_least_gain[0] + 1} of your journey ({month_least_gain[1]} lbs)."
analysis_message += f"\n\nYou **lost** the **most weight** in month {month_most_loss[0] + 1} of your journey ({abs(month_most_loss[1])} lbs)."
analysis_message += f"\n\nYou **lost** the **least weight** in month {month_least_loss[0] + 1} of your journey ({abs(month_least_loss[1])} lbs)."
for i, delta in enumerate(month_weight_deltas):
    if delta > 0:
        analysis_message += f"\n\nYou **gained** {delta} lbs in month {i + 1} of your journey."
    else:
        analysis_message += f"\n\nYou **lost** {abs(delta)} lbs in month {i + 1} of your journey."
if avg_monthly_rate > 0:
    analysis_message += f"\n\nOn **average**, you **gain** {avg_monthly_rate} lbs per month."
else:
    analysis_message += f"\n\nOn **average**, you **lose** {abs(avg_monthly_rate)} lbs per month."

st.markdown(analysis_message)

st.header("Insights 📝")