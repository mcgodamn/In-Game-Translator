import pyhk
from PIL import ImageGrab,Image,ImageTk
import sys
import pyocr
import pyocr.builders
import screenshot
import os
from azure_translator import Translator
import notify
import time
import thread
def detectStr(txt):
	for s in xrange(len(txt)):
		if txt[s]!=' ' and (txt[s]>'z' or txt[s]<'a'):
			if(txt[s]>'9' or txt[s]<'0'):
				return False
	return True
def shutdown():
	time.sleep(5)
	notify.draw('')
def translate(pic):
	tools = pyocr.get_available_tools()
	if len(tools) == 0:
		print("No OCR tool found")
		sys.exit(1)
	tool = tools[0]
	langs = tool.get_available_languages()
	lang = langs[0]
	txt = tool.image_to_string(
		pic,
		lang=lang,
		builder=pyocr.builders.TextBuilder()
	)
	os.remove('temp.png')
	txt = txt.lower()
	print txt
	if (txt == '') or detectStr(txt):
		txt = 'Wrong input,please do it again'
	else:
		t = Translator('a0e476a37adb4c20be2aef398e288181')
		s = t.translate(txt, to="zh-CHT")
		print s
		txt = txt + ' ' + s
	thread.start_new_thread(shutdown,())
	notify.draw(txt)
def capture():
	screenshot.ini()
	image = 0
	while not image:
		image = Image.open('temp.png')
	translate(image)
def main():
	hot = pyhk.pyhk()
	hot.addHotkey(['~', '1'], capture)  
	hot.start()
if __name__ == "__main__":
	main()