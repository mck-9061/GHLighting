import serial
import time
from inputs import devices, get_gamepad
import threading
# from mss.windows import MSS as mss
from mss import mss, tools
import colorsys

port = serial.Serial('COM9', 115200)


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
global inMenu
inMenu = True

global star_loop_active
star_loop_active = False

def star_power():
    global star
    global aStar
    global dStar
    global positions
    global inMenu
    global star_loop_active
    star_loop_active = True
    with mss() as sct:
        while True:
            time.sleep(0.4)
            if inMenu:
                print("In menu")
                break
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

            elif pixel[0] <= 80 and pixel[1] <= 80 and pixel[2] <= 80:
                dStar = True
                star = False
                print("Star power deactivated.")
                break
        star_loop_active = False



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

        g = sct_img.pixel(positions[2], 0)
        r = sct_img.pixel(positions[3], 0)
        y = sct_img.pixel(positions[4], 0)
        b = sct_img.pixel(positions[5], 0)
        o = sct_img.pixel(positions[6], 0)

        # Max out the saturation and value so it displays better
        # if not (g[0] == g[1] and g[1] == g[2]):
        #     hsv_value = colorsys.rgb_to_hsv(g[0]/float(255), g[1]/float(255), g[2]/float(255))
        #     new_rgb = colorsys.hsv_to_rgb(hsv_value[0], 1, 1)
        #     green = (int(new_rgb[0]*255), int(new_rgb[1]*255), int(new_rgb[2]*255))
        #
        # if not (r[0] == r[1] and r[1] == r[2]):
        #     hsv_value = colorsys.rgb_to_hsv(r[0]/float(255), r[1]/float(255), r[2]/float(255))
        #     new_rgb = colorsys.hsv_to_rgb(hsv_value[0], 1, 1)
        #     red = (int(new_rgb[0]*255), int(new_rgb[1]*255), int(new_rgb[2]*255))
        #
        # if not (y[0] == y[1] and y[1] == y[2]):
        #     hsv_value = colorsys.rgb_to_hsv(y[0]/float(255), y[1]/float(255), y[2]/float(255))
        #     new_rgb = colorsys.hsv_to_rgb(hsv_value[0], 1, 1)
        #     yellow = (int(new_rgb[0]*255), int(new_rgb[1]*255), int(new_rgb[2]*255))
        #
        # if not (b[0] == b[1] and b[1] == b[2]):
        #     hsv_value = colorsys.rgb_to_hsv(b[0]/float(255), b[1]/float(255), b[2]/float(255))
        #     new_rgb = colorsys.hsv_to_rgb(hsv_value[0], 1, 1)
        #     blue = (int(new_rgb[0]*255), int(new_rgb[1]*255), int(new_rgb[2]*255))
        #
        # if not (o[0] == o[1] and o[1] == o[2]):
        #     hsv_value = colorsys.rgb_to_hsv(o[0]/float(255), o[1]/float(255), o[2]/float(255))
        #     new_rgb = colorsys.hsv_to_rgb(hsv_value[0], 1, 1)
        #     orange = (int(new_rgb[0]*255), int(new_rgb[1]*255), int(new_rgb[2]*255))

        green = g
        red = r
        yellow = y
        blue = b
        orange = o


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
    global inMenu

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
                set_all_leds()
                inMenu = True
            else:
                # Allow for loading time
                time.sleep(1)
                get_colours()
                set_all_leds()
                inMenu = False


time.sleep(4)

while True:
    print("Waiting...")
    got = str(port.readline())
    if "OK" in got:
        print("Arduino connected")
        break

threading.Thread(target=read_port).start()
threading.Thread(target=check_current_song).start()
threading.Thread(target=update_positions).start()
time.sleep(3)
# threading.Thread(target=star_power).start()

on = [0, 0, 0, 0, 0]

def set_all_leds():
    global green
    global red
    global yellow
    global blue
    global orange

    port.write(b'\x00')
    port.write(b'\x04')
    port.write(green[0].to_bytes(1, 'big'))
    port.write(green[1].to_bytes(1, 'big'))
    port.write(green[2].to_bytes(1, 'big'))

    port.write(b'\x00')
    port.write(b'\x03')
    port.write(red[0].to_bytes(1, 'big'))
    port.write(red[1].to_bytes(1, 'big'))
    port.write(red[2].to_bytes(1, 'big'))

    port.write(b'\x00')
    port.write(b'\x02')
    port.write(yellow[0].to_bytes(1, 'big'))
    port.write(yellow[1].to_bytes(1, 'big'))
    port.write(yellow[2].to_bytes(1, 'big'))

    port.write(b'\x00')
    port.write(b'\x01')
    port.write(blue[0].to_bytes(1, 'big'))
    port.write(blue[1].to_bytes(1, 'big'))
    port.write(blue[2].to_bytes(1, 'big'))

    port.write(b'\x00')
    port.write(b'\x00')
    port.write(orange[0].to_bytes(1, 'big'))
    port.write(orange[1].to_bytes(1, 'big'))
    port.write(orange[2].to_bytes(1, 'big'))


def set_brightness(fret_num):
    port.write(b'\x01')
    port.write(bytes(chr(fret_num), "utf-8")[-1:])
    if on[fret_num]:
        port.write(b'\xFF')
    else:
        port.write(b'\x40')

# set_all_leds()

for i in range(5):
    set_brightness(i)

print("All systems go")

while True:
    if aStar:
        port.write(b'\x02')
        aStar = False
        continue
    if dStar:
        port.write(b'\x03')
        dStar = False
        # set_all_leds()
        continue
    if star:
        continue
    events = get_gamepad()

    for event in events:
        # print(event.code)
        if event.code == "BTN_SOUTH":
            on[4] = not on[4]
            set_brightness(4)
        elif event.code == "BTN_EAST":
            on[3] = not on[3]
            set_brightness(3)
        elif event.code == "BTN_NORTH":
            on[2] = not on[2]
            set_brightness(2)
        elif event.code == "BTN_WEST":
            on[1] = not on[1]
            set_brightness(1)
        elif event.code == "BTN_TL":
            on[0] = not on[0]
            set_brightness(0)
        elif event.code == "BTN_START" and not star_loop_active:
            print("Star pressed")
            threading.Thread(target=star_power).start()
