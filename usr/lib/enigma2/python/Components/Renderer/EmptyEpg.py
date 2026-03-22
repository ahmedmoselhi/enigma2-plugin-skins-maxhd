#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2011
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################

from Renderer import Renderer
from enigma import eLabel, eTimer
from Components.VariableText import VariableText
from Components.config import config

class EmptyEpg(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.EmptyText = ""
		self.fillTimer = eTimer()
		self.fillTimer.timeout.get().append(self.__fillText)
		self.backText = ""

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				self.sizeX = int(value.strip().split(",")[0])
				attribs.append((attrib,value))
			elif attrib == "emptyText":
				self.EmptyText = value
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
			if self.instance and self.backText != self.text:
				if self.text == "":
					self.text = self.EmptyText
				text_width = self.instance.calculateSize().width()
				if text_width > self.sizeX:
					while (text_width > self.sizeX):
						self.text = self.text[:-1] 
						text_width = self.instance.calculateSize().width()
					self.text = self.text[:-3] + "..."
				if self.backText != self.text:
					self.backText = self.text					
					ena = True
					try: ena = config.plugins.setupGlass16.par30.value
					except: pass
					if ena:
						self.text = "_"				
						self.endPoint = len(self.backText)
						self.posIdx = 0                    
						if self.fillTimer.isActive():
							self.fillTimer.stop()
						self.fillTimer.start(1300, True) 					
					
	def __fillText(self):
		self.fillTimer.stop()
		self.posIdx += 1
		if self.posIdx <= self.endPoint:
			self.text = self.backText[:self.posIdx] + "_"
			self.fillTimer.start(50, True)
		else:
			self.text = self.backText 					
					
