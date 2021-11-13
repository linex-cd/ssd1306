#!/usr/bin/env python

# RASPBERRY PI VERSION

# NOTE: You need to have PIL installed for your python at the Pi

from lib_oled96 import ssd1306
from time import sleep
from time import strftime
from PIL import ImageFont, ImageDraw, Image
font = ImageFont.load_default()

font_file = 'font.ttf'
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


	draw.text((8, 2), '远上寒山石径斜', font=font16, fill=1)
	draw.text((8, 15), '白云生处有人家', font=font16, fill=1)
	draw.text((8, 30), '停车坐爱枫林晚', font=font16, fill=1)
	draw.text((8, 45), '霜叶红于二月花', font=font16, fill=1)
	oled.display()

	sleep(3)
	oled.invert()
	sleep(1)
	oled.normal()
	sleep(1)
	oled.scrollonleft()
	sleep(6)
	oled.scrolloff()
#enddef

import json
import requests
import psutil

def show():
	while 1:
		oled.cls()
		draw = oled.canvas
		
		
		#time
		datestr = strftime("%Y-%m-%d")
		timestr = strftime("%H:%M:%S")
		
		draw.text((16, 10), datestr, font=font24, fill=1)
		draw.text((16, 30), timestr, font=font24, fill=1)
		
		#systeminfo
		mem_percent = psutil.virtual_memory().percent
		mem_total = psutil.virtual_memory().total
		mem_available = psutil.virtual_memory().available
		#memstr = '内存:%.1f%%(%d/%d MB)' % (mem_percent, int((mem_total - mem_available)/1024/1024), int(mem_total/1024/1024))
		memstr = '内存:%.1f%%' % (mem_percent)
		#print(memstr)
		
		disk_percent = psutil.disk_usage("/").percent
		disk_total = psutil.disk_usage("/").total
		disk_used= psutil.disk_usage("/").used
		#disktr = '硬盘:%.1f%%(%d/%d MB)' % (disk_percent, int((disk_used)/1024/1024), int(disk_total/1024/1024))
		disktr = '硬盘:%.1f%%' % (disk_percent)
		#print(disktr)
		
		cpu_percent = psutil.cpu_percent(0)
		cpustr = 'CPU:%.1f%%' % (cpu_percent)
		#print(cpustr)
		
		temp_current = psutil.sensors_temperatures()['cpu_thermal'][0].current
		tempstr = '温度:%.1f°C' % (temp_current)
		#print(tempstr)
		
		draw.text((0, 0), memstr, font=font12, fill=1)
		draw.text((64, 0), disktr, font=font12, fill=1)
		draw.text((0, 52), cpustr, font=font12, fill=1)
		draw.text((64, 52), tempstr, font=font12, fill=1)
		
		oled.display()
		sleep(0.2)
	#endwhile
#enddef



start()

show()




		