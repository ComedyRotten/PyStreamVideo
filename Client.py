from tkinter import *
import tkinter.messagebox
from struct import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import socket
import time
import sys

'''
The RTSP protocol is only for commands from the client to the server.
The server sends acknowledgements back of commands, but that is not completely necessary.

The RTP protocol is used by the server to pack up the video frames and send them to the client.
There need to be two threads running on the server and client (unless we implement
the interleaving of messages or something).

Server threads:
Thread 1: sending RTP packets -> pack up frames and send them to the client
Thread 2: receiving RTSP packets -> get commands and act on those commands

Client threads:
Thread 1: receiving RTP packets -> receive the frame and display it for a set amount of time before
            the next frame is displayed. These images will need to be buffered in an array possibly.
Thread 2: sending RTSP packets -> send commands via the GUI buttons. Only four commands will be
            supported: 
            Setup - handshake with timing info, image size, session number, etc.
            Teardown - stop sending RTP packets and close the connection.
            Play - "send me RTP packets"
            Pause - "stop sending me RTP packets"
            Each of these will modify the state of the server. We will need to make sure the server
            knows what to do in each state.
'''
class MediaGui(Frame):

    def __init__(self, dest, port, filename, listenport=33122, debug=False, timeout=10, master=None):
        # Frame Setup
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

        # Connection Setup
        self.dest = dest
        self.dport = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None)  # blocking
        self.sock.bind(('', random.randint(10000, 40000)))
        self.rtimeout = timeout

        # Sequence Numbers for RTSP and RTP packets
        # These increment by 1
        # If a frame is missed (noticeable by timestamp discrepency, the two frames on either side
        # are each shown for an additional half of the time of the missing frame to hide it.
        self.current_RTSP_seqno = 0
        self.current_RTP_seqno = 0

    def init_window(self):

        self.master.title("Media Streamer")
        self.pack(fill=BOTH, expand=1)

        # primary frame
        # frame = Frame(master)
        # frame.pack()

        # ******* Main Menu ********
        menu = Menu(self.master)
        # configure a menu using the previously instantiated menu
        self.master.config(menu=menu)
        # add a submenu (e.g. "File, Edit, Help, etc.")
        file = Menu(menu)
        # create a File button with the drop-down menu with the subMenu
        menu.add_cascade(label="File", menu=file)
        # add a sub-option/command and assign a method to each
        file.add_command(label="Setup", command=self.setup_conn)
        file.add_command(label="Teardown", command=self.teardown_conn)
        file.add_separator()
        file.add_command(label="Exit", command=self.quit)

        edit = Menu(menu)
        menu.add_cascade(label="Media", menu=edit)
        edit.add_command(label="Play", command=self.play_video)
        edit.add_command(label="Pause", command=self.pause_video)

        # Media frame
        self.media_frame = Frame(self)
        self.media_frame.pack(fill=BOTH)

        # ******* Sprites and Icons *******
        # May just end up using this code to display the image since it places it more correctly
        # within the frame. So this code would go in the "show_img" method.
        self.photo = PhotoImage(file="pic.png")
        self.label = Label(self.media_frame, image=self.photo)
        self.label.pack(fill=BOTH)

        # Media controls frame
        self.controls_frame = Frame(self.media_frame)
        self.controls_frame.pack(side=BOTTOM)

        self.setupButton = Button(self.controls_frame, text="Setup", command=self.setup_conn)
        self.setupButton.pack(side=LEFT, padx=2, pady=2)

        self.playButton = Button(self.controls_frame, text="Play", command=self.play_video)
        self.playButton.pack(side=LEFT, padx=2, pady=2)

        self.pauseButton = Button(self.controls_frame, text="Pause", command=self.pause_video)
        self.pauseButton.pack(side=LEFT, padx=2, pady=2)

        self.teardownButton = Button(self.controls_frame, text="Teardown", command=self.teardown_conn)
        self.teardownButton.pack(side=LEFT, padx=2, pady=2)

        # ******* Status Bar ********
        # bd = border, anchor = West (make sure text appears on the left)
        self.status = Label(self, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        self.status.config(text="Testing...")

    def setup_conn(self):
        print("Setting up connection...")

    def teardown_conn(self):
        print("Teardown connection...")

    # If a frame is missed (noticeable by timestamp discrepency, the two frames on either side
    # are each shown for an additional half of the time of the missing frame to hide it.
    def play_video(self):
        print("Playing video...")

    def pause_video(self):
        print("Pause video...")

    def show_image(self):
        # The showing of the image
        # This method will show the current frame of the video, that is all
        # The timing and such is dealt with elsewhere.
        load = Image.open("cah.jpg")
        mymode = load.mode
        mysize = load.size
        mybytes = load.tobytes()
        print(mybytes) # Testing the conversion of a frame to bytes
        cap = cv2.VideoCapture('orion_1.mpg')

        while(cap.isOpened()):
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # cv2.imshow('frame', gray)
            # self.photo = PhotoImage(file="pic.png")
            self.vid = Label(self.media_frame, image=frame)
            self.vid.pack(fill=BOTH)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

        # newimg = Image.new(mymode, mysize)
        # decodedimage = newimg.frombytes(mybytes, decoder_name="raw")

        # render = ImageTk.PhotoImage(decodedimage)
        # print("Format: {0} height: {1} width: {2}".format(render.__sizeof__(), render.height(), render.width()))

        # img = Label(self.media_frame, image=render)
        # img.image = render
        # img.place(x=0, y=0)
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
    def make_RTSP_packet(self, command, seqno, transport, session):
        return "{0}|{1}|{2}|{3}|".format(command, seqno, transport, session)

    # Split and RTSP packet up into its appropriate pieces
    def split_RTSP_packet(self, message):
        pieces = message.decode().split('|')
        command, seqno, transport, session = pieces[0:4]  # first two elements always treated as msg type and seqno
        return command, seqno, transport, session

    # Split an RTP packet up into its appropriate pieces
    def split_packet(self, message):
        pieces = message.decode().split('|')
        seqno, timestamp, SSRC = pieces[0:3]  # first three elements always treated as msg type and seqno
        data = b'|'.join(pieces[3:-1])  # everything in between is considered data
        return seqno, timestamp, SSRC, data

# Create a blank window
root = Tk()
root.geometry("480x320")

# ******* Media Stuff ********
b = MediaGui(root)
test = pack('!BBHfII', 129, 26, 1234, 0.033, 11112222, 19216811)
print(test)
test_unpack = unpack('!BBHfII', test)
print(test_unpack)

# The mainloop is keeping the window on the screen
root.mainloop()
