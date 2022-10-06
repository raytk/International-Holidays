from re import S
import selenium
from selenium.webdriver.common.by import By
from SeleniumDriverSetup import driversetup as DSU
from datetime import date
from time import sleep
import pandas as pd
from datetime import datetime as dt
from os import walk


cy = date.today().year

url = 'https://www.timeanddate.com/holidays/?allcountries'
cdver = DSU(url,'',True)

countries = []
for elem in cdver.find_element(By.CLASS_NAME,'category-list').find_elements(By.TAG_NAME,'a'):
    if elem.get_attribute('innerHTML').find('<')<0:
        if elem.get_attribute('innerHTML') == 'Vatican City (Holy See)':
            countryname = 'vatican-city-state'
        else:
            countryname = elem.get_attribute('innerHTML')
        countries.append(countryname)

fs = []
for dirs,subdirs,files in walk(r'D:\Github\KITOWHATE\Artifacts\International Holidays'):
    for file in files:
        file = file.replace('.csv','').lower().replace('-',' ')
        fs.append(file)

for c in countries:
    if any(c.lower() in s for s in fs) == False:
        print(c)
        if c.find(' ')>=1:
            c = c.replace(' ','-')
        dfmain = pd.DataFrame()
        for year in range(2000,cy+1):
            cdver.get('https://www.timeanddate.com/holidays/%s/%s' % (c.lower(),year)) 
            try:
                cdver.find_element(By.ID,'holidays-table')
            except:
                continue
            df = pd.read_html(cdver.page_source)[0]
            if len(df.columns)>4:
                df.drop(columns=df.columns[-1],axis=1,inplace=True)
            df.columns = df.columns.droplevel()
            df.columns = ['Date', 'Day', 'Name','Type']
            df.dropna(axis=0,inplace=True)
            df.reset_index(inplace=True)
            df.drop(['index'],axis=1,inplace=True)
            for i in range(0,len(df)):
                try:
                    df.at[i,'Date'] = dt.strptime(df.at[i,'Date'] + ' ' + str(year),'%d %b %Y').strftime('%d/%m/%Y')
                except:
                    df.drop(i,inplace=True)
            
            dfmain = pd.concat([dfmain,df])
        dfmain.to_csv('D:\\Github\\KITOWHATE\\Artifacts\\International Holidays\\%s.csv' % (c),index=False)