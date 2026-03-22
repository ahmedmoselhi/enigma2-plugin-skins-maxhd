# Happy2000
#
#
#######################################################################
#                      mod.Zombi (c)2012
#######################################################################

from Components.VariableText import VariableText
from Renderer import Renderer
from enigma import ePoint, eTimer

from enigma import eLabel

class LcdRoller2(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "position":
				self.posY = int(value.strip().split(",")[1])
				attribs.append((attrib,value))
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
			
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			self.text = ""
		else:
			self.text = self.source.text
			if (self.instance):       
				self.c = len(self.text) # bereken hoelang de tekst is characters
				self.a = self.c
				self.c = self.c * 18    # vermenigvuldig de tekst om pixels te krijgen
				self.x2 = self.c /5     # deelt de totale aantal pixels van de tekst door 8 +/-(helft van font="16") voor als de tekst niet scrolt
				self.c = ((self.c /2) + (175)) # deelt de lengte ( pixels) tekst door 4 en tel er 175 bij op.
				self.x = 135            # start pixel x  van de scrollende tekst
				self.y = 0              # Y positie van de tekst
				self.instance.move(ePoint(150,self.posY)) # reset de tekst naar x 150 (buiten het display)
				self.moveTimerText = eTimer()
				self.moveTimerText.timeout.get().append(self.moveTimerTextRun)
				self.moveTimerText.start(1800)
				      	

	def moveTimerTextRun(self):
		self.moveTimerText.stop()
		if (self.a > 13):           # Als de tekst op het display meer dan 14 tekens bevat, dan gaan scrollen
			self.instance.move(ePoint(self.x,self.posY))
			self.x -=1
			self.c -=1
		elif (self.a > 0):          # Als de niet mag scrollen en de tekst bevat meer dan 0 tekens dan tekst stil laten staan
			for d in self.text:       # Kijk in de tekst als er spaties zijn
				if d == " ":
					self.x2 +=2           # Als er een spatie is tel 5 pixels bij de tekst op
			self.x2 = 60 - self.x2    # zet dan de begin positie van de tekst op deze berekening (midden lcd scherm)
			self.a = 0
			self.instance.move(ePoint(self.x2,self.posY)) # zet de vaste tekst hier neer self.p self.y
		if self.c == 1:
			self.changed((self.CHANGED_DEFAULT,))
		self.moveTimerText.start(50)

