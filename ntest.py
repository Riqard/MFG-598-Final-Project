# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 07:56:28 2023

@author: richa
"""
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import altair as alt


tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(['Home',"Economic Data",'Human Development Index','Manufacturing','Military Ependiture','Population'])


# MAKE DATA CHARTS AND TABLES
def show_Data(data,cntry1,cntry2,rng1,rng2,yr1,mesr1,mesr2,txt1,txt2):
    
    st.header(txt2)
    df=data
    
    #Choose what countries you want to examine (Defaulted to China and US)
    countries = st.multiselect("Choose Countries", list(df.index),[cntry1, cntry2])
    countryDB=df.T[countries]
    
    #Choose the range of years to examine (Defaulted to Minimum and Maximum)
    yR = st.slider('Please select a Range of Years',rng1, rng2,(rng1, rng2))
    
    #Creates ranged specified data
    rCountryDB=countryDB[str(min(yR)):str(max(yR))]
    
    #Displays data and its measurements
    df_pct_change = rCountryDB.T.pct_change(axis='columns')
    df_pct_change['Average % Change'] = df_pct_change.mean(axis=1)*100
    st.write(mesr1, rCountryDB.T)
    df_pct_change['Average % Change']
    
    
    #plots data and interactive map
    plot=px.line(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'})
    st.plotly_chart(plot)
    
    st.divider()
    
    #Moves to data for specific year
    st.subheader(txt1)
    
    #Choose specific year
    ySpec=st.slider('Please Choose a Specific Year',rng1,rng2,(yr1))
    ySpecStr=str(ySpec)
    
    #Makes dataframe based on specified year
    ySpecCntry=countryDB.T[str(ySpec)]
    st.write(mesr1,ySpecCntry)
        
    #Makes piechart to compare
    fig=px.pie(countryDB.T,values=str(ySpec),names=countries,color=countries)
    st.write('Examine Size Makeup at Year '+ySpecStr)
    st.plotly_chart(fig, use_container_width=True)
    bar=px.bar(ySpecCntry,color=countries, labels={'value':mesr2,'Country':'Countries','color':'Countries'},title='The Data at Year '+ySpecStr)
    st.plotly_chart(bar,use_container_width=True )

cna='China'
usa='United States'

#HOME TAB#----------------------------------------------------------------------------------------------------------------------------------------------------------






#ECONOMIC TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------


# Extract Economic Data
econData= pd.read_csv('WEOApr2023all.csv')
econData=econData.drop(labels=['WEO Country Code','ISO','WEO Subject Code','Subject Notes','Country/Series-specific Notes','Estimates Start After'], axis=1)
econData=econData.set_index(['Country'])
econData.iloc[:,3:]=econData.iloc[:,3:].astype(float)

#Get only Data in terms of USD
econDataUSD=econData[econData['Units']=='U.S. dollars']

#Get only GDP in terms of USD
econDataUSDGDP=econDataUSD[econDataUSD['Subject Descriptor']=='Gross domestic product, current prices']
econDataUSDGDP=econDataUSDGDP.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only GDP/capita in terms of USD
econDataUSDGDPCap=econDataUSD[econDataUSD['Subject Descriptor']=='Gross domestic product per capita, current prices']
econDataUSDGDPCap=econDataUSDGDPCap.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only Data in terms of PPP
econDataPPP=econData[econData['Units']=='Purchasing power parity; international dollars']

#Get only GDP in terms of PPP
econDataPPPGDP=econDataPPP[econDataPPP['Subject Descriptor']=='Gross domestic product, current prices']
econDataPPPGDP=econDataPPPGDP.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only GDP/Capita in terms of PPP
econDataPPPGDPCap=econDataPPP[econDataPPP['Subject Descriptor']=='Gross domestic product per capita, current prices']
econDataPPPGDPCap=econDataPPPGDPCap.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#cd Downloads\MFG598Data
#streamlit run ntest.py

#Code for Economics Tab
with tab2:
    st.header('Economic Data')
    
    #Give Tab Description
    st.write("This tab will display the global economic data ranging from 1980 to the projected data in 2028. " +"A country's Gross Domestic Product (GDP), is a measure of how much economic output a country generated, typically measured in US Dollars. " 
             +"A country's GDP per capita measures the economic output of a nation per resident. Purchasing Power Parity (PPP) is a metric that adjusts the US Dollar to more closely match how much a dollar is worth in a given country"
             + "These mutrics are based on items such as a nation's standard of living, currency, and more, taking a 'basket of goods' approach." )
    st.divider()
    choice=[]
    sel=st.selectbox('Choose what Data you Wish to See',('GDP-USD','GDP-USD per Capita','GDP-PPP','GDP-PPP per Capita'))
    choice.append(sel)
    if choice == ['GDP-USD']:
        USDGDP=show_Data(econDataUSDGDP,cna,usa,1980,2028,2022,'Data Measured in Millions USD (2021 Prices)','Millions USD (2021 Prices)','Compare GDP for a Specific Year',"Country's GDP in USD")
    
    if choice == ['GDP-USD per Capita']:
        USDGDPCap=show_Data(econDataUSDGDPCap,cna,usa,1980,2028,2022,'Data Measured in USD (2021 Prices)','USD (2021 Prices)','Compare GDP/Capita for a Specific Year',"Country's GDP per Capita in USD")
    
    if choice == ['GDP-PPP']:
        PPPGDP=show_Data(econDataPPPGDP,cna,usa,1980,2028,2022,'Data Measured in Purchasing Power Parity; Millions International Dollars', 'Millions International Dollars' , 'Compare GDP-PPP for a Specific Year',"Country's GDP in PPP")
   
    if choice == ['GDP-PPP per Capita']:
        PPPGDPCap=show_Data(econDataPPPGDPCap,cna,usa,1980,2028,2022,'Data Measured in Purchasing Power Parity; International Dollars', 'International Dollars', 'Compare GDP/Capita in PPP for a Specific Year',"Country's GDP per Capita in PPP")



#HUMAN DEVELOPMENT INDEX TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Extract HDI Data
hdiDF=pd.read_csv('HDR21-22_Composite_indices_complete_time_series.csv').set_index('Country')


#Code for HDI tab
with tab3:
    st.header('Human Development Index')
    hdiData=show_Data(hdiDF,cna,usa,1990,2021,2021,'Scores','Scores','Compare HDI for a Specific Year',"Country's Human Development Index")




#MANUFACTURING TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Extract and Clean Manufacturing Data
mfgData=pd.read_csv('API_NV.IND.MANF.CD_DS2_en_csv_v2_5363423.csv')
mfgData=mfgData.rename(columns={"Country Name": "Country"})
mfgData=mfgData.set_index(['Country'])
mfgData=mfgData.drop(labels=['Country Code','Indicator Code','Indicator Name'], axis=1)

with tab4:
    st.header('Manufacturing')
    mfgShow=show_Data(mfgData,cna,usa,1975,2021,2021,'Amount of Output in US Dollars', 'US Dollars' , 'Compare Amount of Output for a Specific Year', "Country's Manufacturing Output")
    


#MILITARY TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Get annual Military Expenditure Data
milExp=pd.read_csv('milExp.csv').set_index('Country')

#Get MilExp as share of GDP
milExpPer=pd.read_csv('milPercent.csv').set_index('Country')
milExpPer=milExpPer.mul(100)

with tab5:
    st.header('Military Expenditures')
    choice1=[]
    sel1=st.selectbox('Choose what Data you Wish to See',('Annual Military Expenditures','Annual Military Expenditures as a Share of GDP'))
    choice1.append(sel1)
    if choice1 == ['Annual Military Expenditures']:
        milExpData=show_Data(milExp,cna,'United States of America',1949,2022,2021,'Measured in Millions USD (2021 prices)', 'Millions US Dollars (2021 prices)' ,'Compare Military Expenditure in a Specifc Year', 'Annual Military Expenditure')
    if choice1 == ['Annual Military Expenditures as a Share of GDP']:
        milExpPerData=show_Data(milExpPer,cna,'United States of America',1949,2022,2021,'Measured as a Percent Makeup', 'Percentage of GDP' ,'Compare Share of GDP in a Specifc Year', 'Annual Military Expenditure as a Share of GDP')


        

#POPULATION TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

popData=pd.read_csv('totpopmf.csv')
popData['Time']=popData['Time'].astype(str)
popData=popData.rename(columns={"Location": "Country"})
totPopData=popData.drop(labels=['PopMale','PopFemale'], axis=1).pivot_table(values='PopTotal', index='Country', columns='Time', aggfunc='first')*1000
mPopData=popData.drop(labels=['PopTotal','PopFemale'], axis=1).pivot_table(values='PopMale', index='Country', columns='Time', aggfunc='first')*1000
fPopData=popData.drop(labels=['PopTotal','PopMale'], axis=1).pivot_table(values='PopFemale', index='Country', columns='Time', aggfunc='first')*1000

with tab6:
    st.header('Population Data')
    choice2=[]
    sel2=st.selectbox('Choose what Data you Wish to See',('Total Population','Male Population','Female Population'))
    choice2.append(sel2)
    if choice2==['Total Population']:
        totPopData=show_Data(totPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,   'Compare Populations', 'Total Populations of Countries')
    if choice2==['Male Population']:
        totPopData=show_Data(mPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,   'Compare Populations', 'Total Male Populations of Countries')
    if choice2==['Female Population']:
        totPopData=show_Data(fPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,  'Compare Populations', 'Total Female Populations of Countries')
