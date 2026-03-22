#######################################################################

#######################################################################

from Renderer import Renderer
from enigma import eLabel
from Components.VariableText import VariableText
from enigma import eServiceReference

class ais(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			if what[0] == self.CHANGED_CLEAR:
				self.text = "Reference not found !"
			else:
				service = self.source.service
				marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
				bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				sname = service.toString()
				if marker or bouquet:
					self.text = " Skin AIS_HD V2 "
				else:
					pos = sname.rfind(':')
					if pos != -1:
						sname = sname[:pos].rstrip(':')
						if not "::" in sname:
							self.text = "Ref: " + sname
						else:
							self.text = " Skin AIS_HD V2 "
					else:
						self.text = "Reference reading error !"
