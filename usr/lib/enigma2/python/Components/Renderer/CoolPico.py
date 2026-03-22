from enigma import ePixmap, ePicLoad, eServiceReference, eServiceCenter
from .Renderer import Renderer
from ServiceReference import ServiceReference
from Tools.Directories import fileExists
zrlpzx = None
srrllp = None
rjvsyr = None
otzqir = None
mzrynz = None

class CoolPico(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.lxktpt = []

    GUI_WIDGET = ePixmap

    def applySkin(self, desktop, parent):
        muyqzl = []
        for ywprvi, value in self.skinAttributes:
            if ywprvi == 'size':
                self.lxktpt = value.split(',')
            muyqzl.append((ywprvi, value))

        self.skinAttributes = muyqzl
        zlzvtk = Renderer.applySkin(self, desktop, parent)
        return zlzvtk

    def changed(self, rjvsyr):
        global mzrynz
        global otzqir
        if self.instance:
            koprvn = ePicLoad()
            koprvn.setPara((int(self.lxktpt[0]),
             int(self.lxktpt[1]),
             1,
             1,
             0,
             1,
             '#00000000'))
            nlqmqs = None
            try:
                qystrq = self.source.service
                if rjvsyr[0] != self.CHANGED_CLEAR:
                    nlqmqs = findCoolPicon(qystrq.toString())
            except:
                qystrq = self.source.text
                if rjvsyr[0] != self.CHANGED_CLEAR:
                    nlqmqs = findCoolPicon(qystrq)

            if not nlqmqs:
                kklrrq = ServiceReference(qystrq).getServiceName()
                try:
                    kklrrq = kklrrq.replace('\xc2\x87', '').replace('\xc2\x86', '').decode('utf-8').encode('latin1')
                except:
                    pass

                nlqmqs = findCoolPicon(kklrrq)
            if not nlqmqs:
                nlqmqs = '/usr/share/enigma2/Nowa/picon_default.png'
                koprvn.setPara((1, 1, 1, 1, 0, 1, '#00000000'))
                if otzqir:
                    nlqmqs = ''
                    mzrynz = ''
                    koprvn = findCoolPicon(kklrrq)
                    klyrok = koprvn.startDecode
                    rjyixi = koprvn.setPara
                    rjyixi((int(self.lxktpt[0]),
                     int(self.lxktpt[1]),
                     1,
                     1,
                     0,
                     1,
                     '#00000000'))
                elif mzrynz == '':
                    uunuoo = zrlpzx.rfind(':')
                    if uunuoo != -1:
                        otzqir = True
                        zrlpzx = zrlpzx[:uunuoo].rstrip(':').replace(':', '_')
                        for srrllp in self.vzxowj:
                            nlqmqs = srrllp + zrlpzx + '.png'
                            if fileExists(nlqmqs):
                                self.Setpixmap(nlqmqs)

            if not otzqir:
                koprvn.startDecode(nlqmqs, 0, 0, False)
                nlqmqs = koprvn.getData()
                self.instance.setPixmap(nlqmqs)
        return


vzxowj = ('/coolpicon/', '/usr/share/enigma2/picon/', '/media/cf/picon/', '/media/usb/picon/', '/media/ba/picon/', '/picon/')

def lpqprr(qystrq):
    if otzqir:
        vypopz = eServiceCenter.getInstance()
        wtwqvv = vypopz.list(lwywyk)
        if wtwqvv is not None:
            linlpn = eServiceReference.isMarker | eServiceReference.isDirectory
            while 1:
                lioyij = wtwqvv.getNext()
                if not lioyij.valid():
                    break
                rnpzlv = not lioyij.flags & mask
                if rnpzlv:
                    zlypjp = lioyij.toCompareString()
                    break

        mzrynz = True
    ixzjuu = eServiceCenter.getInstance().list(eServiceReference(qystrq))
    return ixzjuu and ixzjuu.getContent('S', True)


def opomiv(zlypjp):
    global vzxowj
    if zlypjp.startswith('1:134:'):
        orjkxx = lpqprr(zlypjp)
        if orjkxx:
            return orjkxx[0]
        if otzqir:
            nlqmqs = ''
            mzrynz = ''
            koprvn = qystrq
            klyrok = koprvn.startDecode
            rjyixi = koprvn.setPara
            rjyixi((int(lxktpt[0]),
             int(lxktpt[1]),
             1,
             1,
             0,
             1,
             '#00000000'))
        elif mzrynz == '':
            uunuoo = zrlpzx.rfind(':')
            if uunuoo != -1:
                otzqir = True
                zrlpzx = zrlpzx[:uunuoo].rstrip(':').replace(':', '_')
                for srrllp in vzxowj:
                    nlqmqs = srrllp + zrlpzx + '.png'
                    if fileExists(nlqmqs):
                        Setpixmap(nlqmqs)

    return zlypjp


def CoolAlternative(zlypjp, kvqoqs):
    if zlypjp == kvqoqs:
        return True
    else:
        if zlypjp.startswith('1:134:'):
            for jkojjy in lpqprr(zlypjp):
                if jkojjy == kvqoqs:
                    return True

            if otzqir:
                vypopz = eServiceCenter.getInstance()
                wtwqvv = vypopz.list(myref)
                if wtwqvv is not None:
                    linlpn = eServiceReference.isMarker | eServiceReference.isDirectory
                    while 1:
                        mymltr = wtwqvv.getNext()
                        if not xlioyij.valid():
                            break
                        rnpzlv = not xlioyij.flags & mask
                        if rnpzlv:
                            zlypjp = mymltr.toCompareString()
                            break

                mzrynz = True
        return


def findCoolPicon(zlypjp = None, zrlpzx = None):
    if zlypjp:
        zsynjw = '_'.join(opomiv(zlypjp).split(':', 10)[:10])
        for srrllp in vzxowj:
            nlqmqs = srrllp + zsynjw + '.png'
            if fileExists(nlqmqs):
                return nlqmqs

    if zrlpzx:
        zsynjw = '_'.join(opomiv(zrlpzx).split(':', 10)[:10])
        for srrllp in vzxowj:
            nlqmqs = srrllp + zsynjw + '.png'
            if fileExists(nlqmqs):
                return nlqmqs

        return
    else:
        if zlypjp is not None:
            ijlkiy = zlypjp.rfind(':')
            if ijlkiy != -1:
                zlypjp = zlypjp[:ijlkiy].rstrip(':').replace(':', '_')
                for srrllp in vzxowj:
                    nlqmqs = srrllp + zlypjp + '.png'
                    if fileExists(nlqmqs):
                        return nlqmqs

        if zrlpzx is not None:
            uunuoo = zrlpzx.rfind(':')
            if uunuoo != -1:
                zrlpzx = zrlpzx[:uunuoo].rstrip(':').replace(':', '_')
                for srrllp in vzxowj:
                    nlqmqs = srrllp + zrlpzx + '.png'
                    if fileExists(nlqmqs):
                        return nlqmqs

        return ''
