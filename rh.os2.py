# THIS IS THE VEHICLE
import socket  # Python server socket module
from pydub import AudioSegment  # Welcome Audio
from pydub.playback import play  # Welcome Audio
import random  # Randomizer for welcome audio
import gpsd  # pip3 install gpsd-py3
import time  # importing for time delays
from datetime import datetime  # importing for time delays

gpsd.connect()

from adafruit_servokit import ServoKit

# Prepare the Servos
kit1 = ServoKit(channels=16)
# kit.servo[0].actuation_range = 270 # Servo activation range only needs to be around 90

cam_control = 0  # Setting default of camera turning to off so analog can be used for steering

from adafruit_motorkit import MotorKit  # Import basic motor info

kit = MotorKit()  # assigning bonnet I2C                  DEFAULT ADDRESS: 0x60
# kit2 = MotorKit(address=0x61) #assigning bonnet I2C
# from adafruit_motor import stepper # Prepare stepper motors
# KIT is headlights | KIT1 is Servo Control |

ip = "192.168.0.190"  # IP of Raspberry Pi -----UPDATE IP------

# start server
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((ip, 8080))  # 8080 probably occupied by MotionOS
serv.listen(5)
print("SERVER: started")

while True:
    # establish connection
    conn, addr = serv.accept()
    # from_client is blank so why have it?
    # from_client = ''
    print("SERVER: connection to Client established")

    welcome = random.randint(1, 7)
    if welcome == 1:
        play(AudioSegment.from_wav("TANK/Audio/Legion_Prime/WB1.wav"))
    if welcome == 2:
        play(AudioSegment.from_wav("TANK/Audio/Legion_Prime/WB2.wav"))
    if welcome == 3:
        play(AudioSegment.from_wav("TANK/Audio/Legion_Prime/WB3.wav"))
    if welcome == 4:
        play(AudioSegment.from_wav("TANK/Audio/Legion_Prime/WB4.wav"))
    if welcome == 5:
        play(AudioSegment.from_wav("TANK/Audio/Legion_Prime/WB5.wav"))
    if welcome == 6:
        play(AudioSegment.from_wav("TANK/Audio/Legion_Prime/WB6.wav"))
    if welcome == 7:
        play(AudioSegment.from_wav("TANK/Audio/Legion_Prime/WB7.wav"))

    while True:
        # receive data and print
        data = conn.recv(4096).decode()
        # Security Measure? VVV
        if not data:  # corrected break | Multiple statements, one line
            break

        # removing usage of from_client
        # from_client += data
        # print("Received: " + from_client)
        print("Received: " + data)

        # SEND GPS DATA
        # THIS IS UNTESTED AND THE WAIT TIMES MIGHT CARRY OVER TO OTHER CODE
        # while 1:
        # gps_data = gpsd.get_current()
        # conn.send(gps_data.encode())
        # time.sleep(5)
        # Headlights DON'T LET THESE GO NEGATIVE AS THAT WOULD REVERSE POLARITY
        if data == 'LLH':
            kit.motor3.throttle = 0.5
        if data == 'LLF':
            kit.motor3.throttle = 1
        if data == 'LLO':
            kit.motor3.throttle = 0

        if data == 'RLH':
            kit.motor4.throttle = 0.5
        if data == 'RLF':
            kit.motor4.throttle = 1
        if data == 'RLO':
            kit.motor4.throttle = 0
