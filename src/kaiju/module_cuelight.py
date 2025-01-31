import RPi.GPIO as GPIO

# Define the GPIO pin for the LED
LED_GPIO = 17  # Change if needed

# GPIO setup (runs when module is imported)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GPIO, GPIO.OUT, initial=GPIO.LOW)  # Ensure LED starts OFF

def turn_on():
    """Turn the LED ON."""
    GPIO.output(LED_GPIO, GPIO.HIGH)
    print(f"LED is now ON via GPIO pin{LED_GPIO}")

def turn_off():
    """Turn the LED OFF."""
    GPIO.output(LED_GPIO, GPIO.LOW)
    print("LED is now OFFvia GPIO pin{LED_GPIO}")

def cleanup():
    """Reset GPIO pins before exiting."""
    GPIO.cleanup()
    print(f"GPIO pin {LED_GPIO} cleanup done.")
