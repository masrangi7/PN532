"""
====================================================
This module will let you communicate with a PN532 RFID/NFC shield or breakout
using I2C, SPI or UART.
"""

from pyA10Lime import i2c
from datetime import datetime
from datetime import timedelta
import time
import os
from pyA10Lime.gpio import gpio
from pyA10Lime.gpio import port
from pyA10Lime.gpio import connector

# from digitalio import Direction


_PREAMBLE = 0x00
_STARTCODE1 = 0x00
_STARTCODE2 = 0xFF
_POSTAMBLE = 0x00
PN532_DEFAULT_ADDRESS = 0x24
_HOSTTOPN532 = 0xD4
_PN532TOHOST = 0xD5

# PN532 Commands
_COMMAND_DIAGNOSE = 0x00
_COMMAND_GETFIRMWAREVERSION = 0x02
_COMMAND_GETGENERALSTATUS = 0x04
_COMMAND_READREGISTER = 0x06
_COMMAND_WRITEREGISTER = 0x08
_COMMAND_READGPIO = 0x0C
_COMMAND_WRITEGPIO = 0x0E
_COMMAND_SETSERIALBAUDRATE = 0x10
_COMMAND_SETPARAMETERS = 0x12
_COMMAND_SAMCONFIGURATION = 0x14
_COMMAND_POWERDOWN = 0x16
_COMMAND_RFCONFIGURATION = 0x32
_COMMAND_RFREGULATIONTEST = 0x58
_COMMAND_INJUMPFORDEP = 0x56
_COMMAND_INJUMPFORPSL = 0x46
_COMMAND_INLISTPASSIVETARGET = 0x4A
_COMMAND_INATR = 0x50
_COMMAND_INPSL = 0x4E
_COMMAND_INDATAEXCHANGE = 0x40
_COMMAND_INCOMMUNICATETHRU = 0x42
_COMMAND_INDESELECT = 0x44
_COMMAND_INRELEASE = 0x52
_COMMAND_INSELECT = 0x54
_COMMAND_INAUTOPOLL = 0x60
_COMMAND_TGINITASTARGET = 0x8C
_COMMAND_TGSETGENERALBYTES = 0x92
_COMMAND_TGGETDATA = 0x86
_COMMAND_TGSETDATA = 0x8E
_COMMAND_TGSETMETADATA = 0x94
_COMMAND_TGGETINITIATORCOMMAND = 0x88
_COMMAND_TGRESPONSETOINITIATOR = 0x90
_COMMAND_TGGETTARGETSTATUS = 0x8A

_RESPONSE_INDATAEXCHANGE = 0x41
_RESPONSE_INLISTPASSIVETARGET = 0x4B

_WAKEUP = 0x55

_MIFARE_ISO14443A = 0x00

# Mifare Commands
MIFARE_CMD_AUTH_A = 0x60
MIFARE_CMD_AUTH_B = 0x61
MIFARE_CMD_READ = 0x30
MIFARE_CMD_WRITE = 0xA0
MIFARE_CMD_TRANSFER = 0xB0
MIFARE_CMD_DECREMENT = 0xC0
MIFARE_CMD_INCREMENT = 0xC1
MIFARE_CMD_STORE = 0xC2
MIFARE_ULTRALIGHT_CMD_WRITE = 0xA2

# Prefixes for NDEF Records (to identify record type)
NDEF_URIPREFIX_NONE = 0x00
NDEF_URIPREFIX_HTTP_WWWDOT = 0x01
NDEF_URIPREFIX_HTTPS_WWWDOT = 0x02
NDEF_URIPREFIX_HTTP = 0x03
NDEF_URIPREFIX_HTTPS = 0x04
NDEF_URIPREFIX_TEL = 0x05
NDEF_URIPREFIX_MAILTO = 0x06
NDEF_URIPREFIX_FTP_ANONAT = 0x07
NDEF_URIPREFIX_FTP_FTPDOT = 0x08
NDEF_URIPREFIX_FTPS = 0x09
NDEF_URIPREFIX_SFTP = 0x0A
NDEF_URIPREFIX_SMB = 0x0B
NDEF_URIPREFIX_NFS = 0x0C
NDEF_URIPREFIX_FTP = 0x0D
NDEF_URIPREFIX_DAV = 0x0E
NDEF_URIPREFIX_NEWS = 0x0F
NDEF_URIPREFIX_TELNET = 0x10
NDEF_URIPREFIX_IMAP = 0x11
NDEF_URIPREFIX_RTSP = 0x12
NDEF_URIPREFIX_URN = 0x13
NDEF_URIPREFIX_POP = 0x14
NDEF_URIPREFIX_SIP = 0x15
NDEF_URIPREFIX_SIPS = 0x16
NDEF_URIPREFIX_TFTP = 0x17
NDEF_URIPREFIX_BTSPP = 0x18
NDEF_URIPREFIX_BTL2CAP = 0x19
NDEF_URIPREFIX_BTGOEP = 0x1A
NDEF_URIPREFIX_TCPOBEX = 0x1B
NDEF_URIPREFIX_IRDAOBEX = 0x1C
NDEF_URIPREFIX_FILE = 0x1D
NDEF_URIPREFIX_URN_EPC_ID = 0x1E
NDEF_URIPREFIX_URN_EPC_TAG = 0x1F
NDEF_URIPREFIX_URN_EPC_PAT = 0x20
NDEF_URIPREFIX_URN_EPC_RAW = 0x21
NDEF_URIPREFIX_URN_EPC = 0x22
NDEF_URIPREFIX_URN_NFC = 0x23

