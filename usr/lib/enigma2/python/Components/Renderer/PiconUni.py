# -*- coding: utf-8 -*-
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import SCOPE_CURRENT_SKIN, resolveFilename, SCOPE_PLUGINS
import os

class PiconUni(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.path = 'piconUni'
		self.scale = '0'
		self.nameCache = {}
		self.pngname = ''

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if not self.instance: return
		pngname = ''
		if what[0] != self.CHANGED_CLEAR:
			sname = self.source.text or ""
			# Python 3: Remove degree symbol using unicode literal
			sname = sname.upper().replace('.', '').replace('°', '')
			if not sname.startswith('1'):
				sname = sname.replace('4097', '1', 1).replace('5001', '1', 1).replace('5002', '1', 1)
			if ':' in sname:
				sname = '_'.join(sname.split(':')[:10])
			pngname = self.nameCache.get(sname, '')
			if not pngname:
				pngname = self.findPicon(sname)
				if pngname:
					self.nameCache[sname] = pngname
		if not pngname:
			pngname = self.nameCache.get('default', self.findPicon('picon_default'))
			if not pngname:
				tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
				if os.path.isfile(tmp): pngname = tmp
			self.nameCache['default'] = pngname
		
		if self.pngname != pngname:
			if pngname:
				if self.scale == '0': self.instance.setScale(1)
				self.instance.setPixmapFromFile(pngname)
				self.instance.show()
			else:
				self.instance.hide()
			self.pngname = pngname

	def findPicon(self, serviceName):
		for path in searchPaths:
			for dirName in self.path.split(','):
				pngname = (path % dirName) + serviceName + '.png'
				if os.path.isfile(pngname): return pngname
		return ''

searchPaths = []
def initPiconPaths():
	if os.path.isfile('/proc/mounts'):
		with open('/proc/mounts', 'r') as f:
			for line in f:
				if any(x in line for x in ('/dev/sd', '/dev/disk/by-uuid/', '/dev/mmc')):
					searchPaths.append(line.split()[1].replace('\\040', ' ') + '/%s/')
	searchPaths.append('/usr/share/enigma2/%s/')
	searchPaths.append(resolveFilename(SCOPE_PLUGINS, '%s/'))
initPiconPaths()