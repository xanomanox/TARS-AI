import board
import busio
import adafruit_max9744


I2C_BUS = 1
I2C_ADDRESS = 0x4B
MIN_VOLUME = 0
MAX_VOLUME = 63
"""
PACKAGE DEPENDENCIES:
apt: python3-smbus, i2c-tools these are the same required for servo control.
pip: adafruit-blinka, adafruit-circuitpython-max9744  | TODO: add these to requirements.txt
"""
def set_volume(amp: adafruit_max9744.MAX9744, volume):
    """
    sets amp volume via i2c
    """
    amp.volume = volume

def main():
    #initialize i2c
    try:
        bus = busio.I2C(board.SCL, board.SDA)
        amp = adafruit_max9744.MAX9744(bus, address=I2C_ADDRESS)
    except FileNotFoundError:
        print(f"no device found")

    while True:
        print("\n==== MAX9744 VOL TEST CONTROL ====")
        print("1. set volume")
        print("2. exit")

        choice = input("Choice: ").strip()

        if choice =='1':
            volume_str = input(f"Enter volume ({MIN_VOLUME}-{MAX_VOLUME}):").strip()

            if not volume_str.isdigit():
                print("error: not an int")
                continue
            volume_val = int(volume_str)

            if volume_val < MIN_VOLUME or volume_val > MAX_VOLUME:
                print(f"Error: value out of range")

            try:
                set_volume(amp, volume_val)
                print(f"Volume set to {volume_val}")
            except IOError as e:
                print(f"Error writing to i2c device {e}")
        elif choice == '2':
            print("Exiting app")
            break
        else:
            print("Invalid choice. Try again")
if __name__ == "__main__":
    main()

