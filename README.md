# 🏋️‍♂️ Weighsight

**Weighsight** is a personal, intelligent weight-tracking dashboard that integrates with Google Calendar to analyze your weigh-in events, visualize trends, and generate tailored insights powered by GPT.

---

## 🔧 What It Does

### 📅 Calendar-Integrated Weight Tracking

- Automatically pulls events titled **"Weigh In"** from your Google Calendar.
- Extracts weight entries from the event description (e.g., `"187.4 lbs"`).
- Filters and cleans data for consistency.

### 📊 Weekly Trend Visualization

- Displays an interactive **Week vs Weight** line chart using **Plotly**.
- Hover over data points to reveal exact dates and weights.
- Color-coded, smooth visual with fill for clarity of progress.

### 📈 Monthly Progress Analytics

- Aggregates weigh-ins into monthly chunks (4-week blocks).
- Calculates:
  - Weight gained or lost each month.
  - Periods of highest gain/loss.
  - Average monthly rate of change.
- Highlights milestones such as **min/max weight** and their corresponding weeks.

### 🧠 AI-Driven Insight Generation

- Leverages **GPT-4.1-mini** to provide short, motivational insights based on your progress.
- Observes patterns and suggests either reinforcement or adjustment.
- Caches insights to avoid repeat computation and speed up loading.

---

## 📦 Tech Stack

- **UI Framework**: [Streamlit](https://streamlit.io/)
- **Visualization**: [Plotly](https://plotly.com/)
- **Data Analysis**: `pandas`, `numpy`, `re`
- **Calendar Integration**: Google Calendar API (via `google-api-python-client`)
- **AI Insight**: OpenAI GPT (via `openai` Python SDK)
- **Credential Handling**: Service Account authentication via `google.oauth2`

---

## 🧪 How It Works (Under the Hood)

1. **Authenticate Calendar Access**

   - Uses a **service account** to fetch events with title matching `"Weigh In"`.

2. **Extract & Format Data**

   - Validates weights using regex (`\d+(\.\d+)?\s*lbs`).
   - Associates each weight with a calendar week and aggregates by month.

3. **Plot Data**

   - Plots weekly data using smooth splines and styled tooltips.

4. **Run Analysis**

   - Finds:
     - Heaviest & lightest weeks
     - Monthly changes (gains/losses)
     - Average trends

5. **Generate GPT Insight**
   - Sends a structured message to OpenAI with your full data + analysis.
   - Displays a motivational, insightful message that updates with each new weigh-in.

---

## 🧠 Example Insight

> "You've consistently lost weight over the last 2 months—great job! If you keep this pace, you’re on track to hit your 140 lbs goal. Keep your weigh-in habit regular—it’s clearly working."

---

## 🚀 Running the App

To run locally:

```bash
pip install streamlit openai google-api-python-client google-auth pandas plotly
streamlit run app.py
```

You’ll need a secrets.toml (.streamlit/secrets.toml) with:

```toml
[gcp_service_account]
# Your Google Cloud service account credentials here

[openai]
OPENAI_API_KEY = "your-openai-key"
```

⸻

🎯 Goal & Progress Tracking

- Target weight is hardcoded to 140 lbs, but you can easily tweak this value as needed.
- Progress updates dynamically each week, as long as you are consistent with loggin.
- Visual and textual feedback reinforce momentum and help adjust when needed.

⸻

📁 Files Used

- app.py – Main Streamlit script
- insights_data.json – Cache for last generated GPT insight (necessary to prevent waste of precious tokens)

⸻

📝 Notes

This is a private, personal-use web app designed for a single user, with no login, account management, or multi-user support. However, it is easily configurable and plug-and-play if you would like to use it.
