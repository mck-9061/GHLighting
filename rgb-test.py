import time
import serial
import threading


port = serial.Serial('COM9', 9600)


def read_port():
    while 1:
        print(str(port.readline()))
        continue

time.sleep(4)

while True:
    print("Waiting...")
    got = str(port.readline())
    if "OK" in got:
        print("Good to go!")
        break

time.sleep(1)

threading.Thread(target=read_port).start()

# 50(hex) - next 3 bytes are RGB values
port.write(b'\x00')
port.write(b'\xFF')
port.write(b'\xFF')
port.write(b'\xFF')

port.write(b'\x01')
port.write(b'\xFF')
port.write(b'\xFF')
port.write(b'\xFF')

port.write(b'\x02')
port.write(b'\xFF')
port.write(b'\xFF')
port.write(b'\xFF')

port.write(b'\x03')
port.write(b'\xFF')
port.write(b'\x00')
port.write(b'\x00')

port.write(b'\x04')
port.write(b'\xFF')
port.write(b'\xFF')
port.write(b'\xFF')

print("done")

