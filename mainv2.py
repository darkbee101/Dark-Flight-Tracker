from email import message
import telebot
from telebot import types
from temp import flightnumber
from datetime import datetime
from support import airlinenamefinder, flightstatusupdater, airportnamefinder, inputdataparser, get_html
import schedule
import time
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
