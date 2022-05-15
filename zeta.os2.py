#THIS IS THE LAPTOP
# Controller Garbage
from inputs import devices

for device in devices.gamepads:
    print(device)

from inputs import get_gamepad

import socket

ip = "192.168.0.190"  # IP of Raspberry Pi
cam_control = 0
BL = 0
BR = 0

# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, 8086))
print("CLIENT: connected")
while 1:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)
        # Test these lines to receive gps data.
        # from_server = client.recv(4096).decode()
        # print("Recieved: " + from_server)

        # Forward/Reverse Stick Control
        # Dear god can I organize all this? Maybe controller inputs can be handled in another script?
        if event.code == 'ABS_Y':
            if event.state in range(25001, 32767):
                print("Back Full Throttle")
                client.send("BFT".encode())
            if event.state in range(15000, 25001):
                print("Back Half Throttle")
                client.send("BHT".encode())
            if event.state in range(-32768, -25000):
                print("Forward Full Throttle")
                client.send("FFT".encode())
            if event.state in range(-25000, -14999):
                print("Forward Half Throttle")
                client.send("FHT".encode())
            if event.state in range(-14998, 15000):
                print("STOP Power")
                client.send("SP".encode())

        # Left/Right Steering Stick Control
        if event.code == 'ABS_RX':
            if event.state in range(25001, 32767):
                if cam_control == 0:
                    print("Right Turn Full")
                    client.send("RTF".encode())
                if cam_control == 1:
                    print("Cam Right Turn Full")
                    client.send("CRTF".encode())
            if event.state in range(15000, 25001):
                if cam_control == 0:
                    print("Right Turn Half")
                    client.send("RTH".encode())
                if cam_control == 1:
                    print("Cam Right Turn Half")
                    client.send("CRTH".encode())
            if event.state in range(-32768, -25000):
                if cam_control == 0:
                    print("Left Turn Full")
                    client.send("LTF".encode())
                if cam_control == 1:
                    print("Cam Left Turn Full")
                    client.send("CLTF".encode())
            if event.state in range(-25000, -14999):
                if cam_control == 0:
                    print("Left Turn Half")
                    client.send("LTH".encode())
                if cam_control == 1:
                    print("Cam Left Turn Half")
                    client.send("CLTH".encode())
            if event.state in range(-14998, 15000):  # This needs to be changed to specifically reset the steering servo
                if cam_control == 0:
                    print("STOP Turn")
                    client.send("ST".encode())
                if cam_control == 1:
                    print("Cam Stop Turn")
                    client.send("CST".encode())

        # ABXY BUTTONS
        if event.code == 'BTN_SOUTH' and event.state == 1:
            print("a")

        if event.code == 'BTN_EAST' and event.state == 1:
            print("b")

        # EMERGENCY BRAKES
        if event.code == 'BTN_WEST' and event.state == 1:
            print("Y - EMERGENCY STOP")
            client.send("STOP".encode())

        # BUMPERS LEFT AND RIGHT / HEADLIGHTS
        if event.code == 'BTN_TL' and event.state == 1:
            if BL == 0:
                print("Turning L light to half")
                BL = 1
                client.send("LLH".encode())
            elif BL == 1:
                print("Turning L light to full")
                BL = 2
                client.send("LLF".encode())
            elif BL == 2:
                print("Turning L light off")
                BL = 0
                client.send("LLO".encode())
        if event.code == 'BTN_TR' and event.state == 1:
            if BR == 0:
                print("Turning R light to half")
                BR = 1
                client.send("RLH".encode())
            elif BR == 1:
                print("Turning R light to full")
                BR = 2
                client.send("RLF".encode())
            elif BR == 2:
                print("Turning R light off")
                BR = 0
                client.send("RLO".encode())


        if event.code == 'ABS_Z' and event state == 500:
            print('Left Trigger')
        if event.code == 'ABS_RZ' and event.state == 500:
            print('Right Trigger')
            # Range is 0 to 0-1023


# USE THIS TO RECEIVE GPS DATA
# receive a message and print it
# from_server = client.recv(4096).decode()
# print("Received: " + from_server)

# exit
client.close()

