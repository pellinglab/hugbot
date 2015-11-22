from time import sleep as s
import pyupm_i2clcd as lcd
scr = lcd.Jhd1313m1(0, 0x3E, 0x62)

def on_lcd(text,col):
	scr.clear()
	if col == 1:
		scr.setColor(255, 20, 147)
		scr.setCursor(0,0)
  	     	scr.write(text)
	        scr.setCursor(1,0)
      		scr.write('Sends you a hug!')


	if col == 2:
		scr.setColor(137, 156, 240)
                scr.setCursor(0,0)
                scr.write('Where there is')
                scr.setCursor(1,0)
                scr.write('luv there\'s life')

	if col == 3:
                scr.setColor(240,240,240)
                scr.setCursor(0,0)
                scr.write(text)

	if col == 4:
                scr.setColor(0, 230, 0)
                scr.setCursor(0,0)
                scr.write('Where there is')
                scr.setCursor(1,0)
                scr.write('luv there\'s life')

