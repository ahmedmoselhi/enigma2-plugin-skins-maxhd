# -*- coding: utf-8 -*-
from Components.config import config
from Components.Renderer.Renderer import Renderer
from enigma import eLabel, eTimer
from Components.VariableText import VariableText

class RollerCharLCD(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.moveTimerText = eTimer()
		self.moveTimerText_conn = self.moveTimerText.timeout.connect(self.moveTimerTextRun)
		self.delayTimer = eTimer()
		self.delayTimer_conn = self.delayTimer.timeout.connect(self.delayTimergo)
		self.stringlength = 12

	GUI_WIDGET = eLabel

	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			self.moveTimerText.stop()
			self.delayTimer.stop()
			self.text = ''
		else:
			self.text = self.source.text
		
		if self.text and len(self.text) > self.stringlength:
			self.text = self.source.text + ' ' * self.stringlength + self.source.text[:self.stringlength + 1]
			self.x = len(self.text) - self.stringlength
			self.idx = 0
			self.backtext = self.text
			self.status = 'start'
			self.moveTimerText.start(2000)
		elif self.text:
			self.x = len(self.text)
			self.idx = 0
			self.backtext = self.text

	def moveTimerTextRun(self):
		self.moveTimerText.stop()
		if self.x > 0:
			txttmp = self.backtext[self.idx:]
			self.text = txttmp[:self.stringlength]
			str_length = 1
			# Unicode handles for Python 3 (ü, ä, ö, ß, etc.)
			accents = ('ü', 'ä', 'ö', 'Ä', 'Ü', 'Ö', 'ß')
			if self.text.startswith(accents):
				str_length = 1 # Python 3 strings are unicode, length is 1 even for accents
			self.idx += str_length
			self.x -= str_length
		if self.x == 0:
			self.status = 'end'
			self.text = self.backtext
		if self.status != 'end':
			self.moveTimerText.start(int(config.lcd.scroll_speed.value))
		if config.lcd.scroll_delay.value != 'noscrolling':
			self.delayTimer.start(int(config.lcd.scroll_delay.value))

	def delayTimergo(self):
		self.delayTimer.stop()
		self.changed((self.CHANGED_DEFAULT,))