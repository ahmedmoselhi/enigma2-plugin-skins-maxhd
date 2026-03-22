# -*- coding: utf-8 -*-
from Components.VariableText import VariableText
from Renderer import Renderer

from enigma import eLabel
from skin import parseColor

class gMultiColorLabel(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.foreColors = []
		self.backColors = []
		self.__get_value = False
		self.__text = False

	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			if self.instance:
				self.instance.hide()
		else:
			if self.instance:
				if  self.__get_value:
					self.setBackgroundColorNum(self.source.get_value)
				if  self.__text:
					self.text = self.source.text
				self.instance.show()
		
	def applySkin(self, desktop, screen):
		if self.skinAttributes:
			attribs = [ ]
			for (attrib, value) in self.skinAttributes:
				if attrib == "backgroundColors":
					for color in value.split(','):
						self.backColors.append(parseColor(color))
				elif attrib == "foregroundColors":
					for color in value.split(','):
						self.foreColors.append(parseColor(color))
				else:
					attribs.append((attrib,value))
			self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, screen)
	
	def setForegroundColorNum(self, x):
		if self.instance:
			if len(self.foreColors) > x:
				self.instance.setForegroundColor(self.foreColors[x])
				self.instance.invalidate()
			else:
				print "setForegroundColorNum failed!",x
	
	def setBackgroundColorNum(self, x):
		if self.instance:
			if len(self.backColors) > x:
				self.instance.setBackgroundColor(self.backColors[x])
				self.instance.invalidate()
			else:
				print "setBackgroundColorNum failed!",x

	def postWidgetCreate(self, instance):
		self.__text = getattr(self.source, "text", None) != None and True
		self.__get_value = getattr(self.source, "get_value", None) != None and True
		instance.hide()
		