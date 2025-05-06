from classes.observer import Observer
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

class Graph(Observer):
    def __init__(self, container):
        super().__init__()
        self._container = container

    def update(self, state):
        self._state = state
        self.render()

    def render(self):
        state = self._state
        entries = [(entry['date'], entry['weight']) for entry in state['entries']]
        dataframe = pd.DataFrame(entries, columns=['date', 'weight'])
        x_labels = [i for i in range(1, len(dataframe) + 1)]
        y_values = [w for w in dataframe['weight']]
        
        trace = go.Scatter(
            x=x_labels,
            y=y_values,
            mode="lines+markers",
            line=dict(color="white", width=3, shape="spline"),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor="rgba(255, 255, 255, 0.1)",
            hovertemplate="<b>Date:</b> %{customdata|%b %d, %Y}<br><b>Weight:</b> %{y}<extra></extra>",
            customdata=dataframe["date"]
        )        
        figure = go.Figure(data=[trace])
        figure.update_layout(
            template="plotly_white",
            plot_bgcolor="#191414",
            paper_bgcolor="#121212",
            title=dict(
                text="2025 Weight Graph",
                x=0.5,
                xanchor='center',
                font=dict(size=24)
            ),
            font=dict(family="Helvetica", size=14, color="white"),
            xaxis_title="<b>Week</b>",
            yaxis_title=f"<b>Weight ({state['scale']})</b>",
            xaxis=dict(
                tickmode="linear",
                tick0=1,
                dtick=1,
                showspikes=False,
                color="white",
                showgrid=False
            ),
            yaxis=dict(showspikes=False, gridcolor="#333", color="white", showgrid=False),
            hovermode="x unified"
        )
        
        with st.empty():
            st.plotly_chart(figure, use_container_width=True)
            st.table(dataframe)
