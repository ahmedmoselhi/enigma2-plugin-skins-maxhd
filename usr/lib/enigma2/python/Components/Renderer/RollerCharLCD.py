# coded by shamann

from Renderer import Renderer
from enigma import eLabel
from enigma import eTimer
from Components.VariableText import VariableText

class RollerCharLCD(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			self.text = ""
		else:
			self.text = self.source.text
		if self.instance:
			if len(self.text) > 17:
				self.x = len(self.text) - 5
				self.idx = 0
				self.backtext = self.text
				self.status = "start" 
				self.moveTimerText = eTimer()
				self.moveTimerText.timeout.get().append(self.moveTimerTextRun)
				self.moveTimerText.start(2000)

	def moveTimerTextRun(self):
		self.moveTimerText.stop()
		if self.x > 0:
			txttmp = self.backtext[self.idx:]
			self.text = txttmp[:30]
			self.idx = self.idx+1
			self.x = self.x-1      
		if self.x == 0: 
			self.status = "end"     
			self.text = self.backtext
			if len(self.text) > 5:
				self.text = self.text[:30] + "..."
		if self.status != "end":
			self.moveTimerText.start(350)

