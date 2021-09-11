import board
import digitalio
import pwmio
import time
import usb_midi
import adafruit_midi
import analogio

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

print("MacroPad MIDI Board")
adc0 = analogio.AnalogIn(board.A0)
adc1 = analogio.AnalogIn(board.A1)
adc2 = analogio.AnalogIn(board.A2)

def getMidiInput():
    pad = [0, 0, 0]
    raw0 = adc0.value
    raw1 = adc1.value
    raw2 = adc2.value

    #pad[0] = int(raw0/37)-21
    #pad[1] = int(raw1/80)-20
    #pad[2] = int(raw2/47)-20

    pad[0] = int(raw0/24)-53
    pad[1] = int(raw1/65)-55
    pad[2] = int(raw2/25)-51

    if pad[0] < 0:
        pad[0] = 0
    if pad[0] > 127:
        pad[0] = 127

    if pad[1] < 0:
        pad[1] = 0
    if pad[1] > 127:
        pad[1] = 127

    if pad[2] < 0:
        pad[2] = 0
    if pad[2] > 127:
        pad[2] = 127

    if pad[0] or pad[1] or pad[2]:
        if pad[1] > pad[0] and pad[1] > pad[2]:
            pad[0] = 0
            pad[2] = 0
        elif pad[2] > pad[1] and pad[2] > pad[0]:
            pad[1] = 0
            pad[0] = 0
        else:
            pad[2] = 0
            pad[1] = 0

    for note in pad:
        if note:
            print(str(pad[0]) + "\t" + str(pad[1]) + "\t" + str(pad[2]))
            #print("-----------")

    time.sleep(0.05)

    return pad


                            # Sound setup routine...
pads = [60,62,64]              # Keeps the pad midi code #s
padCount = 0
while (padCount < 3):
    pad = [0, 0, 0]
    enterKey = 3

    print("Tap pad 0 to play current note, pad 2 to up the note, pad 1 to down the note. Hit hard (velocity 127) to save each pad...")
    key = 60
    while pad[0] < 127 and pad[1] < 127 and pad[2] < 127:

        pad = getMidiInput()

        if pad[0] or pad[1] or pad[2]:

            if pad[2]:
                key += 1
                print('up to ' + str(key))
            if pad[1]:
                key -= 1
                print('down to ' + str(key))

            if key < 1:
                key = 1
            if key >127:
                key = 127

            if pad[0]:
                enterKey -= 1
                if enterKey < 1:
                    pad[0] = 127
                    enterKey = 3

            print("key = " + str(key))
#
            midi.send([NoteOn(key, 100)])
            midi.send([NoteOff(key, 100)])
        #time.sleep(0.1)

    time.sleep(0.5)
    midi.send([NoteOn(key, 100)])   # Dah
    time.sleep(0.5)
    midi.send([NoteOff(key, 100)])
    midi.send([NoteOn(key, 100)])   # Di
    time.sleep(0.25)
    midi.send([NoteOff(key, 100)])
    midi.send([NoteOn(key, 100)])   # Di
    time.sleep(0.25)
    midi.send([NoteOff(key, 100)])
    midi.send([NoteOn(key, 100)])   # Dah
    time.sleep(0.5)
    midi.send([NoteOff(key, 100)])
    midi.send([NoteOn(key, 100)])   # Dah
    time.sleep(0.5)
    midi.send([NoteOff(key, 100)])


    pads[padCount] = key
    print("Saved key " + str(padCount))
    padCount += 1


while True:

    pad0, pad1, pad2 = getMidiInput()

    if pad0:
        midi.send([NoteOn(pads[0], pad0)])
        #print("pad0")
        #time.sleep(0.01)
        midi.send([NoteOff(pads[0], pad0)])

    if pad1:
        midi.send([NoteOn(pads[1], pad1)])
        #print("pad1")
        #time.sleep(0.01)
        midi.send([NoteOff(pads[1], pad1)])

    if pad2:
        midi.send([NoteOn(pads[2], pad2)])
        #print("pad2")
        #time.sleep(0.01)
        midi.send([NoteOff(pads[2], pad2)])


    #time.sleep(0.01)