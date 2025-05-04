# 🏋️‍♂️ Weighsight
**A smart, calendar-integrated weight-tracking webapp** that connects to your Google Calendar to automatically extract weight data, visualize weekly trends, and generate actionable insights using data analysis and forecasting.

## 🚀 Features & Architecture

### 🔐 User Authentication & Account Linking
- Implements **OAuth 2.0** to securely connect and authorize access to the user's Google Calendar.
- Future support for **iCloud Calendar** via **CalDAV** with app-specific passwords.
- Authentication state determines app flow and calendar data access.

---

### 🎯 User Onboarding & Goal Initialization
- On first launch, prompts user to input a **target goal weight**.
- Stores the goal locally for use in progress tracking and predictive analysis.

---

### 📅 Calendar Data Extraction
- Queries events from the user’s calendar from **January 1, 2025 to present**.
- Filters for events titled **"Weigh In"**.
- Extracts and parses weight values from the event **notes** using regex (e.g., `"187.4 lbs"`).
- Formats valid data into structured tuples:  
  `[(date, weight)]`.

---

### 📊 Data Visualization
- Interactive **Week vs Weight** graph powered by **Plotly** or **Matplotlib**.
- Weeks based on **ISO calendar week** (`Jan 1 = Week 1`, `Jan 8 = Week 2`, etc.).
- Tooltips display exact dates and weight entries on hover.
- Skips points with missing or invalid weight data for clean plotting.

---

### 📈 Statistical Analysis Engine
- Calculates:
  - **Monthly weight change** (gain/loss).
  - **Average rate of change per week**.
- Applies **linear regression** to assess user trend and rate of progress.
- Highlights periods of stagnation, acceleration, or reversal.

---

### 🤖 Forecasting & Insight Generation
- Projects weight for the next **4 weeks** based on trendline.
- Evaluates proximity to **goal weight** and estimated time to reach it.
- Optional **GPT-based interpretation layer** that converts raw metrics into natural language suggestions:
  - Example: *“You’re on pace to hit your goal in 6 weeks. Stay consistent or reduce by 200 kcal/day to accelerate.”*

---

## 🛠️ Stack
- **Frontend/UI**: Streamlit (for rapid prototyping and interactivity)
- **Backend**: Python
- **Data**: Google Calendar API, CalDAV (iCloud)
- **Visualization**: Plotly, Matplotlib
- **Analysis**: NumPy, Pandas, scikit-learn
- **AI Integration**: OpenAI GPT API (optional)

---

## 📦 Roadmap
- [ ] Support for iCloud Calendar via CalDAV
- [ ] Persistent user sessions & login
- [ ] Exportable progress reports (PDF/CSV)
- [ ] Mobile-responsive layout
- [ ] OAuth scope refinement and deployment

---

## 📸 Screenshots (Coming Soon)

---

## 📬 Contact
Feel free to reach out if you'd like to collaborate or have feedback on the app!