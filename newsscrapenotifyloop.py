#!/usr/bin/python
import sys
import urllib2
import bs4
from bs4 import BeautifulSoup
import csv
import os
import time
import platform


speakCommand = ''

if platform.system() == "Darwin":
  speakCommand = "say "
elif platform.system() == "Windows":
  speakCommand = 'C:\\Progra~1\\eSpeak\\command_line\\espeak.exe '
elif platform.system() == "Linux":
  speakCommand = 'espeak '

def priceSensitive(imgTag):
  if imgTag is None:
    return 'false'
  if len(imgTag['src']) > 0:
    return 'true'
  else:
    return 'false'

def spellOutWord(word):
  return '.'.join(word)

def spellOutWords(words):
  return ','.join( '.'.join(s) for s in words)

def readLatestHeadlines(symbolHeadlines):
  newHeadlines = list()
  for symbol in symbolHeadlines.keys():
    #soup = BeautifulSoup(urllib2.urlopen('http://www.asx.com.au/asx/research/companyInfo.do?by=asxCode&allinfo=&asxCode=' + symbol ).read())

    #soup = BeautifulSoup(urllib2.urlopen('http://www.asx.com.au/asx/statistics/announcements.do?by=asxCode&asxCode=' + symbol + '&timeframe=Y&year=2013').read())
    soup = BeautifulSoup(urllib2.urlopen('http://www.asx.com.au/asx/statistics/announcements.do?by=asxCode&asxCode=' + symbol + '&timeframe=D&period=T').read())
    table = soup.table
  
    print('symbol,date,price sensitive,headline,number of pages,link')
    if table is not None:
      for row in table.findAll('tr'):
        cols = row.findAll('td')
        if len(cols) > 0:
          line = (symbol + ',' + (cols[0].string or "").strip(' \t\r\n') + ',' + 
                priceSensitive(cols[1].find('img')) + ',' + 
                (cols[2].string or "").strip(' \t\r\n') + ',' + 
                (cols[3].string or "").strip(' \t\r\n') + ',' + 
                'http://www.asx.com.au/' + cols[4].find('a').get('href'))
              #(cols[4].string or "").strip(' \t\r\n'))  # PDF link

          #if priceSensitive(cols[1].find('img')):
            #os.system('say ' + spellOutWord(symbol) + ', ' + cols[2].string)
          
          if not line in symbolHeadlines[symbol]:
            newHeadlines.append(spellOutWord(symbol) + ', ' + cols[2].string)
            symbolHeadlines[symbol].append(line)
            print(line)

  return (symbolHeadlines, newHeadlines)

def marketStatus():
  soup = BeautifulSoup(urllib2.urlopen('http://asx.com.au/asx/widget/marketStatus.do').read())
  return (soup.find(id='status').span.get_text())
  

def main():
  if len(sys.argv) < 2:
    print("Usage: python newsscrape.py ncm bhp rio")
    exit()
  
  symbolHeadlines = dict()
  
  for symbol in sys.argv[1:]:
    symbolHeadlines[symbol] = list()
  
  #print('say Greetings commander.  The latest market news for the following companies: ' +  spellOutWords(sys.argv[1:]) + ', is as follows:')
  #os.system('say Greetings commander.  The latest market news for the following companies: ' + spellOutWords(sys.argv[1:]) + ', is as follows:')
  print(speakCommand + '" Greetings commander.  The latest market news for the following companies: ' +  spellOutWords(sys.argv[1:]) + ', is as follows:"')
  os.system(speakCommand + '" Greetings commander.  The latest market news for the following companies: ' + spellOutWords(sys.argv[1:]) + ', is as follows:"')

  while True:
    #os.system('say Scanning for news') 
    os.system(speakCommand + '" ASX is ' + marketStatus() + '"')
    symbolHeadlines, newHeadlines = readLatestHeadlines(symbolHeadlines)
    for headline in newHeadlines:
      #os.system('say ' + headline)
      os.system(speakCommand + '" ' + headline + '"')
    time.sleep(60 * 10)


main()
