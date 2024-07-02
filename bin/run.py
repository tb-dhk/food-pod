import subprocess
import time
import sys
from datetime import datetime
import RPi.GPIO as GPIO
import cv2
import os
import json
from ultralytics import YOLO

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for the HX711
DT_PIN = 5
SCK_PIN = 6

def createBoolList(size=8):
    return [False] * size

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        self.set_gain(gain)

    def is_ready(self):
        return GPIO.input(self.DOUT) == 0

    def set_gain(self, gain):
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2

        GPIO.output(self.PD_SCK, False)
        self.read()

    def read(self):
        while not self.is_ready():
            pass

        dataBits = [createBoolList(), createBoolList(), createBoolList()]

        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                GPIO.output(self.PD_SCK, True)
                dataBits[j][i] = GPIO.input(self.DOUT)
                GPIO.output(self.PD_SCK, False)

        GPIO.output(self.PD_SCK, True)
        GPIO.output(self.PD_SCK, False)

        if all(item == True for item in dataBits[0]):
            return self.lastVal

        bits = []
        for i in range(2, -1, -1):
            bits += dataBits[i]

        self.lastVal = int(''.join(map(str, bits)), 2)
        return self.lastVal

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)

# Initialize the HX711
hx = HX711(dout=DT_PIN, pd_sck=SCK_PIN)

def log_message(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\r[{log_time}] {message}")

def clean_and_exit():
    log_message("Cleaning...")
    GPIO.cleanup()
    log_message("Bye!\n")
    sys.exit()

def zero_scale():
    log_message("Taring scale...")
    hx.tare()  # Tare the HX711
    log_message("Tare done!\n")

def get_weight():
    try:
        weight = hx.get_units(5)
        return weight
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

def take_picture():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/home/pi/foodpod/{timestamp}.jpg"
    command = ["libcamera-still", "-o", filename, "--vflip", "-n"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    log_message(f"Picture taken and saved as {filename}")
    log_message("Waiting for weight change...")
    return filename

def get_latest_pictures(directory, num_pictures=2):
    files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jpg")], key=os.path.getmtime, reverse=True)
    return files[:num_pictures]

def find_differences(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    diff = cv2.absdiff(image1, image2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    return thresh

def detect_food(image_path):
    model_weights = "runs/detect/train/weights/best.pt"
    model = YOLO(model_weights)
    results = model(image_path)
    for result in results:
        result.show()

def monitor_weight():
    prev_weight = get_weight()
    time.sleep(1)  # Initial delay to allow for any transient readings
    log_message("\nWaiting for weight change...")
    while True:
        log_message(f"\rWaiting for weight change (now {prev_weight/17145})...")
        current_weight = get_weight()
        
        if abs(current_weight - prev_weight) > 0.01:  # Adjust the threshold as needed
            new_pic = take_picture()
            pics = get_latest_pictures("/home/pi/foodpod")
            if len(pics) >= 2:
                diff_image = find_differences(pics[0], pics[1])
                cv2.imwrite("/home/pi/foodpod/diff.jpg", diff_image)
                detect_food("/home/pi/foodpod/diff.jpg")
            else:
                detect_food(new_pic)
            prev_weight = current_weight
        
        time.sleep(1)

if __name__ == "__main__":
    zero_scale()  # Tare the scale to zero
    log_message("Starting weight monitoring...\n")
    
    try:
        monitor_weight()
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()
