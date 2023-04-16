import pyttsx3
from gtts import gTTS
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
import os
from pydub import AudioSegment
from pydub.playback import play

#default settings
engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
volume = engine.getProperty('volume')
engine.setProperty('volume',1) 

echo=False
breaker=False

#functions
def speedchange(args):
   engine.setProperty('rate', args[0])
   print(f"The current WPM rate is now {args[0]}.")

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

#dict for functions
fn_lookup = {
   'sc': speedchange,
   'reverb': reverb,
   'end': stopscript,
   'help': help
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
         engine.save_to_file(speak, 'speak.wav')
         engine.runAndWait()
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
         play(AudioSegment.from_file('speak.wav'))
         #delete
         #os.remove('speak.wav')
      elif echo==False:
         engine.say(speak)
         engine.runAndWait()