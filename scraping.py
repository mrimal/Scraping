# -*- coding: utf-8 -*-
"""
Spyder Editor

@mrijan
"""



import mechanize
import cookielib
import config
import BeautifulSoup
import requests

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

r = requests.post(config.url, data={'fromdate': '2016-12-25', 'todate': '2017-02-28', 'stype': 'commodity_wise', 'page':'commodity', 'commodity_english[]':'Yogurt'})
print(r.status_code, r.reason)
print(r.text)