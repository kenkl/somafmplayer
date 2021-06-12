#!/usr/bin/env python3

from flask import Flask,request
from volumecontroller import *
import subprocess, json, requests

URL = "https://somafm.com/channels.json"
cl = []  # our simplified channel list

app = Flask(__name__)

@app.route('/')
def index():
    message = f"SomaFM player.\nCall with /play?stream=<streamid>\n"

    return message

@app.route('/stop')
def stop():
    stopstream()
    return 'stopped.\n'

@app.route('/play')
def play():
    call = request.args.get('stream', type=str)
    if not call == None:  # stream= has to exist
        url = get_url(call)
        if not url == 'HONK':  # validate that we know about the streamid passed; don't try to play something unknown
            stopstream()
            startstream(url)
            return f'playing from {url}\n'
        else:
            return f"Can't play:\nStream '{call}' is unknown.\n"
    else:
        return 'Syntax error. Call with:\n/play?stream=<streamid>\n'

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
    return f'{getvol()}\n'

@app.route('/voldown')
def fvoldown():
    voldown()
    return f'{getvol()}\n'

@app.route('/togmute')
def fmute():
    setmute(not getmute())
    return 'mute toggle\n'

@app.route('/streamlist')
def streamlist():
    l  = app.make_response(json.dumps(cl))
    l.mimetype = 'application/json'
    return l

def startstream(url):
    command = f'nohup mplayer -quiet -playlist {url} &'
    subprocess.call(command, shell=True)

def stopstream():
    '''Stop whatever mplayer stream is running'''
    subprocess.call('pkill mplayer', shell=True)
    subprocess.call('>nohup.out', shell=True)

def make_cl():
    global cl
    c_raw = requests.get(URL)
    c_raw.raise_for_status()

    channels = json.loads(c_raw.text)
    clist = channels['channels']

    for i in clist:
        c={'id': i['id'], 'title': i['title'], 'description': i['description'], 'playlist': i['playlists'][0]['url']}
        cl.append(c)

def get_url(streamid):
    for i in range(len(cl)):
        if cl[i]['id'] == streamid:
            return cl[i]['playlist']
    return 'HONK'

    

if __name__ == '__main__':
    #app.run(debug=True)
    subprocess.call('>nohup.out', shell=True)
    make_cl()
    app.run(host='0.0.0.0', port=5000, debug=False)


