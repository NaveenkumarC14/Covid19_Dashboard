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
vaccine=pd.read_csv("http://api.covid19india.org/csv/latest/vaccine_doses_statewise_v2.csv")
test=pd.read_csv('https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv')


#import streamlit as st
import base64
st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%;">COVID-19 Interactive Dashboard</h1>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;">It shows Coronavirus Cases and Forecasting in India</p>
  <h3></h3>
  <p style="margin: auto; font-weight: bold; text-align: center; width: 100%;">(Best Viewed on Desktop.Use Landscape or Desktop mode for Mobile View)</p>
  
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
dis_vac_new=dis_vac.iloc[:,[2,5,-2,-1]]
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

total=vaccine['Total Doses Administered'].iloc[-1]
#aa=total.iloc[0]
#total=int(total.iloc[0,len(aa)-1])
def special_format(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)
va_v2=vaccine.iloc[-38:]
va=va_v2[['State','Total Doses Administered']]
va.columns.values[1]='Vaccine'
df=pd.merge(df,va)





tested_total=pd.read_csv('https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv')
total_test1=tested_total['Total Samples Tested'].iloc[-2]
total_test=int(total_test1)
st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
    <h1 style="margin: auto: width: 100%;">''' + str(special_format(total_test)) + ''' Tested</h1>
    <h1 style="margin: auto: width: 100%;">''' + str(special_format(total)) + ''' Vaccine Doses Administered</h1>
 </div>
''', unsafe_allow_html=True);

state_wise_daily=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
daily_test=pd.read_csv('https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv')
daily_vaccine=pd.read_csv('http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv')



Daily=st.selectbox('Daily',('None','Confirmed','Recovered','Deceased','Tested','Vaccine'))
#daily_state = st.selectbox('Choose state',daily_vaccine['State'].unique())
selected_state_daily = daily_vaccine[daily_vaccine['State']=='India']
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
if Daily=='Tested':
	fig=px.bar(daily_test,x='Tested As Of',y="Total Samples Tested",labels={'Tested As Of':'Date'})
	st.plotly_chart(fig)
if Daily=='Vaccine':
        #daily_state = st.selectbox('Choose state',daily_vaccine['State'].unique())
       # selected_state_daily = daily_vaccine[daily_vaccine['State']==daily_state]	
	fig=px.bar(selected_state_daily,x='Updated On',y="Total Doses Administered",labels={'Updated On':'Date'})
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
   <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: ''' + str(vaccine['Vaccinated As of'].iloc[-1]) + '''</p>
</div>
''', unsafe_allow_html=True);
#st.markdown("## **Overall Cases**")


st.markdown('''
            <div style="height:150px;width: 2%; background-color: white; float:left;left: 1500px; border-radius: 2px;"">
            </div>
                    <div>
		     <div style="height:100px;width: 22%; background-color: #FF7276; float:left; left: 1700px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		    <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; color: #2F4F4F; font-size: 12px; padding: 20px 25px 0px 20px;">Confirmed</div>
                        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(Total_Confirmed) +''' </div>
            </div>
	</div>
            <div style="height:150px;width: 2%;background-color: white; float:left; left: 200px; border-radius: 2px;">
	     </div>
                    <div>
			<div style="height:100px;width: 22%; background-color: #ADD8E6; float:left; left: 1500px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center ; font-weight: bold; color: #2F4F4F; font-size: 12px; padding: 20px 25px 0px 20px;">Active</div>
                       <div style="font-family: Arial, Helvetica, sans-serif; text-align: center ;font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(Total_Active)+'''  </div>
	    </div>
	    </div>
		<div style="height:150px;width: 2%; background-color: white; float:left;left: 150px; border-radius: 2px;"">
            </div>
                    <div>
          	 <div style="height:100px;width: 22%; background-color:#A9A9A9; float:left; left: 700px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		    <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; color: #2F4F4F; font-size: 12px; padding: 20px 25px 0px 20px;">Deaths</div>
                        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(Total_Death) +''' </div>
                 </div>
            </div>
		<div style="height:150px;width: 2%; background-color: white; float:left;left: 300px; border-radius: 2px;"">
            </div>
                    <div>
		    <div style="height:100px;width: 22%; background-color: #90EE90; float:left; left: 1400px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		    <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; color: #2F4F4F; font-size: 12px; padding: 20px 25px 0px 20px;">Recovered</div>
                        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(Total_Recovered) +''' </div>
                  </div>
		  </div>
	   
	''' , unsafe_allow_html=True);




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
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: ''' + str(vaccine['Vaccinated As of'].iloc[-1]) + '''</p>
</div>
 ''', unsafe_allow_html=True);



st.markdown('''
            <div style="height:150px;width: 2%; background-color: white; float:left;left: 1500px; border-radius: 2px;"">
            </div>
                    <div>
		     <div style="height:100px;width: 22%; background-color: white; float:left; left: 1700px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		    <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; color: #33adff; font-size: 12px; padding: 20px 25px 0px 20px;">Confirmed</div>
                        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(selected_state['Confirmed'].iloc[0]) +''' </div>
            </div>
	</div>
            <div style="height:150px;width: 2%;background-color: white; float:left; left: 200px; border-radius: 2px;">
	     </div>
                    <div>
			<div style="height:100px;width: 22%; background-color: white; float:left; left: 1500px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center ; font-weight: bold; color: #33adff; font-size: 12px; padding: 20px 25px 0px 20px;">Active</div>
                       <div style="font-family: Arial, Helvetica, sans-serif; text-align: center ;font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(selected_state['Active'].iloc[0])+'''  </div>
	    </div>
	    </div>
		<div style="height:150px;width: 2%; background-color: white; float:left;left: 150px; border-radius: 2px;"">
            </div>
                    <div>
          	 <div style="height:100px;width: 22%; background-color: white; float:left; left: 700px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		    <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; color: #33adff; font-size: 12px; padding: 20px 25px 0px 20px;">Deaths</div>
                        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(selected_state['Deaths'].iloc[0]) +''' </div>
                 </div>
            </div>
		<div style="height:150px;width: 2%; background-color: white; float:left;left: 300px; border-radius: 2px;"">
            </div>
                    <div>
		    <div style="height:100px;width: 22%; background-color: white; float:left; left: 1400px; border-radius: 20px; border: 2px solid #d9d9d9; border-right: right;">
		    <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; color: #33adff; font-size: 12px; padding: 20px 25px 0px 20px;">Recovered</div>
                        <div style="font-family: Arial, Helvetica, sans-serif;text-align: center; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 2px;">'''+ str(selected_state['Recovered'].iloc[0]) +''' </div>
                  </div>
		  </div>
	   
	''' , unsafe_allow_html=True);




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
dis=dis3.drop([768,772,769,767,770,771,766,158,211,219,270,271,312,347,459,472])
#vaccine=new[new['State']==state_select1]  #line74
#dis=pd.merge(dis,new)
state_select1 = st.selectbox('Select a state',dis['State'].unique())
selected_state1 = dis[dis['State'] == state_select1]  #use new for vaccine line 75

                 
    
vaccine=selected_state1.groupby(['District'],as_index=False).agg('sum')
#vaccine_state=pd.merge(dis,vaccine)

	
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
