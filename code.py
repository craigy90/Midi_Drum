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

while True:

    raw0 = adc0.value
    raw1 = adc1.value
    raw2 = adc2.value

    pad0 = int(raw0/30)-50
    pad1 = int(raw1/65)-32
    pad2 = int(raw2/20)-50

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
        time.sleep(0.1)
        if pad1 > pad0 or pad1 > pad2:
            pad0 = 0
            pad2 = 0
        elif pad2 > pad1 or pad2 > pad0:
            pad1 = 0
            pad2 = 0
        elif pad0 > pad2 or pad0 > pad1:
            pad2 = 0
            pad1 = 0
        print(pad0, "\t", pad1, "\t", pad2)

    if pad0:
        midi.send([NoteOn(40, pad0)])
        print("pad0")
        time.sleep(0.01)
        midi.send([NoteOff(40, pad0)])

    if pad1:
        midi.send([NoteOn(45, pad1)])
        print("pad1")
        time.sleep(0.01)
        midi.send([NoteOff(45, pad1)])

    if pad2:
        midi.send([NoteOn(50, pad2)])
        print("pad2")
        time.sleep(0.01)
        midi.send([NoteOff(50, pad2)])


    time.sleep(0.01)