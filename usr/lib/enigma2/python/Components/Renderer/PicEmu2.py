# -*- coding: utf-8 -*-
from Components.Renderer.Renderer import Renderer
from enigma import iServiceInformation, ePixmap
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, resolveFilename
from Components.Element import cached
from Components.Converter.Poll import Poll
import os

class PicEmu2(Renderer, Poll):
	__module__ = __name__
	if os.path.exists("/usr/lib64"):
		searchPaths = ('/data/%s/', '/usr/share/enigma2/%s/', '/usr/lib64/enigma2/python/Plugins/Extensions/%s/', '/media/sde1/%s/', '/media/cf/%s/', '/media/sdd1/%s/', '/media/hdd/%s/', '/media/usb/%s/', '/media/ba/%s/', '/mnt/ba/%s/', '/media/sda/%s/', '/etc/%s/')
	else:
		searchPaths = ('/data/%s/', '/usr/share/enigma2/%s/', '/usr/lib/enigma2/python/Plugins/Extensions/%s/', '/media/sde1/%s/', '/media/cf/%s/', '/media/sdd1/%s/', '/media/hdd/%s/', '/media/usb/%s/', '/media/ba/%s/', '/mnt/ba/%s/', '/media/sda/%s/', '/etc/%s/')

	def __init__(self):
		Poll.__init__(self)
		Renderer.__init__(self)
		self.path = 'emu'
		self.nameCache = {}
		self.pngname = ''
		self.picon_default = "picon_default.png"

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
			elif attrib == 'picon_default':
				self.picon_default = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not service:
			return ""
		nameemu = []
		nameser = []
		if not info:
			return ""
		if fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			try:
				if fileExists("/etc/init.d/softcam"):
					with open("/etc/init.d/softcam", "r") as f:
						for line in f:
							if "echo" in line:
								nameemu.append(line)
					camdlist = nameemu[1].split('"')[1] if len(nameemu) > 1 else None
				else:
					camdlist = None
			except:
				camdlist = None
			try:
				if fileExists("/etc/init.d/cardserver"):
					with open("/etc/init.d/cardserver", "r") as f:
						for line in f:
							if "echo" in line:
								nameser.append(line)
					serlist = nameser[1].split('"')[1] if len(nameser) > 1 else None
				else:
					serlist = None
			except:
				serlist = None
			if serlist and camdlist:
				return f"{serlist} {camdlist}"
			elif camdlist:
				return camdlist
			elif serlist:
				return serlist
		return ""

	text = property(getText)

	def changed(self, what):
		self.poll_interval = 50
		self.poll_enabled = True
		if self.instance:
			pngname = ''
			if what[0] != self.CHANGED_CLEAR:
				sname = ""
				service = self.source.service
				if service:
					info = service.info()
					if info:
						caids = info.getInfoObject(iServiceInformation.sCAIDs)
						if fileExists("/tmp/ecm.info"):
							try:
								value = self.getText().lower()
								if not value:
									sname = "fta"
								else:
									with open("/tmp/ecm.info", "r") as f:
										content = f.read()
									if "address" in content:
										sname = "cccam"
							except:
								pass
						if caids and not sname:
							for caid in caids:
								caid_str = self.int2hex(caid).upper().zfill(4)[:2]
								if caid_str:
									sname = "fta"
									break
				pngname = self.nameCache.get(sname, '')
				if not pngname:
					pngname = self.findPicon(sname)
					if pngname:
						self.nameCache[sname] = pngname
			if not pngname:
				pngname = self.nameCache.get('fta', '')
				if not pngname:
					pngname = self.findPicon('fta')
					if not pngname:
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
						if fileExists(tmp):
							pngname = tmp
						self.nameCache['default'] = pngname
			if self.pngname != pngname:
				self.pngname = pngname
				self.instance.setPixmapFromFile(self.pngname)

	def int2hex(self, val):
		return "%x" % val

	def findPicon(self, serviceName):
		for path in self.searchPaths:
			pngname = (path % self.path) + serviceName + '.png'
			if fileExists(pngname):
				return pngname
		return ''