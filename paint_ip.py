#!/usr/bin/python
import epd7in5
import Image
import ImageDraw
import ImageFont
from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6


EPD_WIDTH = 640
EPD_HEIGHT = 384

epd = epd7in5.EPD()
epd.init()

image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
draw = ImageDraw.Draw(image)
head_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 28)
body_text = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)

text_y = 10
head_buffer = 10
line_height = 20

def print_line(text, style):
  global text_y
  y_pos = text_y
  text_y = text_y + line_height
  font = body_text
  if style == "heading":
    text_y = text_y + head_buffer + line_height
    font = head_text
  draw.text((10, y_pos), text, font = font, fill = 0)

ip_list = []
for interface in interfaces():
  if interface != "lo":
    print_line(interface, "heading")
    for link in ifaddresses(interface).get(AF_INET, ()):
      ipv4 = "IPv4: " + link['addr']
      print_line(ipv4, "body")
    for link in ifaddresses(interface).get(AF_INET6, ()):
      ipv6 = "IPv6: " + link['addr']
      print_line(ipv6, "body")
    print_line("", "heading")

epd.display_frame(epd.get_frame_buffer(image))
