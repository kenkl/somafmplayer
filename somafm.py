#!/usr/bin/env python3

from flask import Flask,request
from volumecontroller import *
import subprocess, json

streams = {
    'DroneZone': 'https://somafm.com/dronezone256.pls', 
    'GrooveSalad': 'https://somafm.com/groovesalad256.pls',
    'GrooveSaladClassic': 'https://somafm.com/gsclassic130.pls',
    'n5MD': 'https://somafm.com/n5md130.pls',
    'DeepSpaceOne': 'https://somafm.com/deepspaceone130.pls',
    }

app = Flask(__name__)

@app.route('/')
def index():
    message = f"SomaFM player.\nCall with /play?stream=<StreamName>\nKnown Streams: {streamlistt()}\n"

    return message

@app.route('/dronezone')
def playdz():
    stopstream()
    startstream('DroneZone')
    return 'playing.\n'

@app.route('/stop')
def stop():
    stopstream()
    return 'stopped.\n'

@app.route('/play')
def play():
    call = request.args.get('stream', type=str)
    #print(call)
    #print(type(call))
    if not call == None:  # stream= has to exist
        if call in streams:
            stopstream()
            startstream(call)
            return f'playing from {streams[call]}\n'
        else:
            return f"Can't play:\nStream '{call}' is unknown.\n"
    else:
        return 'Syntax error. Call with:\n/play?stream=<StreamName>\n'

@app.route('/vol')
def fsetvol():  # the 'f' prefix avoids name collision with the volume module imported above
    level = request.args.get('level', type=int)
    if not level == None:  # level= has to exist
        setvol(level)
        return f'{level}\n'
    else:
        v = getvol()
        return f'{v}\n'

@app.route('/volup')
def fvolup():
    volup()
    return f'volup {step}\n'

@app.route('/voldown')
def fvoldown():
    voldown()
    return f'voldown {step}\n'

@app.route('/togmute')
def fmute():
    setmute(not getmute())
    return 'mute toggle\n'

@app.route('/streamlist')
def streamlist():
    l  = app.make_response(json.dumps(streams))
    l.mimetype = 'application/json'
    return l


def startstream(streamname):
    command = f'nohup mplayer -quiet -playlist {streams[streamname]} &'
    subprocess.call(command, shell=True)

def stopstream():
    '''Stop whatever mplayer stream is running'''
    subprocess.call('pkill mplayer', shell=True)
    subprocess.call('>nohup.out', shell=True)

def streamlistt():
    '''Simply returns a formatted list of known streams'''
    streamnames=''
    for key in streams.keys():
        streamnames += key + ', '

    return streamnames
    

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=False)


