from requests.packages import urllib3
urllib3.disable_warnings()
import mraa
from time import sleep as s
from time import time as t
from time import localtime as locT
import json
import tweepy
from tweepy.streaming import StreamListener as streaM
from tweepy import Stream
import lcd
from math import sqrt,log

#API keys
key = 'Apiw2TmQUhef0WfO2jFf7x8SJ'
sec = '2X0qjkZwFFWfSls2VGV29i9jNzWsDzrZTYAGlWqL9bqyI80n8n'
token = '4245336989-CPrlzt40WRR5AffkorI7yI7uDsNnE2TlTx7191j'
tokenS = 'Py8M936CSd96PkkdJWu2ZHF5j85a2EcFn0koBwS9vMzXf'

auth = tweepy.OAuthHandler(key,sec)
auth.set_access_token(token,tokenS)
api = tweepy.API(auth)

def sendTweet(msg):
        #Send a single "tweet" from the authenticated account
        api.update_status(status = msg)



pot = mraa.Aio(0)   
galv = mraa.Aio(3)
#Setup gpio
pump = mraa.Gpio(12)
sol = mraa.Gpio(13)
pump.dir(mraa.DIR_OUT)
sol.dir(mraa.DIR_OUT)
#Calibrate

def calibration():
	t1 = t()
	t2 = 0
	i = 0
	calVal = 0
	while (t2-t1) <20:
		potVal = float(pot.read())
	    	calVal =  potVal + calVal
		i +=1
		t2 = t()
	calVal = (calVal/i)
	lcd.on_lcd('Calibrated: '+str(calVal),3)
	return calVal

class X (streaM):
        #Filters the recived data from the twitter feed         
        def on_data(self,data):
                #Convert the JSon object to unicode
                try:
                        y = json.loads(data)
                        name = y['user']['name']
                        at = y['user']['screen_name']
                        tweet = y['text']
                        loc = y['user']['location']
                        ti = y['created_at']
                        print at,'      ',name,'        ',tweet,'       ',loc,' ',ti
                        print
			if (u'@becon_hug' in tweet) or (u'@BeCon_Hug' in tweet) or (u'@Becon_Hug' in tweet):
				if (u'beconhug' in tweet) or (u'BeconHug' in tweet): #or (u'#beconhug' in tweet):
					lcd.on_lcd('@'+str(at),1)
					sol.write(1)
                			pump.write(1)
                			s(3)
                			pump.write(0)
					s(5)
					sol.write(0)
					s(4)
					return False
						
                except KeyError:
                        pass
                #Terminal data display

        def on_error(self,status):
                print(status)
		main()



def go():
	x = 0
	print 'Live!'
	lcd.on_lcd('cute',4)
	x =Stream(auth,X()).filter(track =['beconhug'])
	s(10)
		

def stDev(st):
	
	try:
		mean = sum(st)/len(st)
	except ZeroDivisionError:
		mean = 0
	val = 0
	for i in range(len(st)):
		val += (st[i]-mean)**2

	try:
		toRet =sqrt(val/len(st))
	except ZeroDivisionError:
		toRet = 0
	
	return 	toRet

def temp_check():
	temp_R = mraa.Aio(1)
	r = 3975
	res =(1023-float(temp_R.read()))*10000/(float(temp_R.read()))
	temp = 1/(log(res/10000)/r+1/298.15)-273.15
	return temp


#main loop
def main():
	x = 0
	calVal = calibration()
	while True:
	        lcd.on_lcd('cute',2)
		potVal = float(pot.read())
		stdAcc = []
		while potVal < (calVal+calVal*0.05):
			potVal = float(pot.read())
			stdAcc.append(float(galv.read()))
			s(0.001)
			if len(stdAcc) == 8000:
				stdAcc = []
		if (stDev(stdAcc) < 70) and (temp_check() < 35):
			sendTweet('I\'m stressed #beconhug '+str(locT().tm_hour-5)+':'+str(locT().tm_min))
			s(1)
			go()

main()
