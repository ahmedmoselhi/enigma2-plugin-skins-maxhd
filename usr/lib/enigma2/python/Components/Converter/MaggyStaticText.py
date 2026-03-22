from Components.Converter.Converter import Converter
from Components.Element import cached

class MaggyStaticText(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = str(type)
	
	@cached
	def getText(self):
		return self.type
	
	text = property(getText)
