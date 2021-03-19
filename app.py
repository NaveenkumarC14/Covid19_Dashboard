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
from googleDriveFileDownloader import googleDriveFileDownloader
a=googleDriveFileDownloader()
a.downloadFile("https://drive.google.com/file/d/1aaq_cBChM-mPiDwefukBiwRKQ3Vt3JFv/view?usp=sharing")


df1 = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")

#import streamlit as st
import base64
st.title('Covid-19 India Cases')
st.write("It shows ***Coronavirus Cases*** in India")
st.sidebar.title("Menu")


#image = PhotoImage(file = 'C:\\Users\\Sathishkumar\\Videos\\Corona-is-innocent.gif')
image= open(a, "rb")
contents = image.read()
data_url = base64.b64encode(contents).decode("utf-8")
image.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="corona gif">',
    unsafe_allow_html=True,
)

#image = Image.open("C:\\Users\\Sathishkumar\\Videos\\Corona-is-innocent.gif")
#st.image(image,use_column_width=False)
#st.markdown('<style>body{background-color: lightblue;}</style>',unsafe_allow_html=True)

@st.cache
def load_data():
    df1 = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
    df=df1.drop([0,37])
    return df

df = load_data()

visualization = st.sidebar.selectbox('Select a Chart type',('Bar Chart','Pie Chart','Line Chart','Scatter Chart'))
#total=st.sidebar.selectbox('Select a Total Cases',df1['State'].iloc[0],)
state_select = st.sidebar.selectbox('Select a state',df['State'].unique())
status_select = st.sidebar.radio('Covid-19 patient status',('Confirmed','Active','Recovered','Deaths'))
#select = st.sidebar.selectbox('Covid-19 patient status',('confirmed_cases','active_cases','recovered_cases','death_cases'))
selected_state = df[df['State']==state_select]
st.markdown("## **Overall Cases**")

df1 = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
def get_total(df1):
    total = pd.DataFrame({
    'Status':['Confirmed', 'Active', 'Recovered','Deaths'],
    'Number of cases':(df1.iloc[0]['Confirmed'],
    df1.iloc[0]['Active'], 
    df1.iloc[0]['Recovered'], df1.iloc[0]['Deaths'])})
    return total
total=get_total(df1)

if visualization=='Bar Chart':
    total_graph = px.bar(total, x='Status',y='Number of cases',
                               labels={'Number of cases':'Number of Total cases'},color='Status')
    st.plotly_chart(total_graph)

elif visualization=='Pie Chart':
    #if total==(df1['State'].iloc[0],):
        st.title("Total Cases")
        fig = px.pie(total, values=total['Number of cases'], names=total['Status'])
        st.plotly_chart(fig)
elif visualization =='Line Chart':
        st.title("Total Cases")
        fig = px.line(total,x=total['Status'],y=total['Number of cases'])
        st.plotly_chart(fig)
elif visualization =='Scatter Chart':
        #fig=px.scatter(total, x=total['Status'], y=total['Number of cases'], color=total['Status'],size=total['Number of cases'])
        fig=px.scatter(total, x=total['Status'], y=total['Number of cases'],
	         size="Number of cases", color=total['Status'],size_max=60)    
        st.plotly_chart(fig)
    
    
def get_table():
    datatable = total[['Status','Number of cases']]
    return datatable

datatable = get_table()
st.dataframe(datatable)


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
        
elif visualization =='Scatter Chart':
        #fig=px.scatter(total, x=total['Status'], y=total['Number of cases'], color=total['Status'],size=total['Number of cases'])
    if status_select == 'Deaths':
        st.title("Total Death Cases Among states")   
        fig=px.scatter(df, x='State', y=df['Deaths'],
	         size="Deaths",size_max=110)    
        st.plotly_chart(fig)
    elif status_select =='Confirmed':
      st.title("Total Confirmed Cases Among states")
      fig=px.scatter(df, x='State', y=df['Confirmed'],
	         size="Confirmed",size_max=110)
      st.plotly_chart(fig)
    elif status_select =='Recovered':
        st.title("Total Recovered Cases Among states")
        fig=px.scatter(df, x='State', y=df['Recovered'],
	         size="Recovered",size_max=110)
        st.plotly_chart(fig)
    else:
        st.title("Total Active Cases Among states")
        fig=px.scatter(df, x='State', y=df['Active'],
	         size="Active",size_max=110)
        st.plotly_chart(fig)

def get_table():
    datatable = df[['State', 'Confirmed', 'Active', 'Recovered','Deaths']].sort_values(by=['Confirmed'],ascending =False)
    return datatable

datatable = get_table()
st.dataframe(datatable)
