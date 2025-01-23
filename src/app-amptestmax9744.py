import smbus
import sys

I2C_BUS = 1
I2C_ADDRESS = 0x40
MIN_VOLUME = 0
MAX_VOLUME = 63
"""
In the TARS system, volume control is not set 
"""
def set_volume(bus, volume):
    """
    sets amp volume via i2c
    """
    register = 0x00
    bus.write_byte_data(I2C_ADDRESS,register,volume)

def main():
    #initialize i2c
    try:
        bus = smbus.SMBus(I2C_BUS)
    except FileNotFoundError:
        print(f"no device found")

    while True:
        print("\n==== MAX9744 VOL CONTROL")
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
                set_volume(bus, volume_val)
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

