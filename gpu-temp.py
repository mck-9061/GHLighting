import GPUtil
import serial
import time
import threading

port = serial.Serial('COM21', 9600)


def read_port():
    while 1:
        print(str(port.readline()))
        continue


time.sleep(4)

port.write(b'a')
print("Written")
while True:
    got = str(port.readline())
    if "OK" in got:
        print("Good to go!")
        break

threading.Thread(target=read_port).start()

port.write(b'0')
port.write(b'\x00')

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

lastValue = 90

while True:
    time.sleep(0.1)
    gpu = GPUtil.getGPUs()[0]
    print(gpu.temperature)

    c = 90 - translate(gpu.load, 0, 1, 0, 90)
    if c < 0:
        c = 0
    print(c)

    colour = 0
    if c > lastValue:
        colour = lastValue + 1
    elif c < lastValue:
        colour = lastValue - 1
    else:
        colour = lastValue

    lastValue = colour



    port.write(b'0')

    a = bytes(chr(colour), "utf-8")

    port.write(bytes(chr(colour), "utf-8")[-1:])

    print(bytes(chr(colour), "utf-8")[-1:])
    print(bytes(chr(colour), "utf-8"))
    print(len(a))
    print(gpu.load)
