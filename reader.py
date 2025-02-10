#!/usr/bin/env python
# coding=utf-8

# uvex-Profas - Anlagenerfassung
# RFID - reader
#
# www.emsgmbh.com

import pn532
import mfrc522
import event
import threading
import time

try:
    import config
    import logging

    logger = logging.getLogger(__name__)
except ImportError:
    class DebugLogger():
        def debug(self, msg, *args):
            print(msg % args)


    logger = DebugLogger()

# TEST
import signal
from sys import exit


class RFIDReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'RFIDReaderThread'
        self.rfid_uid_found_event = event.Event()
        self.continue_reading = True
        self.mifare_reader = pn532.PN532()

    def register(self, event_handler):
        self.rfid_uid_found_event += event_handler

    def unregister(self, event_handler):
        self.rfid_uid_found_event -= event_handler

    def run(self):
        while (self.continue_reading):
            # configure Pn532
            self.mifare_reader.SAM_configuration()
            # Scan for cards Returns True if the command was received successfully. this does not return the uid !!!
            status = self.mifare_reader.listen_for_passive_target()

            # if no card is found: continue
            if status != True:
                # and wait a bit before doing so
                print("No card is found......")
                time.sleep(0.2)
                continue

            if self.continue_reading:
                # Get the UID of the card
                # will wait up to timeout seconds and return None if no card is found
                # else return a bytearray with the uid
                uid = self.mifare_reader.read_passive_target()
                print("This is the type of uid", type(uid))
                print("This the UID ==================>", uid)
                # if no uid is found: continue
                if uid == None:
                    continue

                self.rfid_uid_found_event(self, byte_arr_to_hex_str(uid))

            if self.continue_reading:
                # do not poll too often
                time.sleep(0.2)

        self.mifare_reader.cleanup()

    def stop(self):
        self.continue_reading = False


byte_arr_to_hex_str = lambda arr: u"".join(u"%02x" % b for b in arr)


# TEST
class ExampleListener:
    def __init__(self, title):
        self.title = title

    def event_eargs_printer(self, sender, eargs):
        print "%s: %r event eargs: %r\n" % (self.title, sender, eargs)


if __name__ == '__main__':
    print"Testing MFRC522 touch event reader"
    listener = ExampleListener('example listener')


    def end_read(signal, frame):
        print"Ctrl+C captured, ending read."
        test.stop()
        exit()


    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    test = RFIDReader()
    test.register(listener.event_eargs_printer)
    test.start()

    print"main thread sleep.."
    time.sleep(15)
    print"main thread sleep some more without handler..."
    test.unregister(listener.event_eargs_printer)
    time.sleep(5)
    print"main thread sleep some more with smoothed handler..."
    test.register(event.smooth(3)(listener.event_eargs_printer))
    time.sleep(15)
    print"main thread stops"

    test.stop()
    # print "%s (%s) alive? %s \n" % (test.name, test.ident, test.is_alive())
