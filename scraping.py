# -*- coding: utf-8 -*-
"""
Spyder Editor

@mrijan
"""



import mechanize
import cookielib
import config
from bs4 import BeautifulSoup
import requests
import pandas
from pandas import DataFrame
import csv

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)


#br.addheaders = [('User-agent', 'Chrome')]
# The site we will navigate into, handling it's session
br.open(config.loginurl)


for f in br.forms():
    print f

br.select_form(nr=0)

# User credentials
br.form['username'] = config.username
br.form['password'] = config.password
# Login
br.submit()

z = br.open(config.url).read()
#print(z)
fromdate = '2012-01-01'
todate = '2016-12-30'
#commodityName = 'Yogurt'
#Sending post requests to the website for the data
veggies = pandas.read_csv('veggies3.csv')

results = []

for vegs in veggies: 
    
    r = requests.post(config.url, data={'fromdate': fromdate, 'todate': todate, 'stype': 'commodity_wise', 'page':'commodity', 'commodity_english[]':vegs})
    print(r.status_code, r.reason)
    soup = BeautifulSoup(r.text)
    print soup
#print(r.text)
#pages_list = soup.find_all('input', name ='pg')

    pages_list = soup.find_all(name='input', attrs={'name': 'pg', 'type': 'hidden'})
#print(pages_list)

    a = 1 

    for pages in pages_list :
        a = a + 1
    
    print a 
    
    try:
        table = soup.find('table', {"class": "table"})
        rows = table.find_all('tr')
    except AttributeError as e:
        print 'No table found'
    
    #print(table)
    
    
    for row in rows :
        table_headers = row.find_all('th')
        if table_headers:
            results.append([headers.get_text() for headers in table_headers])
        
        table_data = row.find_all('td', attrs={})    
        if table_data:
            results.append([data.get_text() for data in table_data])
    #print(results)        
   # final_table = pandas.DataFrame(results, index=None)

#writer = pandas.ExcelWriter('output.xlsx')
#final_table.to_excel(writer,'Sheet1')
#writer.save()
   

#Trying to loop over all the available page numbers and then appending the data to the excel file. 

    for i in range(2,a):
        r = requests.post(config.url, data={'fromdate': fromdate, 'todate': todate, 'stype': 'commodity_wise', 'page':'commodity', 'commodity_english[]':vegs, 'pg': i})
        print(r.status_code, r.reason)
        soup = BeautifulSoup(r.text)
        print i
        try:
            table = soup.find('table', {"class": "table"})
            rows = table.find_all('tr')
        except AttributeError as e:
            print 'No table found'

#print(table)
   # resultsNew = []

            for row in rows :
                table_headers = row.find_all('th')
                #if table_headers:
                #    results.append([headers.get_text() for headers in table_headers])
                
                table_data = row.find_all('td', attrs={})    
                if table_data:
                    results.append([data.get_text() for data in table_data])
                    print(results)        



final_table = pandas.DataFrame(results, index=None)
    #with open('newOutput.csv','a') as f:
       #final_table.to_csv(f, header=False)
       
print(final_table)
writer = pandas.ExcelWriter('newOutput.xlsx')
final_table.to_excel(writer, 'Sheet1' )
writer.save()
