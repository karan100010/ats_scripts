#!/usr/bin/env python3
import playsound
from asterisk.agi import *

agi = AGI()

try:
    # Answer the call
    agi.answer()

    # Play the audio file
    playsound.playsound("hello-world.wav")

    # Wait for the user to enter digits
    result = agi.wait_for_digit(5000)  # Timeout after 5000 milliseconds"

    # You can then handle the result as needed
    if result == -1:
        agi.verbose("User did not enter any digits")
    else:
        agi.verbose("User entered: " + chr(result))

except AGIException as e:
    agi.verbose(str(e))