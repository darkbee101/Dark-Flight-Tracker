from email import message
import telebot
from telebot import types
from temp import flightnumber
from datetime import datetime
import schedule
import time
import requests
from bs4 import BeautifulSoup
import re
def inputdataparser(flightcode):
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    flightinfo = temp.match(flightcode).groups()
    return flightinfo

def getdata(url):
    r = requests.get(url)
    return r.text
def get_html(Airline_code, Flight_number, Date, Month, Year):
    # url
    url = "https://www.flightstats.com/v2/flight-tracker/"+Airline_code + \
        "/"+Flight_number+"?year="+Year+"&month="+Month+"&date="+Date
    # pass the url
    # into getdata function
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    return(soup)
 
# Get Flight number
# from Html code
 
 
 
# Get Airport name
# from HTML code
 
 
def flightstatusupdater(soup):

    status=soup.find("div", {"class": "iicbYn"})
    punctual="On Time"
    if isinstance(status, type(None))==True:
        status=soup.find("div", {"class": "hYcdHE"})
        punctual=(soup.find("div", {"class": "ggStql"})).text

    if isinstance(status, type(None))==True:
        statusmsg ="ERROR. Cannot find flight on the given date"
        punctual="00"
    else:
        statusmsg=status.text
    finalmsg="*"+statusmsg+ " \| "+punctual+"*"
    return finalmsg

   
    
def airportnamefinder(soup):
    airport_all=soup.find_all("div", {"class": "cHdMkI"})
    airportdepart="*"+airport_all[0].text+"*"
    airportarrival="*"+airport_all[1].text+"*"
    return airportdepart, airportarrival

    
def airlinenamefinder(soup):
    airlinename="*"+(soup.find("div", {"class": "eOUwOd"})).text +"*"
    return airlinename

 















global storetime
storetime=5
tb = telebot.TeleBot("5113850478:AAGLd3_gKvGAJ_Zf2QhNipwM4rfsM5IO90E")
global chat_id
chat_id="0"

@tb.message_handler(commands=['start', 'help'])
def send_welcome(message):
	global chat_id
	global storetime
	chat_id=message.chat.id
	print (chat_id)
	while True:
		now = datetime.now()
		if now.hour==storetime:
			infosenderdaily(now)
			if now.hour==23:
				storetime=0
			else:
				storetime=storetime+1
		else:
			time.sleep (1)
	

def infosenderdaily(now):
	flightnumber="TG601"
	flightdate=now.strftime("%d.%m.%Y")
	flightdates=now.strftime("%d\.%m\.%Y")
	inputdata=inputdataparser(flightnumber)
	date, month, year = map(str, flightdate.split('.'))
	soup = get_html(inputdata[0], inputdata[1], date, month, year)
	airportnames=airportnamefinder(soup)
	flightstatus=flightstatusupdater(soup)
	airlinename=airlinenamefinder(soup)
	finalmsg=flightdates+"\n"+"\n"+ airlinename +"\n"+"\n"+ "Flight: "+flightnumber+"\n"+"Departing From:\n"+airportnames[0]+"\n"+ "Destination:\n"+airportnames[1]+"\n"+"Flight Status:\n"+flightstatus
	tb.send_message(chat_id,  finalmsg, parse_mode="MarkdownV2")

	
	

tb.infinity_polling()
