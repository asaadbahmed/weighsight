import streamlit as st
import pandas as pd
import datetime
import random
from classes.graph import Graph
from classes.weight_state import WeightState

sample_size = 5 # number of weeks
sample_dates = [(datetime.datetime(2025, 1, 1) + datetime.timedelta(weeks=i)).strftime('%Y-%m-%d') for i in range(sample_size)]
sample_weights = [round(random.uniform(120.0, 220.0), 1) for _ in range(len(sample_dates))]
sample_entries = [{'date': date, 'weight': weight} for date, weight in zip(sample_dates, sample_weights)]

graph_container = st.empty()
graph = Graph(graph_container)
weight_state = WeightState({
    'entries': sample_entries,
    'scale': 'lbs'
})

weight_state.subscribe(graph)
weight_state.notify()

sample_state = weight_state.get_state()
sample_state['entries'].append({'date': '02-05-2025', 'weight': 0.0})
weight_state.set_state(sample_state)