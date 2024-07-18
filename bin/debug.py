import time
import sys
import RPi.GPIO as GPIO

# GPIO pin setup
DT_PIN = 5  # Data output pin
SCK_PIN = 6  # Clock pin

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(SCK_PIN, GPIO.OUT)

def read_data():
    count = 0
    GPIO.output(SCK_PIN, False)  # Pull SCK low to start data read

    # Wait until the DT_PIN goes low
    while GPIO.input(DT_PIN) == 1:
        pass

    # Read 24-bit data from the HX711
    for _ in range(24):
        GPIO.output(SCK_PIN, True)
        count = count << 1  # Shift left to make room for the next bit
        GPIO.output(SCK_PIN, False)
        if GPIO.input(DT_PIN) == 1:
            count += 1  # If the DT_PIN is high, set the bit to 1

    # Set the channel and gain factor (1, 2, or 3)
    GPIO.output(SCK_PIN, True)
    count = count ^ 0x800000  # Convert from 2's complement
    GPIO.output(SCK_PIN, False)

    return count

def diagnostic_test():
    print("Starting HX711 diagnostic test...")
    time.sleep(1)

    for i in range(10):
        try:
            data = read_data()
            print(f"Reading {i+1}: {data}")
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("Test interrupted by user.")
            sys.exit()
        except Exception as e:
            GPIO.cleanup()
            print(f"Error: {e}")
            sys.exit()

    GPIO.cleanup()
    print("Diagnostic test complete.")

if __name__ == "__main__":
    diagnostic_test()
