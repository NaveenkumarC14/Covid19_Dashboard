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
vaccine=pd.read_csv("http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv")
test=pd.read_csv('https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv')


#import streamlit as st
import base64
st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">COVID-19 Interactive Dashboard</h1>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;">It shows Coronavirus Cases and Forecasting in India</p>
  
</div>
''', unsafe_allow_html=True);
#st.title('Covid-19 India Cases')
#st.write("It shows ***Coronavirus Cases*** and ***Forecasting*** in India")
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

	
# = Image.open("C:\\Users\\Sathishkumar\\Videos\\Corona-is-innocent.gif")
#st.image(image,use_column_width=False)
#st.markdown('<style>body{background-color: lightblue;}</style>',unsafe_allow_html=True)

@st.cache
def load_data():
    df1 = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
    df=df1.drop([0,37])
    return df

df = load_data()
df1 = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
df=df1.drop([0,37])
dis_vac=pd.read_csv('http://api.covid19india.org/csv/latest/cowin_vaccine_data_districtwise.csv')
dis_vac_new=dis_vac.iloc[:,[5,-2,-1]]
new1=dis_vac_new.drop(0)
new=new1.fillna(0)
new.iloc[:,-2]=new.iloc[:,-2].astype(int)
new.iloc[:,-1]=new.iloc[:,-1].astype(int)
new["Vaccine"]=new.sum(axis=1)

visualization = st.sidebar.selectbox('Select a Chart type',('Bar Chart','Pie Chart','Line Chart','Scatter Chart'))
#total=st.sidebar.selectbox('Select a Total Cases',df1['State'].iloc[0],)
state_select = st.sidebar.selectbox('Select a state',df['State'].unique())
status_select = st.sidebar.radio('Covid-19 patient status',('Confirmed','Active','Recovered','Deaths'))
#select = st.sidebar.selectbox('Covid-19 patient status',('confirmed_cases','active_cases','recovered_cases','death_cases'))
selected_state = df[df['State']==state_select]

selected_series = st.sidebar.selectbox("Forecasting:", ('None','Confirmed Cases', 'Death Cases', 'Recovered Cases'))
#st.sidebar.text("Created By:-")
#st.sidebar.write("Created By:- **_Naveenkumar C_** :sunglasses:")

total=vaccine[vaccine['State']=='Total']
aa=total.iloc[0]
total=int(total.iloc[0,len(aa)-1])
def special_format(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)
va=vaccine.iloc[:,[0,-1]]
va.columns.values[1]='Vaccine'
df=pd.merge(df,va)

tested_total=pd.read_csv('https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv')
total_test1=tested_total['Total Samples Tested'].iloc[-1]
total_test=int(total_test1)
st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
    <h1 style="margin: auto: width: 100%;">''' + str(special_format(total_test)) + ''' Tested</h1>
    <h1 style="margin: auto: width: 100%;">''' + str(special_format(total)) + ''' Vaccine Doses Administered</h1>
 </div>
''', unsafe_allow_html=True);

state_wise_daily=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
Daily=st.selectbox('Daily',('None','Confirmed','Recovered','Deceased','Tested','Vaccine'))
if Daily=='Confirmed':
	Confirmed=state_wise_daily[state_wise_daily['Status']=='Confirmed']
	fig=px.bar(Confirmed,x='Date',y="TT",labels={'TT':'Number of Total cases'})
	st.plotly_chart(fig)
if Daily=='Recovered':
	Recovered=state_wise_daily[state_wise_daily['Status']=='Recovered']
	fig=px.bar(Recovered,x='Date',y="TT",labels={'TT':'Number of Total cases'})
	st.plotly_chart(fig)
if Daily=='Deceased':
	Deceased=state_wise_daily[state_wise_daily['Status']=='Deceased']
	fig=px.bar(Deceased,x='Date',y="TT",labels={'TT':'Number of Total cases'})
	st.plotly_chart(fig)
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
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">Overall Cases</h1>
   <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: ''' + str(df1['Last_Updated_Time'][0]) + '''</p>
</div>
''', unsafe_allow_html=True);
#st.markdown("## **Overall Cases**")

st.markdown('''

<div class="jumbotron text-center" style='padding: 0px';background-color:#fff>
 <div class="row" style="background-color:#fff;width:100%;margin:auto;">
    <div class="row-sm-3">
      <p style ='text-align: center; background-color: #fff; font-weight: 400 ;color: red'>Total Confirmed</p>
      <p style='text-align: center; font-size: 15px; color: red'></p>
      <p style='text-align: center; font-size: 40px; font-weight: 600; color: red'>''' + str(Total_Confirmed) + '''</p>
    </div>    
    <div class="row-sm-3" style='background-color: #fff; border-radius: 5px'>
      <p style='text-align:center; font-weight: 400 ; color: black'>Total Deaths</p>
      <p style='text-align: center; font-size: 15px; color: black'></p>
      <p style='text-align: center; font-size: 40px; font-weight: 600; color: black'>''' + str(Total_Death)+ '''</p>
    </div>    
    <div class="row-sm-3">    
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: green'>Total Recovered</p>
      <p style='text-align: center; font-size: 15px; color: green'></p>
      <p style='text-align: center ; font-size: 40px; font-weight: 600; color: green'>''' + str(Total_Recovered) + '''</p>    
     </div>     
    <div class="row-sm-3">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: blue'>Total Active</p>
      <p style='text-align: center; font-size: 15px; color: green'></p>
      <p style='text-align: center ; font-size: 40px; font-weight: 600; color: blue'>''' + str(Total_Active) + '''</p>
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
        #st.title("Total Cases")
        fig = px.pie(total, values=total['Number of cases'], names=total['Status'])
        st.plotly_chart(fig)
