import module_cuelight as cuelight  # Import the LED module

def main():
    """CLI menu for LED control."""
    while True:
        print("\n--- LED Control Menu ---")
        print("1. Turn ON LED")
        print("2. Turn OFF LED")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            cuelight.turn_on()
        elif choice == "2":
            cuelight.turn_off()
        elif choice == "3":
            print("Exiting...")
            cuelight.cleanup()  # Ensure GPIO resets before exit
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt...")
    finally:
        cuelight.cleanup()  # Ensure cleanup on forced exit
