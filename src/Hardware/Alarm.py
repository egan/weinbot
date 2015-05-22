##
# Hardware.py: Class implementing control of WEINBot alarm tones via GPIO.
#
# Copyright 2015, Egan McComb
#
##

import Adafruit_BBIO.GPIO as GPIO
import threading
import time
import logging

class Alarm():
    """
        Alarm: A class that provides an interface to control the WEINBot STI
               minicontroller alarm and tones (5 bit selector) via GPIO.

        http://www.sti-usa.com/pdf/specs/SA5000.pdf
    """
    # Alarm tone aliases. See page 5 of the documentation for a list of tones.
    aliases = {
            "water": 1,
            "waste": 3,
            "rev": 5,
            "gen": 7
            }

    def __init__(self, pin_enable="P8_26", pins_selector=("P8_21", "P8_22", "P8_23", "P8_24", "P8_25")):
        """
            pin_enable:    BBB GPIO pin controlling alarm on/off.
            pins_selector: BBB GPIO pins for tone selector.

        """

        # Set up GPIO.
        self.go = False
        self.pin_enable = pin_enable
        GPIO.setup(pin_enable, GPIO.OUT)
        self.pins_selector = pins_selector
        for pin in pins_selector:
            GPIO.setup(pin, GPIO.OUT)

        return None

    def __del__(self):
        self.stop()
        return

    def start(self):
        """
            start: Start the alarm.

        """
        logging.debug("alarm: started")
        self.go = True
        GPIO.output(self.pin_enable, GPIO.HIGH)

    def strobe(self, tone, time_spec):
        """
            strobe: Strobe alarm tone according to time.

                tone:      Tone or alias to produce.
                time_spec: List of times for toggle (s).
        """
        self.setTone(tone)
        t = threading.Thread(target=self.__handler, args=(time_spec,))
        t.start()

    def __handler(self, time_spec):
        logging.debug("alarm: strobe started")
        for t in time_spec:
            self.toggle()
            time.sleep(t)
        self.toggle()
        logging.debug("alarm: strobe stopped")

    def setTone(self, tone):
        """
            setTone: Set the alarm tone.

                tone: Tone number or alias to produce.

        """
        # Determine tone number (decimal).
        if tone in self.aliases:
            tone = self.aliases[tone]
        elif tone in range(1, 33):
            tone -= 1
        else:
            logging.debug("setTone: invalid tone number or alias")
            return -1

        # Pause alarm if needed.
        if self.go:
            self.stop()
            self.go = True

        # Write tone selector bits.
        if (tone & 0x1):
            GPIO.output(self.pins_selector[0], GPIO.HIGH)
        else:
            GPIO.output(self.pins_selector[0], GPIO.LOW)

        if (tone & 0x2):
            GPIO.output(self.pins_selector[1], GPIO.HIGH)
        else:
            GPIO.output(self.pins_selector[1], GPIO.LOW)

        if (tone & 0x4):
            GPIO.output(self.pins_selector[2], GPIO.HIGH)
        else:
            GPIO.output(self.pins_selector[2], GPIO.LOW)

        if (tone & 0x8):
            GPIO.output(self.pins_selector[3], GPIO.HIGH)
        else:
            GPIO.output(self.pins_selector[3], GPIO.LOW)

        if (tone & 0x10):
            GPIO.output(self.pins_selector[4], GPIO.HIGH)
        else:
            GPIO.output(self.pins_selector[4], GPIO.LOW)

        logging.debug("setTone: %d" %(tone))

        # Resume alarm if needed.
        if self.go:
            self.start()

    def toggle(self):
        """
            toggle: Toggle alarm state.

        """
        if self.go:
            self.stop()
        else:
            self.start()

    def stop(self):
        """
            stop: Stop the alarm.

        """
        logging.debug("alarm: stopped")
        self.go = False
        GPIO.output(self.pin_enable, GPIO.LOW)
