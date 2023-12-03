import serial
import time
from inputs import devices, get_gamepad
import threading
# from mss.windows import MSS as mss
from mss import mss, tools

port = serial.Serial('COM21', 9600)


def read_port():
    while 1:
        print(str(port.readline()))
        continue


global positions


def update_positions():
    global positions
    count = 1
    file = open("positions.csv", encoding="utf8").readlines()
    line = file[count]
    positions = []
    for num in line.split(","):
        positions.append(int(num.replace("\n", "")))
    print(positions)
    while True:
        input()
        count += 1
        if count > 4:
            count = 1
        print("Changed to " + str(count) + " player(s).")

        line = file[count]
        positions = []
        for num in line.split(","):
            positions.append(int(num.replace("\n", "")))
        print(positions)


global star
star = False
global aStar
aStar = False
global dStar
dStar = False


def star_power():
    global star
    global aStar
    global dStar
    global positions
    with mss() as sct:
        while True:
            # Check star power
            # px = ImageGrab.grab().load()
            # pixel = px[1242, 814]
            # pixel = getpixelcolor.pixel(1242, 814)
            # monitor = {'top':0, 'left':0, 'width':1920, 'height':1080, 'mon':1}
            monitor = {'top': positions[8], 'left': positions[7], 'width': 1, 'height': 1, 'mon': 1}

            output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

            # Grab the data
            sct_img = sct.grab(monitor)

            # Save to the picture file
            # tools.to_png(sct_img.rgb, sct_img.size, output=output)
            # print(output)

            pixel = sct_img.pixel(0, 0)
            # print(pixel)

            if (pixel[0] > 80 or pixel[1] > 80 or pixel[2] > 80) and not star:
                aStar = True
                star = True
                print("Star power activated!")

            elif pixel[0] <= 80 and pixel[1] <= 80 and pixel[2] <= 80 and star:
                dStar = True
                star = False
                print("Star power deactivated.")

            time.sleep(0.5)


global green
global red
global yellow
global blue
global orange

green = [0, 255, 0]
red = [255, 0, 0]
yellow = [255, 255, 0]
blue = [0, 0, 255]
orange = [255, 179, 0]


def get_colours():
    global green
    global red
    global yellow
    global blue
    global orange
    global positions

    with mss() as sct:
        monitor = {'top': positions[1], 'left': 0, 'width': 1920, 'height': 1, 'mon': 1}

        output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

        sct_img = sct.grab(monitor)

        green = sct_img.pixel(positions[2], 0)
        red = sct_img.pixel(positions[3], 0)
        yellow = sct_img.pixel(positions[4], 0)
        blue = sct_img.pixel(positions[5], 0)
        orange = sct_img.pixel(positions[6], 0)

        print(green)
        print(red)
        print(yellow)
        print(blue)
        print(orange)


def check_current_song():
    global green
    global red
    global yellow
    global blue
    global orange

    # Use the current song file to determine if we're in a game or not
    lastContents = ""

    while True:
        time.sleep(1)
        f = open("C:\\Program Files\\ScoreSpy Launcher\\GameData\\100\\currentsong.txt", encoding="utf8").read()
        # f = open("C:\\Users\\natha\\OneDrive\\Documents\\Clone Hero\\currentsong.txt", encoding="utf8").read()
        if not f == lastContents:
            print("State changed")
            lastContents = f
            if f == "":
                # No longer in song, use default colours
                print("Menu")
                green = [0, 255, 0]
                red = [255, 0, 0]
                yellow = [255, 255, 0]
                blue = [0, 0, 255]
                orange = [255, 179, 0]
            else:
                # Allow for loading time
                time.sleep(1)
                get_colours()


time.sleep(4)

port.write(b'a')
print("Written")
while True:
    got = str(port.readline())
    if "OK" in got:
        print("Good to go!")
        break

threading.Thread(target=read_port).start()
threading.Thread(target=check_current_song).start()
threading.Thread(target=update_positions).start()
time.sleep(3)
threading.Thread(target=star_power).start()

port.write(b'0')
port.write(b'\x00')

on = [0, 0, 0, 0, 0]


def set_all_leds():
    global green
    global red
    global yellow
    global blue
    global orange

    if on[0]:
        port.write(b'\x50')
        port.write(bytes(chr(green[0]), "utf-8")[-1:])
        port.write(bytes(chr(green[1]), "utf-8")[-1:])
        port.write(bytes(chr(green[2]), "utf-8")[-1:])
    if on[1]:
        port.write(b'\x50')
        port.write(bytes(chr(red[0]), "utf-8")[-1:])
        port.write(bytes(chr(red[1]), "utf-8")[-1:])
        port.write(bytes(chr(red[2]), "utf-8")[-1:])
    if on[2]:
        port.write(b'\x50')
        port.write(bytes(chr(yellow[0]), "utf-8")[-1:])
        port.write(bytes(chr(yellow[1]), "utf-8")[-1:])
        port.write(bytes(chr(yellow[2]), "utf-8")[-1:])
    if on[3]:
        port.write(b'\x50')
        port.write(bytes(chr(blue[0]), "utf-8")[-1:])
        port.write(bytes(chr(blue[1]), "utf-8")[-1:])
        port.write(bytes(chr(blue[2]), "utf-8")[-1:])
    if on[4]:
        port.write(b'\x50')
        port.write(bytes(chr(orange[0]), "utf-8")[-1:])
        port.write(bytes(chr(orange[1]), "utf-8")[-1:])
        port.write(bytes(chr(orange[2]), "utf-8")[-1:])


while True:
    if aStar:
        port.write(b'\x02')
        aStar = False
        continue
    if dStar:
        port.write(b'\x03')
        dStar = False
        continue
    if star:
        continue
    events = get_gamepad()
    s = True
    for event in events:
        if event.code == "BTN_SOUTH":
            if on[0]:
                on[0] = 0
            else:
                on[0] = 1
        elif event.code == "BTN_EAST":
            if on[1]:
                on[1] = 0
            else:
                on[1] = 1
        elif event.code == "BTN_NORTH":
            if on[2]:
                on[2] = 0
            else:
                on[2] = 1
        elif event.code == "BTN_WEST":
            if on[3]:
                on[3] = 0
            else:
                on[3] = 1
        elif event.code == "BTN_TL":
            if on[4]:
                on[4] = 0
            else:
                on[4] = 1
        else:
            s = False
    if s:
        set_all_leds()
