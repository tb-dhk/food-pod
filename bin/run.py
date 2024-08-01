import subprocess
import time
import sys
from datetime import datetime
import RPi.GPIO as GPIO
from hx711 import HX711
import cv2
import os
import numpy as np
from ultralytics import YOLO
import pyodbc
import dotenv
from collections import deque
import threading

dotenv.load_dotenv(".env")

def log_message(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"[{log_time}] {message.lower()}")

log_message("startup commenced.")

def sql_log_message(cnxn, message):
    cursor = cnxn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    cursor.execute("""
        INSERT INTO BinStatus (bin_id, status, timestamp)
        VALUES (?, ?, ?)
    """, (0, message.lower(), time_now))
    cnxn.commit()

def initialize_gpio_with_timeout(timeout=10):
    def init_gpio():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        global hx
        hx = HX711(dout=DT_PIN, pd_sck=SCK_PIN, gain=128)

    gpio_thread = threading.Thread(target=init_gpio)
    gpio_thread.start()
    gpio_thread.join(timeout)

    if gpio_thread.is_alive():
        log_message("GPIO initialization timeout.")
        sql_log_message(cnxn, "GPIO initialization timeout.")
        clean_and_exit()

DT_PIN = 5
SCK_PIN = 6

def clean_and_exit(cnxn=None):
    log_message("Cleaning...")
    if cnxn:
        sql_log_message(cnxn, "Cleaning...")
    GPIO.cleanup()
    log_message("Bye!")
    if cnxn:
        sql_log_message(cnxn, "Bye!")
    sys.exit()

def zero_scale():
    log_message("Taring scale...")
    hx.tare()  # Tare the HX711
    log_message("Tare done!")
    log_message(f"offset set to {hx.OFFSET}.")

def take_picture():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(os.getcwd(), "images", f"{timestamp}.jpg")
    command = ["libcamera-still", "-o", filename, "--vflip", "-n"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    log_message(f"Picture taken and saved as {filename}")
    log_message("Waiting for weight change...")

def get_latest_pictures(directory, num_pictures=2):
    files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jpg") and "-diff" not in f], key=os.path.getmtime, reverse=True)
    return files[:num_pictures]

def find_differences(image1, image2):
    diff = cv2.absdiff(image1, image2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    # Create an image to hold only the different pixels from image2
    diff_pixels = np.zeros_like(image2)
    diff_pixels[thresh != 0] = image2[thresh != 0]
    
    return diff_pixels

def detect_food(image_path):
    model_weights = "../model/models/food-detection/yolo_v8_v0.2.pt"
    model = YOLO(model_weights)
    results = model(image_path)
    results[0].save(filename=image_path.split(".")[0] + "-detected.jpg")
    return results[0].boxes

def convert_results_to_area_dict(boxes):
    area_dict = {}

    for i in range(len(boxes.xyxy)):
        cls = int(boxes.cls[i].item())
        xyxy = boxes.xyxy[i].detach().cpu().numpy()

        area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])

        if cls in area_dict:
            area_dict[cls] += area
        else:
            area_dict[cls] = area

    return area_dict

def monitor_weight(cnxn):
    weight_buffer = deque(maxlen=5)
    significant_change_threshold = 1

    prev_weight = hx.get_weight()
    weight_buffer.append(prev_weight)
    time.sleep(1)

    calibration_factor = float(os.getenv("CALIBRATION_FACTOR"))

    while True:
        current_weight = hx.get_weight()
        weight_buffer.append(current_weight)

        average_weight = sum(weight_buffer) / len(weight_buffer)
        calibrated_average_weight = average_weight / calibration_factor
        calibrated_prev_weight = prev_weight / calibration_factor
        weight_change = calibrated_average_weight - calibrated_prev_weight
        log_message(f"Waiting for weight change (calibrated average now {calibrated_average_weight}) (calibrated change {weight_change})...")

        if abs(weight_change) > significant_change_threshold:
            log_message("Significant weight change detected.")
            take_picture()
            pics = get_latest_pictures("images")
            if len(pics) >= 2:
                log_message(f"Found {len(pics)} latest pictures.")
                image1 = cv2.imread(pics[1])
                image2 = cv2.imread(pics[0])

                log_message(f"Calculating difference mask between {pics[0]} and {pics[1]}...")
                diff_mask = find_differences(image1, image2)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                diff_filename = f"images/{timestamp}-diff.jpg"
                cv2.imwrite(diff_filename, diff_mask)

                log_message(f"Detecting food from differences image ({diff_filename})...")
                results = detect_food(diff_filename)
            elif len(pics) == 1:
                log_message("Less than two pictures available, detecting food from new picture...")
                results = detect_food(pics[0])
            else:
                log_message("No images in directory. Taking first picture...")

            with cnxn:
                cursor = cnxn.cursor()

                results = convert_results_to_area_dict(results)

                total_area = sum(results.values())
                total_weight = weight_change

                raw_weights_dict = {}
                total_raw_weight = 0

                for cls in results:
                    cursor.execute(f"SELECT density FROM Food WHERE id = {cls}")
                    row = cursor.fetchone()
                    if row:
                        density = float(row[0])
                        area = results[cls]
                        height = 2
                        raw_weight = area * height * density
                        total_raw_weight += raw_weight
                        raw_weights_dict[cls] = raw_weight

                conversion_factor = total_weight / total_raw_weight if total_raw_weight else 0

                adjusted_weights_dict = {cls: weight * conversion_factor for cls, weight in raw_weights_dict.items()}

                log_message(f"results: {results}")
                log_message(f"weights: {adjusted_weights_dict}")

                with open(pics[1], 'rb') as file:
                    pic_bin = file.read()

                with open(pics[0], 'rb') as file:
                    pic_new = file.read()

                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                    INSERT INTO Logs (time, bin_id, picture_of_bin, filtered_picture_of_new_food, dictionary_of_estimated_amts_of_food, change_in_weight)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (time_now, 0, pyodbc.Binary(pic_bin), pyodbc.Binary(pic_new), str(adjusted_weights_dict), weight_change))
                cnxn.commit()

        prev_weight = average_weight
        time.sleep(0.5)

def sql_login():
    server = 'food-pod.database.windows.net'
    database = 'food-pod'
    username = 'foodpod'
    password = os.getenv("SQL_PASSWORD")
    driver = '{ODBC Driver 18 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+',1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn

while True:
    try:
        cnxn = sql_login()
        sql_log_message(cnxn, "code succesfully started.")
        initialize_gpio_with_timeout()
        zero_scale()
        log_message("Starting weight monitoring...")
        sql_log_message(cnxn, "Weight monitoring started.")
        monitor_weight(cnxn)
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit(cnxn)
    except Exception as e:
        log_message(f"Error occurred: {e}")
        sql_log_message(cnxn, f"Error occurred: {e}")
        time.sleep(5)

