

from PIL import Image, ImageDraw


class ssd1306():

	def __init__(self, bus, address=0x3C):
		self.cmd_mode = 0x00
		self.data_mode = 0x40
		self.bus = bus
		self.addr = address
		self.width = 128
		self.height = 64
		self.pages = int(self.height / 8)
		self.image = Image.new('1', (self.width, self.height))
		self.canvas = ImageDraw.Draw(self.image) # this is a "draw" object for preparing display contents

		self._command(
			const.DISPLAYOFF,
			const.SETDISPLAYCLOCKDIV, 0x80,
			const.SETMULTIPLEX,	   0x3F,
			const.SETDISPLAYOFFSET,   0x00,
			const.SETSTARTLINE,
			const.CHARGEPUMP,		 0x14,
			const.MEMORYMODE,		 0x00,
			const.SEGREMAP,
			const.COMSCANDEC,
			const.SETCOMPINS,		 0x12,
			const.SETCONTRAST,		0xCF,
			const.SETPRECHARGE,	   0xF1,
			const.SETVCOMDETECT,	  0x40,
			const.DISPLAYALLON_RESUME,
			const.NORMALDISPLAY,
			const.DISPLAYON)

	def _command(self, *cmd):
		"""
		Sends a command or sequence of commands through to the
		device - maximum allowed is 32 bytes in one go.
		LIMIT ON ARDUINO: CMD BYTE + 31 = 32, SO LIMIT TO 31	 bl
		"""
		assert(len(cmd) <= 31)
		self.bus.write_i2c_block_data(self.addr, self.cmd_mode, list(cmd))

	def _data(self, data):
		"""
		Sends a data byte or sequence of data bytes through to the
		device - maximum allowed in one transaction is 32 bytes, so if
		data is larger than this it is sent in chunks.
		In our library, only data operation used is 128x64 long, ie whole canvas.
		"""

		for i in range(0, len(data), 31):
			self.bus.write_i2c_block_data(self.addr, self.data_mode, list(data[i:i+31]))


	def display(self):
		"""
		The image on the "canvas" is flushed through to the hardware display.
		Takes the 1-bit image and dumps it to the SSD1306 OLED display.
		"""

		self._command(
			const.COLUMNADDR, 0x00, self.width-1,  # Column start/end address
			const.PAGEADDR,   0x00, self.pages-1)  # Page start/end address

		pix = list(self.image.getdata())
		step = self.width * 8
		buf = []
		for y in range(0, self.pages * step, step):
			i = y + self.width-1
			while i >= y:
				byte = 0
				for n in range(0, step, self.width):
					byte |= (pix[i + n] & 0x01) << 8
					byte >>= 1

				buf.append(byte)
				i -= 1

		self._data(buf) # push out the whole lot

	def cls(self):
		self.image.close()
		self.image = Image.new('1', (self.width, self.height))
		self.canvas = ImageDraw.Draw(self.image)
		
	def onoff(self, onoff):
		if onoff == 0:
			self._command(const.DISPLAYOFF)
		else:
			self._command(const.DISPLAYON)
	def invert(self):
		self._command(const.INVERTDISPLAY)
		
	def normal(self):
		self._command(const.NORMALDISPLAY)
	
	def scrollonleft(self):
		self._command(0x2E);        #关闭滚动
		self._command(0x26);        #水平向左或者右滚动 26/27
		self._command(0x00);        #虚拟字节
		self._command(0x00);        #起始页 0
		self._command(0x07);        #滚动时间间隔
		self._command(0x07);        #终止页 7
		self._command(0x00);        #虚拟字节
		self._command(0xFF);        #虚拟字节
		self._command(0x2F);        #开启滚动
	
	def scrollonright(self):
		self._command(0x2E);        #关闭滚动
		self._command(0x27);        #水平向左或者右滚动 26/27
		self._command(0x00);        #虚拟字节
		self._command(0x00);        #起始页 0
		self._command(0x07);        #滚动时间间隔
		self._command(0x07);        #终止页 7
		self._command(0x00);        #虚拟字节
		self._command(0xFF);        #虚拟字节
		self._command(0x2F);        #开启滚动
	
	def scrollonup(self):
		self._command(0x2e);        #关闭滚动
		self._command(0x29);        #水平垂直和水平滚动左右 29/2a
		self._command(0x00);        #虚拟字节
		self._command(0x00);        #起始页 0
		self._command(0x07);        #滚动时间间隔
		self._command(0x07);        #终止页 1
		self._command(0x01);        #垂直滚动偏移量
		self._command(0x2F);        #开启滚动
	def scrollondown(self):
		self._command(0x2e);        #关闭滚动
		self._command(0x2a);        #水平垂直和水平滚动左右 29/2a
		self._command(0x00);        #虚拟字节
		self._command(0x00);        #起始页 0
		self._command(0x07);        #滚动时间间隔
		self._command(0x07);        #终止页 1
		self._command(0x01);        #垂直滚动偏移量
		self._command(0x2F);        #开启滚动
		
	def scrolloff(self):
		self._command(0x2e);        #关闭滚动

class const:
	CHARGEPUMP = 0x8D
	COLUMNADDR = 0x21
	COMSCANDEC = 0xC8
	COMSCANINC = 0xC0
	DISPLAYALLON = 0xA5
	DISPLAYALLON_RESUME = 0xA4
	DISPLAYOFF = 0xAE
	DISPLAYON = 0xAF
	EXTERNALVCC = 0x1
	INVERTDISPLAY = 0xA7
	MEMORYMODE = 0x20
	NORMALDISPLAY = 0xA6
	PAGEADDR = 0x22
	SEGREMAP = 0xA0
	SETCOMPINS = 0xDA
	SETCONTRAST = 0x81
	SETDISPLAYCLOCKDIV = 0xD5
	SETDISPLAYOFFSET = 0xD3
	SETHIGHCOLUMN = 0x10
	SETLOWCOLUMN = 0x00
	SETMULTIPLEX = 0xA8
	SETPRECHARGE = 0xD9
	SETSEGMENTREMAP = 0xA1
	SETSTARTLINE = 0x40
	SETVCOMDETECT = 0xDB
	SWITCHCAPVCC = 0x2
