# edited by helour and shamann
import os
from .Converter import Converter
from time import localtime, strftime
from Components.Element import cached
from Components.Language import language


class g16ClockToText(Converter, object):
	DEFAULT = 0
	WITH_SECONDS = 1
	IN_MINUTES = 2
	DATE = 3
	FORMAT = 4
	AS_LENGTH = 5
	TIMESTAMP = 6

	def readLocaleStrings(self):
		self.lcMonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		if os.path.isfile('/etc/lcstrings.list') is True:
			myfile = open('/etc/lcstrings.list', 'r')
			lang = language.getActiveLanguage()
			for line in myfile.readlines():
				if line.startswith(lang):
					line = line.strip().split(":")[1]
					self.lcMonths = line.strip().split(',')
					break
			myfile.close()

	def toLocale(self, s):
		WeekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		for index, weekday in enumerate(WeekDays): 
			if s.find(weekday) >= 0:
				s = s.replace(weekday, _(weekday))
				break
		for index, month in enumerate(Months): 
			if s.find(month) >= 0:
				#s = s.replace(month, _(month))
				s = s.replace(month, self.lcMonths[index])		
				break
		return s

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "WithSeconds":
			self.type = self.WITH_SECONDS
		elif type == "InMinutes":
			self.type = self.IN_MINUTES
		elif type == "Date":
			self.type = self.DATE
		elif type == "AsLength":
			self.type = self.AS_LENGTH
		elif type == "Timestamp":	
			self.type = self.TIMESTAMP
		elif str(type).find("Format:") != -1:
			self.type = self.FORMAT
			self.fmt_string = type[7:]
		else:
			self.type = self.DEFAULT
		self.readLocaleStrings()

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""

		# handle durations
		if self.type == self.IN_MINUTES:
			return "%d min" % (time / 60)
		elif self.type == self.AS_LENGTH:
			return "%d:%02d" % (time / 60, time % 60)
		elif self.type == self.TIMESTAMP:
			return str(time)
		
		t = localtime(time)
		
		if self.type == self.WITH_SECONDS:
			return "%2d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
		elif self.type == self.DEFAULT:
			return "%2d:%02d" % (t.tm_hour, t.tm_min)
		elif self.type == self.DATE:
			return self.toLocale(strftime("%A %B %d, %Y", t))
		elif self.type == self.FORMAT:
			spos = self.fmt_string.find('%')
			if spos > 0:
				s1 = self.fmt_string[:spos]
				s2 = strftime(self.fmt_string[spos:], t)
				if self.fmt_string[spos:].startswith("%H") and s2[0] == "0" and s2[1] != ":":
					s2 = s2[1:]
				return self.toLocale(str(s1+s2))
			else:
				s = strftime(self.fmt_string, t)
				if self.fmt_string.startswith("%H") and s[0] == "0" and s[1] != ":": 
					s = s[1:]
				return self.toLocale(s)
		else:
			return "???"

	text = property(getText)
