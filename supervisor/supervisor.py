# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import smbus2
import bme280

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Setup the 128x32 OLED screen via I2C
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# init canvas
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

# BM280 init
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# First define some constants to allow easy resizing of shapes.
padding = 0
top = 0

# Load fonts
font = ImageFont.load_default()
bigFontSize = 20
bigFont = ImageFont.truetype('zrnic.ttf', bigFontSize)

while True:
    top = 0
    
    # Sample environment
    data = bme280.sample(bus, address, calibration_params)

    # clear the canvas
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I"
    IP = subprocess.check_output(cmd, shell = True )
    IP = IP.decode('utf-8').strip()
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    #cmd = "free -m | awk 'NR==2{printf \"%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    cmd = "free -m | awk 'NR==2{printf \"%s/%sMB\", $3,$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    MemUsage = MemUsage.decode('utf-8')
    #cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    #Disk = subprocess.check_output(cmd, shell = True )
    Temp = str(round(data.temperature, 1)) + '°C ' + \
    str(round(data.humidity,1)) + '%'

    # Write two lines of text.
    (topWidth, topHeight) = bigFont.getsize(Temp)
    left = (width - topWidth)/2
    draw.text((left, top), Temp, font=bigFont, fill=255)
    top += bigFontSize + padding
    draw.text((0, top),    str(IP) + ' ' + MemUsage, font=font, fill=255)
    #draw.text((x, top+24),str(CPU) + '% | '+ \
    #str(MemUsage),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)

