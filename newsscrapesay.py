#!/usr/bin/python
import sys
import urllib2
import bs4
from bs4 import BeautifulSoup
import csv
import os

def priceSensitive(imgTag):
  if imgTag is None:
    return 'false'
  if len(imgTag['src']) > 0:
    return 'true'
  else:
    return 'false'

def spellOutWord(word):
	return '.'.join(word)


if len(sys.argv) < 2:
  print("Usage: python newsscrape.py ncm bhp rio")
  exit()

os.system('say Greetings commander.  The latest market news for the following companies: ' +  ', '.join(spellOutWord(sys.argv[1:])) + ', is as follows:')

for symbol in sys.argv[1:]:
  #soup = BeautifulSoup(urllib2.urlopen('http://www.asx.com.au/asx/research/companyInfo.do?by=asxCode&allinfo=&asxCode=' + symbol ).read())
  soup = BeautifulSoup(urllib2.urlopen('http://www.asx.com.au/asx/statistics/announcements.do?by=asxCode&asxCode=' + symbol + '&timeframe=Y&year=2013').read())
  table = soup.table

  print('date,price sensitive,headline,number of pages,link')
  if table is not None:
    for row in table.findAll('tr'):
      cols = row.findAll('td')
      if len(cols) > 0:
        #for link in cols[1].find_all('img'):
        #  print("AA DEBUG: " + link['src'])
        if priceSensitive(cols[1].find('img')): 
          os.system('say ' + spellOutWord(symbol) + '. ' + cols[2].string)
        print((cols[0].string or "").strip(' \t\r\n') + ',' + 
              priceSensitive(cols[1].find('img')) + ',' + 
              (cols[2].string or "").strip(' \t\r\n') + ',' + 
              (cols[3].string or "").strip(' \t\r\n') + ',' + 
              'http://www.asx.com.au/' + cols[4].find('a').get('href'))
              #(cols[4].string or "").strip(' \t\r\n'))  # PDF link
