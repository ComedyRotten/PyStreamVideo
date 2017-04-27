import random
import socket
import _thread
import time

'''
This is the server that sends a given file over a stream. It does nothing else.

State 0: WAITING
State 1: SETUP
State 2: PLAY
State 3: PAUSE
State 4: TEARDOWN
'''

class Server():

    def __init__(self, dest, port, filename, listenport=33122, debug=False, timeout=10):
        self.dest = dest
        self.dport = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None)  # blocking
        self.sock.bind(('', random.randint(10000, 40000)))
        self.rtimeout = timeout

        self.current_state = 0
        self.current_seqno = 0

        if filename == None:
            self.infile = sys.stdin
        else:
            self.infile = open(filename, "r")

        self.MESSAGE_HANDLER = {
            'SETUP': self._handle_setup,
            'PLAY': self._handle_play,
            'PAUSE': self._handle_pause,
            'TEARDOWN': self._handle_teardown
        }

    def start(self):
        # Running loop
        while True:
            # Continually act according to the current state
            if self.current_state == 0:
                # Wait for initial setup message (do nothing)
                pass
            elif self.current_state == 1:
                # Setup the connection and prepare to send data
                pass
            elif self.current_state == 2:
                # Play the video, begin sending the RTP packets
                pass
            elif self.current_state == 3:
                # Pause, stop sending the rtp packets
                pass
            elif self.current_state == 4:
                # Stop sending the RTP packets and teardown the connection
                pass
            else:
                # If the state is unrecognized, don't do anything
                pass

            # look for a message and where it came from
            message = self.receive(self.rtimeout)

            # if a message is received
            if message:
                # Split the received packet up into it's individual parts
                command, seqno, session = self.split_packet(message)

                # feed the retrieved command and info into the handler
                self.MESSAGE_HANDLER.get(command)(seqno, session)
        pass

    def _handle_setup(self, seqno, session):
        pass

    def _handle_play(self, seqno, session):
        pass

    def _handle_pause(self, seqno, session):
        pass

    def _handle_teardown(self, seqno, session):
        pass

    # Waits until packet is received to return.
    def receive(self, timeout=None):
        self.sock.settimeout(timeout)
        try:
            return self.sock.recv(4096)
        except (socket.timeout, socket.error):
            return None

    '''
    Sends a packet to the destination address.
    '''
    def send(self, message, address=None):
        if address is None:
            address = (self.dest, self.dport)
        self.sock.sendto(message.encode(), address)

    '''
    Prepares an RTP packet to send
    Message format:
    The message is 1472 bytes divided up into the following:
        seqno:      2-byte sequence number
        timestamp:  4-byte timestamp of the current time of the sent frame
        SSRC:       4-byte unique identifier of the source of the stream (RTSP session id)
        delimiters: 3 bytes
        data:       1459 bytes of data
    '''
    def make_RTP_packet(self, seqno, timestamp, SSRC, data):
        return "{0}|{1}|{2}|{3}".format(seqno, timestamp, SSRC, data)

    '''
        Prepares an RTSP packet to send.
        Message format:
        The message is 1472 bytes divided up into the following:
            Command: 32-byte string
            CSeq:    32-bit integer same as what the client sent, increments by one
            Transport: what it's going to send (RTP, unicast, client/server port, ssrc
            Session: 32-bit Unique session id (we initialize this)
            
        The server only sends initial setup information and acknowledgements.
        We probably don't need to send anything since this is just a very basic, P2P streaming video.
    '''
    def make_RTSP_packet(self, command, seqno, session):
        return "{0}|{1}|{2}|".format(command, seqno, session)

    # Split and RTSP packet up into its appropriate pieces
    def split_packet(self, message):
        pieces = message.decode().split('|')
        command, seqno, session = pieces[0:3]  # first two elements always treated as msg type and seqno
        return command, seqno, session