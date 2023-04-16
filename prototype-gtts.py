from gtts import gTTS
from gtts import lang
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
import simpleaudio as sa
import subprocess

#default settings
echo=False
breaker=False
dial="en"
languages=lang.tts_langs()
accents="com"

#functions
def reverb(args):
    global echo
    echo=not echo
    print(f'Reverb is now {echo}.')

def stopscript(args):
    exit()

def help(args):
    print("Currently valid commands are:")
    for key in fn_lookup:
        print(r'/' + key, end=' ')
    print("\n")

def language(args):
    global dial
    try:
        dial=""
        for x in args:
            dial+=x
        print("The language is now " + languages[dial] + ".")
    except:
        dial="en"
        print("That is not a valid language.")

def langlist(args):
    global langauges
    for key,value in languages.items():
        print(key + '=' + value, end=' ')
    print('')

def accent(args):
    global accents
    print("co.uk or com.au or com")
    args=input()
    accents=args

#dict for functions
fn_lookup = {
    'reverb': reverb,
    'end': stopscript,
    'help': help,
    'lang': language,
    'll': langlist,
    'acc': accent
}

#TTS script here
while True:
    speak=str(input())
    #if it is valid input...
    if speak=='':
        print("Please try again.")
    #if it is a command...
    elif speak.startswith(r'/'):
        line=speak.strip(r'/')
        line=line.strip()
        cmd=line.split(' ')[0]
        args=line.split(' ')[1:]
        if cmd in fn_lookup:
            fn_lookup[cmd](args)
        else:
            print(f'{cmd} is not a valid command.')
    #if it is something to be said...
    else:
        if echo==True:
            #save as file
            tts = gTTS(speak, lang=dial, tld=accents)
            tts.save('speak.mp3')
            #CONVERT
            subprocess.call(['ffmpeg', '-i', 'speak.mp3', '-c', 'pcm_u8', '-y', 'speak.wav'], stderr=subprocess.DEVNULL)
            #reverb
            with AudioFile('speak.wav', 'r') as f:
                audio = f.read(f.frames)
                samplerate = f.samplerate
            open('speak.wav', 'w').close()
            board = Pedalboard([Reverb(room_size=1)])
            effected = board(audio, samplerate)
            with AudioFile('speak.wav', 'w', samplerate, effected.shape[0]) as f:
                f.write(effected)
            #play
            wave_obj = sa.WaveObject.from_wave_file("speak.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
        elif echo==False:
            tts = gTTS(speak, lang=dial, tld=accents)
            tts.save('speak.mp3')
            #CONVERT
            subprocess.call(['ffmpeg', '-i', 'speak.mp3', '-c', 'pcm_u8', '-y', 'speak.wav'], stderr=subprocess.DEVNULL)
            wave_obj = sa.WaveObject.from_wave_file("speak.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
