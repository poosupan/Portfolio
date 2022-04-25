import streamlit as st
#import sqlite3
#from google.cloud import storage
import pandas as pd
#import numpy as np
#from datetime import datetime

#import sys
import plotly.graph_objects as go
import plotly.express as px
import sqlalchemy

st.set_page_config(layout="wide", page_icon="💬", page_title="Portfolio testing")

st.subheader("Hello i'm POS")
st.title("I love Gam very much")
st.write("I always love her forever and forever")

DB_SQL = st.secrets["db_sql"]

@st.cache(suppress_st_warning=True)
def load_data():
    engine = sqlalchemy.create_engine(DB_SQL)
    df = pd.read_sql('SELECT * FROM port_allocate_test2', engine, index_col=['Time'])
    numeric_df = df.select_dtypes(['float','int'])
    numeric_cols = numeric_df.columns

    text_df = df.select_dtypes(['object'])
    text_cols = text_df.columns
    return relative(df), numeric_cols, text_cols

def relative(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)*100
    return cumret

df, numeric_cols, text_cols = load_data()

checkbox = st.sidebar.checkbox(label = 'Compare with BTC')
feature_selection = ['Balance']
if checkbox:
    #st.write(df)
    feature_selection = ['Balance', 'BTC_price']

#feature_selection = #st.sidebar.multiselect(label = 'Features to polt', options = numeric_cols, default = 'Balance')
df_feature = df[feature_selection]
plotly_figure = px.line(df_feature, x = df_feature.index, y = feature_selection, title = 'Pecentage change')
plotly_figure.update_layout(showlegend=False)
st.plotly_chart(plotly_figure, use_container_width=True)