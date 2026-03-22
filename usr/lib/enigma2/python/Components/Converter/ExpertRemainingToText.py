#
#	Expert RemainingToText Converter
#	by Ismail Demir
#
#
#	Example usage in the skin.xml:
#
#		<widget source="session.Event_Now" render="Label" position="960,82" size="120,28" font="Regular;24" >
#			<convert type="EventTime">Remaining</convert>
# 			<convert type="ExpertRemainingToText">WithSeconds</convert>
#		</widget>
#
#######################################################

from Components.Converter.Converter import Converter
from Components.Element import cached

class ExpertRemainingToText(Converter, object):
	DEFAULT = 0
	WITH_SECONDS = 1
	IN_MINUTES = 2

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "WithSeconds":
			self.type = self.WITH_SECONDS
		elif type == "InMinutes":
			self.type = self.IN_MINUTES
		else:
			self.type = self.DEFAULT

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""

		(duration, remaining) = self.source.time

		if self.type == self.WITH_SECONDS:
			if remaining is not None:
				return "%02d:%02d:%02d" % (remaining / 3600, (remaining / 60) - ((remaining / 3600) * 60), remaining % 60)
			else:
				return "%02d:%02d:%02d" % (duration / 3600, (duration / 60) - ((duration / 3600) * 60), duration % 60)

		elif self.type == self.IN_MINUTES:
			if remaining is not None:
				return "%02d:%02d" % (remaining / 3600, (remaining / 60) - ((remaining / 3600) * 60))
			else:
				return "%02d:%02d" % (duration / 3600, (duration / 60) - ((duration / 3600) * 60))

		elif self.type == self.DEFAULT:
			if remaining is not None:
				return "+%d min" % (remaining / 60)
			else:
				return "%d min" % (duration / 60)

		else:
			return "???"
			
	text = property(getText)