_GPIO_VALIDATIONBIT = 0x80
_GPIO_P30 = 0
_GPIO_P31 = 1
_GPIO_P32 = 2
_GPIO_P33 = 3
_GPIO_P34 = 4
_GPIO_P35 = 5

_ACK = b"\x00\x00\xFF\x00\xFF\x00"
_FRAME_START = b"\x00\x00\xFF"


class BusyError(Exception):
    """Base class for exceptions in this module."""


class PN532(object):
    """PN532 driver base, must be extended for I2C/SPI/UART interfacing"""

    def __init__(self):
        """Create an instance of the PN532 class"""
        gpio.init()  # Initialize module. Always called first
        self.low_power = True
        i2c.init('/dev/i2c-2')
        i2c.open(PN532_DEFAULT_ADDRESS)

    #  self.PN532_Init()

    # write data to slave device
    def write_PN532(self, framebytes):
        # print("Before write_PN532..........")
        #	print("This is the Typ of data : ","This is the Typ of data : ",  type(framebytes))
        #	print("the framebytes before adding the addr  :",[hex(i) for i in framebytes])
        i2c.write(list(framebytes))  ### write val to register addr

    #       print("After write_PN532 method.....")

    # read data from slave device
    def read_PN532(self, len):
        return i2c.read(len)

    def mySleep(self, secondToSleep):
        # from datetime import timedelta

        # now = datetime.now()
        # futureTime = now + timedelta(seconds=secondToSleep)
        # while now < futureTime:
        #    print("Now is greater than future time.....")
        #    break
        time.sleep(secondToSleep)

    #  print("Waiking after the mySleep method..................")

    def _wakeup(self):
        gpio.setcfg(port.PG10, gpio.OUTPUT)  # Configure LED1 as output
        self.mySleep(0.01)
        gpio.output(port.PG10, gpio.LOW)
        self.mySleep(0.01)
        gpio.output(port.PG10, gpio.HIGH)
        self.mySleep(0.01)

    def display(self):
        print("Timer display method.......")

    def _wait_ready(self, mytimeout=1):
        """Poll PN532 if status byte is ready, up to `timeout` seconds"""

        # print("Before the first mySleep method inside _wait_ready method...............")
        # self.mySleep(1)
        # print("After the first mySleep inside _wait_ready method...............")

        status = bytearray(1)
        currentDatetime = datetime.now()

        while ((datetime.now() - currentDatetime).total_seconds() < mytimeout):
            #    print("Inside while loop from _wait_ready method...............")
            try:
                #	print("Before status[0] call......................................")

                response = self.read_PN532(1)
                #	print("This is the first read method call =============>",response)
                status[0] = response[0]
            #	print(" status[0] is equal to =================> ", status[0])

            except OSError:
                print("Inside the OSError...............................")
                self._wakeup()
                continue
            if status == b'\x01':
                #	print("status is equals to ==========>",status)
                return True
            self.mySleep(0.1)
            # Timed out!
        return False

    def _write_frame(self, data):
        """Write a frame to the PN532 with the specified data bytearray."""
        assert (
                data is not None and 1 < len(data) < 255
        ), "Data must be array of 1 to 255 bytes."
        # Build frame to send as:
        # - Preamble (0x00)
        # - Start code  (0x00, 0xFF)
        # - Command length (1 byte)
        # - Command length checksum
        # - Command bytes
        # - Checksum
        # - Postamble (0x00)
        length = len(data)
        frame = bytearray(length + 8)
        frame[0] = _PREAMBLE
        frame[1] = _STARTCODE1
        frame[2] = _STARTCODE2
        checksum = sum(frame[0:3])
        frame[3] = length & 0xFF
        frame[4] = (~length + 1) & 0xFF
        frame[5:-2] = data
        checksum += sum(data)
        frame[-2] = ~checksum & 0xFF
        frame[-1] = _POSTAMBLE
        # Send frame.

        #        print("Write frame: ", [hex(i) for i in frame])
        self.write_PN532(frame)

    def _read_frame(self, length):
        """Read a response frame from the PN532 of at most length bytes in size.
        Returns the data inside the frame if found, otherwise raises an exception
        if there is an error parsing the frame.  Note that less than length bytes
        might be returned!
        """
        # Read frame with expected length of data.
        #	print("*************************************************************************************************************")

        response = self.read_PN532(length + 7)

        #	print("This is the response ===========>", [hex(i) for i in response])
        #	print("This is the response type", type(response))
        # Swallow all the 0x00 values that preceed 0xFF.
        offset = 1
        while response[offset] == 0x00:
            offset += 1
            if offset >= len(response):
                raise RuntimeError("Response frame preamble does not contain 0x00FF!")
        if response[offset] != 0xFF:
            raise RuntimeError("Response frame preamble does not contain 0x00FF!")
        offset += 1
        if offset >= len(response):
            raise RuntimeError("Response contains no data!")
        # Check length & length checksum match.
        frame_len = response[offset]
        if (frame_len + response[offset + 1]) & 0xFF != 0:
            raise RuntimeError("Response length checksum did not match length!")
        # Check frame checksum value matches bytes.
        checksum = sum(response[offset + 2: offset + 2 + frame_len + 1]) & 0xFF
        if checksum != 0:
            raise RuntimeError(
                "Response checksum did not match expected value: ", checksum
            )
        # Return frame data.
        return response[offset + 2: offset + 2 + frame_len]

    def call_function(
            self, command, response_length=0, params=[], timeout=1
    ):  # pylint: disable=dangerous-default-value
        """Send specified command to the PN532 and expect up to response_length
        bytes back in a response.  Note that less than the expected bytes might
        be returned!  Params can optionally specify an array of bytes to send as
        parameters to the function call.  Will wait up to timeout seconds
        for a response and return a bytearray of response bytes, or None if no
        response is available within the timeout.
        """
        if not self.send_command(command, params=params, timeout=timeout):
            return None
        return self.process_response(
            command, response_length=response_length, timeout=timeout
        )

    def send_command(
            self, command, params=[], timeout=1
    ):  # pylint: disable=dangerous-default-value
        """Send specified command to the PN532 and wait for an acknowledgment.
        Will wait up to timeout seconds for the acknowlegment and return True.
        If no acknowlegment is received, False is returned.
        """
        if self.low_power:
            #           print("low_power is true and calling _wakeup method.............")
            self._wakeup()
        #          print("_wakeup method sucessfull................")

        # Build frame data with command and parameters.
        data = bytearray(2 + len(params))
        data[0] = _HOSTTOPN532
        data[1] = command & 0xFF
        for i, val in enumerate(params):
            data[2 + i] = val
        # Send frame and wait for response.
        try:
            #         print("Sending frame using _write_frame method.............................")
            #	    print("Write data from send_command:", [hex(i) for i in data])
            self._write_frame(data)
        #           print("write frame .....")
        except OSError:
            print("OS Error inside send_command......................")
            return False
        boolean_wait_ready = self._wait_ready(timeout)
        if not boolean_wait_ready:
            return False
        #	print("This is the boolean_wait_ready", boolean_wait_ready)
        # Verify ACK response and wait to be ready for function response.
        #	print("Before _ACK == self.read_PN532(len(_ACK))")
        responseACK = bytearray(2)
        ackPacketCode = b"\x00\xFF"
        responseAckArry = self.read_PN532(len(_ACK))
        #	print("This is the response array ===>",responseAckArry)

        responseACK[0] = responseAckArry[2]
        responseACK[1] = responseAckArry[3]

        #	print("This is the responseAck ===>",[hex(i) for i in responseACK])
        #	print(type(responseACK))
        #	print("This ia the ackPacketCode ======>",ackPacketCode)
        #	print(type(ackPacketCode))
        if not ackPacketCode == responseACK:
            raise RuntimeError("Did not receive expected ACK from PN532!")
        return True

    def process_response(self, command, response_length=0, timeout=1):
        """Process the response from the PN532 and expect up to response_length
        bytes back in a response.  Note that less than the expected bytes might
        be returned! Will wait up to timeout seconds for a response and return
        a bytearray of response bytes, or None if no response is available
        within the timeout.
        """
        if not self._wait_ready(timeout):
            return None
        # Read response bytes.
        response = self._read_frame(response_length + 2)
        #	print("This is the final response-............", [hex(i) for i in response])
        # Check that response is for the called function.
        if not (response[0] == _PN532TOHOST and response[1] == (command + 1)):
            raise RuntimeError("Received unexpected command response!")
        # Return response data.
        return response[2:]

    def power_down(self):
        """Put the PN532 into a low power state. If the reset pin is connected a
        hard power down is performed, if not, a soft power down is performed
        instead. Returns True if the PN532 was powered down successfully or
        False if not."""
        if self._reset_pin:  # Hard Power Down if the reset pin is connected
            self._reset_pin.value = False
            self.low_power = True
        else:
            # Soft Power Down otherwise. Enable wakeup on I2C, SPI, UART
            response = self.call_function(_COMMAND_POWERDOWN, params=[0xB0, 0x00])
            self.low_power = response[0] == 0x00
        time.sleep(0.005)
        return self.low_power

    def firmware_version(self):
        """Call PN532 GetFirmwareVersion function and return a tuple with the IC,
        Ver, Rev, and Support values.
        """
        response = self.call_function(_COMMAND_GETFIRMWAREVERSION, 4, timeout=0.5)
        #	print("This is the type of response inside firmware_version final result", type(response))
        #	print("this is the final result =========================>", response)
        if response is None:
            raise RuntimeError("Failed to detect the PN532")
        return tuple(response)

    def SAM_configuration(self):  # pylint: disable=invalid-name
        """Configure the PN532 to read MiFare cards."""
        # Send SAM configuration command with configuration for:
        # - 0x01, normal mode
        # - 0x14, timeout 50ms * 20 = 1 second
        # - 0x01, use IRQ pin
        # Note that no other verification is necessary as call_function will
        # check the command was executed as expected.
        self.call_function(_COMMAND_SAMCONFIGURATION, params=[0x01, 0x14, 0x01])

    def read_passive_target(self, card_baud=_MIFARE_ISO14443A, timeout=1):
        """Wait for a MiFare card to be available and return its UID when found.
        Will wait up to timeout seconds and return None if no card is found,
        otherwise a bytearray with the UID of the found card is returned.
        """
        # Send passive read command for 1 card.  Expect at most a 7 byte UUID.
        response = self.listen_for_passive_target(card_baud=card_baud, timeout=timeout)
        # If no response is available return None to indicate no card is present.
        if not response:
            return None
        return self.get_passive_target(timeout=timeout)

    def listen_for_passive_target(self, card_baud=_MIFARE_ISO14443A, timeout=1):
        """Send command to PN532 to begin listening for a Mifare card. This
        returns True if the command was received succesfully. Note, this does
        not also return the UID of a card! `get_passive_target` must be called
        to read the UID when a card is found. If just looking to see if a card
        is currently present use `read_passive_target` instead.
        """
        # Send passive read command for 1 card.  Expect at most a 7 byte UUID.
        try:
            response = self.send_command(
                _COMMAND_INLISTPASSIVETARGET, params=[0x01, card_baud], timeout=timeout
            )
        except BusyError:
            return False  # _COMMAND_INLISTPASSIVETARGET failed
        return response

    def get_passive_target(self, timeout=1):
        """Will wait up to timeout seconds and return None if no card is found,
        otherwise a bytearray with the UID of the found card is returned.
        `listen_for_passive_target` must have been called first in order to put
        the PN532 into a listening mode.
        It can be useful to use this when using the IRQ pin. Use the IRQ pin to
        detect when a card is present and then call this function to read the
        card's UID. This reduces the amount of time spend checking for a card.
        """
        response = self.process_response(
            _COMMAND_INLISTPASSIVETARGET, response_length=30, timeout=timeout
        )
        # If no response is available return None to indicate no card is present.
        if response is None:
            return None
        # Check only 1 card with up to a 7 byte UID is present.
        if response[0] != 0x01:
            raise RuntimeError("More than one card detected!")
        if response[5] > 7:
            raise RuntimeError("Found card with unexpectedly long UID!")
        # Return UID of card.
        return response[6: 6 + response[5]]

    def cleanup(self):
        i2c.close()

    def PN532_Init(self):
        # self.SAM_configuration()
        firmwareVersion = self.firmware_version()
        print("This is the firmware version ==============================>", firmwareVersion)
    # self.listen_for_passive_target()
    # self.read_passive_target()
