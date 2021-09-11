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

stop = 0
key = 20
while (stop == 0):
    print("Enter 'a' to up the note, 'z' to down the note 'q' to exit ...")
    keyB = input()
    print(stop)
    if keyB == 'a':
        key += 1
        print('up to ' + str(key))
    if keyB == 'z':
        key -= 1
        print('down to ' + str(key))
    if keyB == 'q':
        stop = 1
    if key < 1:
        key = 1
    if key >127:
        key = 127

    midi.send([NoteOn(key, 127)])
    #print("pad2")
    #time.sleep(0.01)
    midi.send([NoteOff(key, 127)])
    #time.sleep(1)

while True:

    raw0 = adc0.value
    raw1 = adc1.value
    raw2 = adc2.value

    pad0 = int(raw0/24)-53
    pad1 = int(raw1/65)-63
    pad2 = int(raw2/25)-51

    if pad0 < 0:
        pad0 = 0
    if pad0 > 127:
        pad0 = 127

    if pad1 < 0:
        pad1 = 0
    if pad1 > 127:
        pad1 = 127

    if pad2 < 0:
        pad2 = 0
    if pad2 > 127:
        pad2 = 127

    if pad0 or pad1 or pad2:
        if pad1 > pad0 and pad1 > pad2:
            pad0 = 0
            pad2 = 0
        elif pad2 > pad1 and pad2 > pad0:
            pad1 = 0
            pad0 = 0
        else:
            pad2 = 0
            pad1 = 0
        #print(pad0, "\t", pad1, "\t", pad2)

    if pad0:
        midi.send([NoteOn(62, pad0)])
        #print("pad0")
        #time.sleep(0.01)
        midi.send([NoteOff(62, pad0)])

    if pad1:
        midi.send([NoteOn(60, pad1)])
        #print("pad1")
        #time.sleep(0.01)
        midi.send([NoteOff(60, pad1)])

    if pad2:
        midi.send([NoteOn(65, pad2)])
        #print("pad2")
        #time.sleep(0.01)
        midi.send([NoteOff(65, pad2)])


    #time.sleep(0.01)