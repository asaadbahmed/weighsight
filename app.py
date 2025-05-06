import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import re
import os
import json
from openai import OpenAI

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def auth():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=["https://www.googleapis.com/auth/calendar.events.readonly"])
    service = build("calendar", "v3", credentials=creds)
    return service

def get_events(service):
    try:
        events_result = service.events().list(
            calendarId="asaadbinahmed@gmail.com", 
            timeMin="2025-01-01T00:00:00Z",
            maxResults=52, 
            singleEvents=True,
            orderBy="startTime",
            q="Weigh In"
            ).execute()
    except HttpError as error:
        print(f'An error occurred: {error}')

    return events_result.get('items', [])

client = OpenAI(api_key=st.secrets["openai"]["OPENAI_API_KEY"])
events = get_events(auth())
formatted_dates = []
formatted_weights = []

for e in events:
    weight = e.get('description')
    date = e.get('start')

    if not weight or not date:
        continue

    date = date.get('date')
    if not date:
        continue

    result = re.match(r'^\d+(\.\d+)?\s*lbs$', weight)
    if not result:
        continue

    weight = result.group(0)


    formatted_weights.append(weight)
    formatted_dates.append(date)

weights = [float(w.replace("lbs", "").replace("kg", "").strip()) for w in formatted_weights]
date_weight_pairs = list(zip(formatted_dates, weights)) # [week0=(date, weight), week1=(date, weight), ..., weekn=(date, weight)]
weight_by_month = [date_weight_pairs[i:i+4] for i in range(0, len(date_weight_pairs), 4)] # [month0=[week0=(date, weight), week1=(date, weight), ..., week4(date, weight)]

data = pd.DataFrame({
    "date": formatted_dates,
    "weight": weights,
    "week": [f"Week {i+1}" for i in range(len(formatted_dates))]
})

trace = go.Scatter(
    x=data["week"],
    y=data["weight"],
    mode="lines+markers",
    marker=dict(size=6, color="#00ff00"),
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
    xaxis=dict(showspikes=False, color="white", showgrid=False, fixedrange=True),
    yaxis=dict(showspikes=False, gridcolor="#333", color="white", showgrid=False, autorange=True, fixedrange=True),
    hovermode="x unified",
    margin=dict(t=60, b=40, l=60, r=40),
)

st.title("Weighsight")
st.plotly_chart(fig, use_container_width=True, config={
    "scrollZoom": False,
    "displayModeBar": False
})
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
    delta = month[len(month) - 1][1] - month[0][1]
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
analysis_message = f"You weighed a **maximum** of {round(max_weight, 2)} lbs (week {max_week + 1}) and a **minimum** of {round(min_weight, 2)} lbs (week {min_week + 1})."
analysis_message += f"\n\nYou **gained** the **most weight** in month {month_most_gain[0] + 1} of your journey ({round(month_most_gain[1], 2)} lbs)."
analysis_message += f"\n\nYou **gained** the **least weight** in month {month_least_gain[0] + 1} of your journey ({round(month_least_gain[1], 2)} lbs)."
analysis_message += f"\n\nYou **lost** the **most weight** in month {month_most_loss[0] + 1} of your journey ({round(abs(month_most_loss[1]), 2)} lbs)."
analysis_message += f"\n\nYou **lost** the **least weight** in month {month_least_loss[0] + 1} of your journey ({round(abs(month_least_loss[1]), 2)} lbs)."

for i, delta in enumerate(month_weight_deltas):
    if delta > 0:
        analysis_message += f"\n\nYou **gained** {round(delta, 2)} lbs in month {i + 1} of your journey."
    else:
        analysis_message += f"\n\nYou **lost** {round(abs(delta), 2)} lbs in month {i + 1} of your journey."
if avg_monthly_rate > 0:
    analysis_message += f"\n\nOn **average**, you **gain** {round(avg_monthly_rate, 2)} lbs per month."
else:
    analysis_message += f"\n\nOn **average**, you **lose** {round(abs(avg_monthly_rate), 2)} lbs per month."

st.header("Insights 📝")
INSIGHT_FILE = "insights_data.json"
def load_cached_insight():
    if os.path.exists(INSIGHT_FILE):
        with open(INSIGHT_FILE, "r") as f:
            return json.load(f)
    return {"week": -1, "insight": ""}

def save_insight(week_index, insight_text):
    with open(INSIGHT_FILE, "w") as f:
        json.dump({"week": week_index, "insight": insight_text}, f)

def gen_insight():
    response = client.chat.completions.create(model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a personal weight-tracking coach. You provide short, motivational, and insightful feedback, pointing out meaningful patterns, plateaus, and progress trends."},
        {"role": "user", "content": f"Here's the user's weight journey so far. Goal: 140 lbs. Height: 6'2 male. Analysis: {analysis_message}. Weekly Weights: {date_weight_pairs}. Please provide a specific, motivational insight. Mention positive habits if progress is good, or possible adjustments if growth has slowed. Be concise but thoughtful."}
    ],
    temperature=0.7)
    return response.choices[0].message.content

cached = load_cached_insight()
current_week_index = len(weights)

if current_week_index > cached["week"]:
    with st.spinner("Thinking..."):
      gpt_output = gen_insight()
    save_insight(current_week_index, gpt_output)
    st.markdown(gpt_output)
else:
    st.markdown(cached["insight"])
st.markdown(f"**Progress: {round(weights[len(weights) - 1], 1)} / 140 lbs**")

st.header("Analysis 🔍")
st.markdown(analysis_message)