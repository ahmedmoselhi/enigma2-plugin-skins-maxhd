# 2013.06.29 21:16:37 Arab Standard Time
#Embedded file name: /usr/lib/enigma2/python/Components/Renderer/eXcPicon.py
from Renderer import Renderer
from enigma import ePixmap, eEnv, ePicLoad
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename

class eXcPicon(Renderer):
    searchPaths = (eEnv.resolve('${datadir}/enigma2/%s/'),
     '/media/cf/%s/',
     '/media/usb/%s/',
     '/media/ba/%s/',
     '/media/hdd/%s/')

    def __init__(self):
        Renderer.__init__(self)
        self.path = 'picon'
        self.nameCache = {}
        self.pngname = ''

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if self.instance:
            pngname = ''
            if what[0] != self.CHANGED_CLEAR:
                sname = self.source.text
                pos = sname.rfind(':')
                if pos != -1:
                    sname = sname[:pos].rstrip(':').replace(':', '_')
                pngname = self.nameCache.get(sname, '')
                if pngname == '':
                    pngname = self.findPicon(sname)
                    if pngname != '':
                        self.nameCache[sname] = pngname
            if pngname == '':
                pngname = self.nameCache.get('default', '')
                if pngname == '':
                    pngname = self.findPicon('picon_default')
                    if pngname == '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                        if fileExists(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                    self.nameCache['default'] = pngname
            if self.pngname != pngname:
                self.picload = ePicLoad()
                self.picload.PictureData.get().append(self.piconShow)
                self.picload.setPara((self.instance.size().width(),
                 self.instance.size().height(),
                 1,
                 1,
                 False,
                 1,
                 '#00000000'))
                self.picload.startDecode(pngname)
                self.pngname = pngname

    def piconShow(self, picInfo = None):
        ptr = self.picload.getData()
        if ptr != None:
            self.instance.setPixmap(ptr.__deref__())
        return

    def findPicon(self, serviceName):
        for path in self.searchPaths:
            pngname = path % self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname

        return ''
# okay decompyling eXcPicon.pyo 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.06.29 21:16:37 Arab Standard Time