elif visualization =='Line Chart':
        #st.title("Total Cases")
        fig = px.line(state_wise_daily, x="Date", y="TT",labels={'TT':'Number of Total cases'}, color="Status",
              line_group="Status", hover_name="Status")
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










st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">State level analysis</h1>
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: ''' + str(selected_state['Last_Updated_Time'].iloc[0]) + '''</p>
</div>
 ''', unsafe_allow_html=True);

st.markdown('''

<div class="jumbotron text-center" style='padding: 0px';background-color:#fff>
 <div class="row" style="background-color:#fff;width:100%;margin:auto;">
    <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: red'>Total Confirmed</p>
      <p style='text-align: center; font-size: 15px; color: red'></p>
      <p style='text-align: center; font-size: 42px; font-weight: bold; color: red'>''' + str(selected_state['Confirmed'].iloc[0]) + '''</p>
    </div>
    <div class="row-sm-4" style='background-color: #fff; border-radius: 5px'>
      <p style='text-align:center; font-weight: 400 ; color: black'>Total Deaths</p>
      <p style='text-align: center; font-size: 15px; color: #e73631'></p>
      <p style='text-align: center; font-size: 42px; font-weight: bold; color: black'>''' + str(selected_state['Deaths'].iloc[0])+ '''</p>
    </div>
    <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: green'>Total Recovered</p>
      <p style='text-align: center; font-size: 15px; color: green'></p>
      <p style='text-align: center ; font-size: 42px; font-weight: bold; color:green'>''' + str(selected_state['Recovered'].iloc[0]) + '''</p>
     </div>
     <div class="row-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: blue'>Total Active</p>
      <p style='text-align: center; font-size: 15px; color: blue'></p>
      <p style='text-align: center ; font-size: 42px; font-weight: bold; color: blue'>''' +str(selected_state['Active'].iloc[0]) + '''</p>
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
    datatable = df[['State', 'Confirmed', 'Active', 'Recovered','Deaths','Vaccine']].sort_values(by=['Confirmed'],ascending =False)
    return datatable
datatable = get_table()
st.dataframe(datatable)

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">District level analysis</h1>
   <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: ''' + str(selected_state['Last_Updated_Time'].iloc[0]) + '''</p>
</div>
 ''', unsafe_allow_html=True);

#st.markdown("## **District level analysis**")
dis1=pd.read_csv("https://api.covid19india.org/csv/latest/district_wise.csv")
dis2=dis1[2:775]
dis3=dis2.drop(607)
dis=dis3.drop([768,772])
#dis=pd.merge(dis,new)
state_select1 = st.selectbox('Select a state',dis['State'].unique())
selected_state1 = dis[dis['State'] == state_select1]
def get_table():
    datatable = selected_state1[['District', 'Confirmed', 'Active', 'Recovered','Deceased']]
    return datatable
datatable = get_table()
st.dataframe(datatable)


df2 = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
if selected_series==('Confirmed Cases'):
	st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">Forecasting</h1>
</div>
 ''', unsafe_allow_html=True);
if selected_series==( 'Death Cases'):
	st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">Forecasting</h1>
</div>
 ''', unsafe_allow_html=True);
if selected_series==( 'Recovered Cases'):
	st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">Forecasting</h1>
</div>
 ''', unsafe_allow_html=True);
	
if selected_series == 'Confirmed Cases':
    
   # st.markdown("## **Forecasting**")
    prophet_df=df2.rename(columns={'Date_YMD':"ds","Total Confirmed":"y"})
    model=Prophet()
    model.fit(prophet_df)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)
    fig=plot_plotly(model,forecast)
    fig.update_layout(title="Forecast of Confirmed Cases",yaxis_title="Cases",xaxis_title="Date")
    st.plotly_chart(fig)
elif selected_series=="Death Cases":
    #st.markdown("## **Forecasting**")
    prophet_df=df2.rename(columns={'Date_YMD':"ds","Total Deceased":"y"})
    model=Prophet()
    model.fit(prophet_df)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)
    fig=plot_plotly(model,forecast)
    fig.update_layout(title="Forecast of Death Cases",yaxis_title="Cases",xaxis_title="Date")
    st.plotly_chart(fig)
elif selected_series=="Recovered Cases":
	
    #st.markdown("## **Forecasting**")
    prophet_df=df2.rename(columns={'Date_YMD':"ds","Total Recovered":"y"})
    model=Prophet()
    model.fit(prophet_df)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)
    fig=plot_plotly(model,forecast)
    fig.update_layout(title="Forecast of Recovered Cases",yaxis_title="Cases",xaxis_title="Date")
    st.plotly_chart(fig)

st.markdown(
    '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<div class='jumbotron text-center footer' style='background-color: #fff;'>
    <div class='row'>
        <div class='col-md-12'>
            <p style='font-weight: 400'>______</p>
            <p style='font-weight: 400'>Designed, Developed and Maintained by Naveenkumar C</p>
            <p>Contact <a href='mailto:naveekumarc14@gmail.com'>naveekumarc14@gmail.com</a> to report issues<p>
        </div>
    </div>
<div>
    ''',
    unsafe_allow_html=True
)
