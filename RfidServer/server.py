from flask import Flask
from flask_restful import Resource, Api, reqparse
import pn532
import time
import mfrc522

app = Flask(_name_)
api = Api(api)


class PN532(Resource):
    mifare_reader_PN532 = pn532.PN532()
    mifare_reader_mfrc522 = mfrc522.MFRC522()


"""   def __init__(self):
        self.mifare_reader = pn532.PN532()
        self.continue_reading = True
"""
# method go here
def getUid(self):
    isPN532 = False
    uid == None
    response = self.mifare_reader_PN532.firmware_verison()

    if response != 'Failed to detect the PN532':
        isPN532 = True


    if isPN532 == True:
        while (self.continue_reading):
            # configure pn532
            self.mifare_reader_PN532.SAM_configuration()
            # scan for cards and return True if the command was received successfully. this does not return the uid!!!
            status = self.mifare_reader_PN532.listen_for_passive_target()

            # if card is found continu
            if status != True:
                # wait a bit before
                time.sleep(0.2)
                continue

            if self.continue_reading:
                uid = self.mifare_reader_PN532.read_passive_target()

                if uid == None:
                    continue
    elif isPN532 != True:
        while True:
            # scan for the card
            (status, tagType) = self.mifare_reader_mfrc522.MFRC522_Request(self.mifare_reader_mfrc522.PICC_REQIDL)

            # if no card is found continue
            if status != self.mifare_reader_mfrc522.MI_OK:
                continue

            (status, uid) = self.mifare_reader_mfrc522.MFRC522_Anticoll()

            # if no uid is found: continue
            if status != self.mifare_reader_mfrc522.MI_OK:
                continue

    return byte_arry_to_hex_str(uid), 200


byte_arry_to_hex_str = lambda arr: u"".join(u"%02x % b for b in arry")

api.add_resource(PN532, '/getUid')  # /getUid us or entry point

if __name__ == '__main__':
    app.run()
