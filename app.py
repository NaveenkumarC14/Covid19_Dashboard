# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 08:20:50 2020

@author: Sathishkumar
"""





import streamlit as st
import pandas as pd
import numpy as np 
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


st.title('Covid-19 India Cases')
st.write("It shows ***Coronavirus Cases*** in India")
st.sidebar.title("Selector")
image = Image.open("C:\\Users\\Sathishkumar\\Desktop\\New folder\\Coronavirus.jpg")
st.image(image,use_column_width=True)
st.markdown('<style>body{background-color: lightblue;}</style>',unsafe_allow_html=True)

@st.cache
def load_data():
    df = pd.read_csv("C:\\Users\\Sathishkumar\\Desktop\\New folder\\state_wise.csv")
    return df

df = load_data()

visualization = st.sidebar.selectbox('Select a Chart type',('Bar Chart','Pie Chart','Line Chart'))
state_select = st.sidebar.selectbox('Select a state',df['State'].unique())
status_select = st.sidebar.radio('Covid-19 patient status',('Confirmed','Active','Recovered','Deaths'))
#select = st.sidebar.selectbox('Covid-19 patient status',('confirmed_cases','active_cases','recovered_cases','death_cases'))
selected_state = df[df['State']==state_select]
st.markdown("## **State level analysis**")

def get_total_dataframe(df):
    total_dataframe = pd.DataFrame({
    'Status':['Confirmed', 'Active', 'Recovered','Deaths'],
    'Number of cases':(df.iloc[0]['Confirmed'],
    df.iloc[0]['Active'], 
    df.iloc[0]['Recovered'],df.iloc[0]['Deaths'])})
    return total_dataframe
state_total = get_total_dataframe(selected_state)
if visualization=='Bar Chart':
    state_total_graph = px.bar(state_total, x='Status',y='Number of cases',
                               labels={'Number of cases':'Number of cases in %s' % (state_select)},color='Status')
    st.plotly_chart(state_total_graph)
elif visualization=='Pie Chart':
    if status_select=='Confirmed':
        st.title("Total Confirmed Cases ")
        fig = px.pie(df, values=df['Confirmed'], names=df['State'])
        st.plotly_chart(fig)
    elif status_select=='Active':
        st.title("Total Active Cases ")
        fig = px.pie(df, values=df['Active'], names=df['State'])
        st.plotly_chart(fig)
    elif status_select=='Death':
        st.title("Total Death Cases ")
        fig = px.pie(df, values=df['Deaths'], names=df['State'])
        st.plotly_chart(fig)
    else:
        st.title("Total Recovered Cases ")
        fig = px.pie(df, values=df['Recovered'], names=df['State'])
        st.plotly_chart(fig)
elif visualization =='Line Chart':
    if status_select == 'Death':
        st.title("Total Death Cases Among states")
        fig = px.line(df,x='State',y=df['Deaths'])
        st.plotly_chart(fig)
    elif status_select =='Confirmed':
        st.title("Total Confirmed Cases Among states")
        fig = px.line(df,x='State',y=df['Confirmed'])
        st.plotly_chart(fig)
    elif status_select =='Recovered':
        st.title("Total Recovered Cases Among states")
        fig = px.line(df,x='State',y=df['Recovered'])
        st.plotly_chart(fig)
    else:
        st.title("Total Active Cases Among states")
        fig = px.line(df,x='State',y=df['Active'])
        st.plotly_chart(fig)
        
def get_table():
    datatable = df[['State', 'Confirmed', 'Active', 'Recovered','Deaths']].sort_values(by=['Confirmed'],ascending =False)
    return datatable

datatable = get_table()
st.dataframe(datatable)