#!/usr/bin/env python3

import alsaaudio

step = 5 #volup/voldown step increment

devices = alsaaudio.cards()
idx = devices.index('IQaudIODAC')
mixers=alsaaudio.mixers(idx)
mixeridx = mixers.index('Digital')
mixer = alsaaudio.Mixer(mixers[int(mixeridx)], cardindex=idx)

def getvol():
    v = mixer.getvolume()
    return v[0]

def setvol(v):
    if v >= 0 and v <=100:
        mixer.setvolume(v)
    
def getmute():
    m = mixer.getmute()
    return m[0]

def setmute(mute=False):
    mixer.setmute(mute)

def volup():
    v = getvol()
    v += step
    if v > 100:
        v = 100
    setvol(v)

def voldown():
    v = getvol()
    v -= step
    if v < 0:
        v = 0
    setvol(v)
    



if __name__ == "__main__":
    print("Do things with IQAudio board")


