# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 08:20:50 2020

@author: Naveenkumar
"""





import streamlit as st
import pandas as pd
import numpy as np 
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

#from googleDriveFileDownloader import googleDriveFileDownloader
#a=googleDriveFileDownloader()
#a.downloadFile("https://drive.google.com/file/d/1aaq_cBChM-mPiDwefukBiwRKQ3Vt3JFv/view?usp=sharing")


df1 = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")

#import streamlit as st
import base64
st.title('Covid-19 India Cases')
st.write("It shows ***Coronavirus Cases*** in India")
st.sidebar.title("Menu")


#image = PhotoImage(file = 'C:\\Users\\Sathishkumar\\Videos\\Corona-is-innocent.gif')
image= open("1e4585a1cd51216e70f33db2954eb83c.gif",'rb')
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
selected_series = st.sidebar.selectbox("Forecasting:", ('None','Confirmed Cases', 'Death Cases', 'Recovered Cases'))
#st.sidebar.text("Created By:-")
st.sidebar.write("Created By:- **_Naveenkumar C_** :sunglasses:")
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
Total_Confirmed=total['Number of cases'].iloc[0]
Total_Death=total['Number of cases'].iloc[3]
Total_Recovered=total['Number of cases'].iloc[2]
Total_Active=total['Number of cases'].iloc[1]

st.markdown('''
<h1></h1>
<div class="jumbotron text-center" style='padding: 0px';background-color:#fff>
 <div class="row" style="background-color:#fff;width:100%;margin:auto;">
    <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: red'>Total Confirmed</p>
      <p style='text-align: center; font-size: 15px; color: red'>[''' + str(Total_Confirmed) + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: red'>''' + str(Total_Confirmed) + '''</p>
    </div>
    <div class="row-sm-4" style='background-color: #fff; border-radius: 5px'>
      <p style='text-align:center; font-weight: 400 ; color: #000'>Total Deaths</p>
      <p style='text-align: center; font-size: 15px; color: #e73631'>[''' + str(Total_Death) + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #e73631'>''' + str(Total_Death) + '''</p>
    </div>
    <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Recovered</p>
      <p style='text-align: center; font-size: 15px; color: #70a82c'>[''' + str(Total_Recovered) + ''']</p>
      <p style='text-align: center ; font-size: 35px; font-weight: bold; color: #70a82c'>''' + str(Total_Recovered) + '''</p>
     </div>
     <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Active</p>
      <p style='text-align: center; font-size: 15px; color: #70a82c'>[''' + str(Total_Active) + ''']</p>
      <p style='text-align: center ; font-size: 35px; font-weight: bold; color: #70a82c'>''' + str(Total_Active) + '''</p>
     </div>
  </div>
</div>
 ''', unsafe_allow_html=True);
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
   

    
#def get_table():
 #   datatable = total[['Status','Number of cases']]
 #   return datatable

#datatable = get_table()
#st.dataframe(datatable)


st.markdown("## **State level analysis**")
st.markdown('''
<h1></h1>
<div class="jumbotron text-center" style='padding: 0px';background-color:#fff>
 <div class="row" style="background-color:#fff;width:100%;margin:auto;">
    <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: red'>Total Confirmed</p>
      <p style='text-align: center; font-size: 15px; color: red'>[''' + str(selected_state['Confirmed']) + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: red'>''' + str(selected_state['Confirmed']) + '''</p>
    </div>
    <div class="row-sm-4" style='background-color: #fff; border-radius: 5px'>
      <p style='text-align:center; font-weight: 400 ; color: #000'>Total Deaths</p>
      <p style='text-align: center; font-size: 15px; color: #e73631'>[''' + str(selected_state['Deaths']) + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #e73631'>''' + str(selected_state['Deaths'])+ '''</p>
    </div>
    <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Recovered</p>
      <p style='text-align: center; font-size: 15px; color: #70a82c'>[''' + str(selected_state['Recovered']) + ''']</p>
      <p style='text-align: center ; font-size: 35px; font-weight: bold; color: #70a82c'>''' + str(selected_state['Recovered']) + '''</p>
     </div>
     <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Active</p>
      <p style='text-align: center; font-size: 15px; color: #70a82c'>[''' + str(selected_state['Active']) + ''']</p>
      <p style='text-align: center ; font-size: 35px; font-weight: bold; color: #70a82c'>''' +str(selected_state['Active']) + '''</p>
     </div>
  </div>
</div>
 ''', unsafe_allow_html=True);


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
df2 = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
if selected_series == 'Confirmed Cases':
    st.markdown("## **Forecasting**")
    prophet_df=df2.rename(columns={'Date_YMD':"ds","Total Confirmed":"y"})
    model=Prophet()
    model.fit(prophet_df)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)
    fig=plot_plotly(model,forecast)
    fig.update_layout(title="Forecast of Confirmed Cases",yaxis_title="Cases",xaxis_title="Date")
    st.plotly_chart(fig)
elif selected_series=="Death Cases":
    st.markdown("## **Forecasting**")
    prophet_df=df2.rename(columns={'Date_YMD':"ds","Total Deceased":"y"})
    model=Prophet()
    model.fit(prophet_df)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)
    fig=plot_plotly(model,forecast)
    fig.update_layout(title="Forecast of Death Cases",yaxis_title="Cases",xaxis_title="Date")
    st.plotly_chart(fig)
elif selected_series=="Recovered Cases":
    st.markdown("## **Forecasting**")
    prophet_df=df2.rename(columns={'Date_YMD':"ds","Total Recovered":"y"})
    model=Prophet()
    model.fit(prophet_df)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)
    fig=plot_plotly(model,forecast)
    fig.update_layout(title="Forecast of Recovered Cases",yaxis_title="Cases",xaxis_title="Date")
    st.plotly_chart(fig)


