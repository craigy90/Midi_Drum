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
adc = analogio.AnalogIn(board.A0)

while True:

    raw = adc.value
    pad1 = int(raw/20)-22
    if pad1 < 0:
        pad1 = 0
    if pad1 > 127:
        pad1 = 127
    print(pad1)
    if pad1:
        midi.send([NoteOn(40, pad1)])
        print("Note on...")
        time.sleep(1)
        midi.send([NoteOff(40, pad1)])
        print("Note off...")
        time.sleep(1)


    time.sleep(0.01)