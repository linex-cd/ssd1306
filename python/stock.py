#!/usr/bin/env python

# RASPBERRY PI VERSION

# NOTE: You need to have PIL installed for your python at the Pi

from lib_oled96 import ssd1306
from time import sleep
from time import strftime
from PIL import ImageFont, ImageDraw, Image
font = ImageFont.load_default()

font_file = '/home/pi/font.ttf'
font12 = ImageFont.truetype(font_file, 12)
font16 = ImageFont.truetype(font_file, 16)
font24 = ImageFont.truetype(font_file, 24)


from smbus import SMBus                  #  These are the only two variant lines !!
i2cbus = SMBus(1)                        #
# 1 = Raspberry Pi but NOT early REV1 board

oled = ssd1306(i2cbus)
draw = oled.canvas   # "draw" onto this canvas, then call display() to send the canvas contents to the hardware.

def start():

	# Draw some shapes.
	# First define some constants to allow easy resizing of shapes.
	padding = 2
	shape_width = 20
	top = padding
	bottom = oled.height - padding - 1
	# Draw a rectangle of the same size of screen
	draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)


	title = strftime("股市监控系统")
	subtitle = strftime("正在启动...")
	
	draw.text((16, 10), title, font=font16, fill=1)
	draw.text((34, 30), subtitle, font=font12, fill=1)
	oled.display()

	sleep(3)

#enddef

import json
import requests


def show():

	stock1 = ''
	stock2 = ''
	stock3 = ''
	stock4 = ''
	
	while 1:
		
		oled.cls()
		draw = oled.canvas
				
				
		#stock
		url = 'http://api.money.126.net/data/feed/0000001,1399001,1399300,1399006'
		
		try:

			ret = requests.get(url)
			if ret.status_code == 200:
						

				data = ret.text
			
			
			
				data = data.replace('_ntes_quote_callback(','').replace(');','')
				data = json.loads(data)
				
				stock1_num = '0000001'
				stock2_num = '1399001'
				stock3_num = '1399300'
				stock4_num = '1399006'
				
				stock1 = '%s %s' % (data[stock1_num]['name'], data[stock1_num]['price'])
				stock2 = '%s %s' % (data[stock2_num]['name'], data[stock2_num]['price'])
				stock3 = '%s  %s' % (data[stock3_num]['name'], data[stock3_num]['price'])
				stock4 = '%s %s' % (data[stock4_num]['name'], data[stock4_num]['price'])
				
				
				
			#endif
				
		except:
			pass
		#endtry
		
		#time
		datestr = strftime("%Y-%m-%d %H:%M:%S")
		draw.text((6, 0), datestr, font=font12, fill=1)
		
		draw.line((0, 14, 128, 14), fill=1)
		
		#stock
		draw.text((12, 14), stock1, font=font12, fill=1)
		draw.text((12, 26), stock2, font=font12, fill=1)
		draw.text((13, 38), stock3, font=font12, fill=1)
		draw.text((12, 50), stock4, font=font12, fill=1)

		
		oled.display()
		sleep(1)
	#endwhile
#enddef



start()

show()




		