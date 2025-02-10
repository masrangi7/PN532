#!/usr/bin/env python
# -*- coding: utf8 -*-

from tempmon.tempmon import measure as temp_measure
import rfid.reader as rfid_reader
from datetime import datetime
import time


def warn(msg):
    print
    '\033[93m' + msg + '\033[0m'


class EventListener(object):
    def __init__(self):
        self.tag_seen = False

    def event_eargs_printer(self, sender, eargs):
        print
        "RFID-Tag registriert, UID ist %s\n" % (eargs,)
        self.tag_seen = True


print
'Uhrzeit:', datetime.now().isoformat(' ')

print
'Temperatursensor-Test:'
# temp_measurement = temp_measure(3, '/dev/i2c-2', 0x48)
# print 'gemessene Temperatur:', temp_measurement
# if temp_measurement < 25.0 or temp_measurement > 45:
#    warn('ACHTUNG: Temperatur nicht in erwartetem Bereich (25-45°C). Sensor richtig angeschlossen?')

print
'RFID-Reader-Test:'
listener = EventListener()

reader = rfid_reader.RFIDReader()
reader.register(listener.event_eargs_printer)
reader.start()
print
'Bitte halten Sie einen RFID-Tag gegen die Lesezone'
time.sleep(15)
reader.stop()

if not listener.tag_seen:
    warn('Kein RFID-Tag gelesen. RFID-Reader richtig angeschlossen?')

raw_input("Zum Beenden [ENTER] drücken...")
