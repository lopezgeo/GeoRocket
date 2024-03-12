import datetime
import requests
from GeoRocket_randNum import generate_random_temperature
import subprocess
import time
import threading
import math
import matplotlib.pyplot as plt

#GET CURRENT TIME AND USER LOCATION
def get_current_time_and_location():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current Time: {current_time}")

    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')

        print(f"Location: {city}, {region}, {country}")
    except Exception as e:
        print(f"Unable to retrieve real location. Error: {e}. Using default location: GeoRocket HQ")
    
#DISPLAY WELCOME MESSAGE (GEOROCKET)    
def display_welcome_message():
    print("Welcome to the GeoRocket Simulator!\n")
    get_current_time_and_location()

#GET USER INPUT FOR ROCKET HEIGHT
def get_rocket_height():
    while True:
        try:
            rocket_height = float(input("\nEnter rocket height (between 50 to 150 meters): "))
            if 50 <= rocket_height <= 150:
                return rocket_height
            else:
                print("Error: The average rocket height is between 50 to 150 meters.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

#GET USER INPUT FOR BOOSTER COUNT
def get_booster_count():
    while True:
        try:
            booster_count = int(input("Enter booster count (0 or 2): "))
            if booster_count == 0 or booster_count == 2:
                return booster_count
            else:
                print("Please enter a valid value for booster count (0 or 2).")
        except ValueError:
            print("Invalid input. Please enter an integer value.")

#GET USER INPUT FOR FUEL AMOUNT
def get_fuel_amount():
    while True:
        try:
            fuel_amount = float(input("Enter fuel amount (between 550,000 to 3,500,000 gallons): "))
            if 550000 <= fuel_amount <= 3500000:
                return fuel_amount
            else:
                print("Error: The average fuel amount is between 550,000 to 3,500,000 gallons.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

#GET USER INPUT FOR PAYLOAD TYPE
def get_payload_type():
    payload_options = ['satellite', 'space probe', 'humans']

    while True:
        payload_type = input(f"Choose payload type ({', '.join(payload_options)}): ").lower()
        if payload_type in payload_options:
            if payload_type == 'satellite':
                return get_satellite_size()
            elif payload_type == 'humans':
                return get_human_count()
            else:
                return payload_type
        else:
            print("Error: Please choose a valid payload type.")

#IF USER WANTS SATELLITE PAYLOAD, CHOOSE SIZE
def get_satellite_size():
    satellite_weights = {
        'micro': 1106,
        'mini': 401,
        'small': 901,
        'medium': 1851,
        'intermediate': 3351,
        'large': 4601,
        'heavy': 6001,
        'extra heavy': 7000
    }

    while True:
        print("Satellite Size Options:")
        for size in satellite_weights:
            print(f"- {size.capitalize()}")

        chosen_size = input("Choose satellite size: ").lower()

        if chosen_size in satellite_weights:
            weight = satellite_weights[chosen_size]
            print(f"The weight of the {chosen_size.capitalize()} satellite is {weight} kg.")
            confirmation = input("Is this size fine? (yes/no): ").lower()

            if confirmation == 'yes':
                return chosen_size
            elif confirmation == 'no':
                print("Choose a different satellite size.")
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            print("Error: Please choose a valid satellite size.")

#IF USER WANTS HUMAN PAYLOAD, CHOOSE HUMAN COUNT (MAX 20)
def get_human_count():
    while True:
        try:
            human_count = int(input("Enter the number of humans (up to 20): "))
            if 0 <= human_count <= 20:
                return human_count
            else:
                print("Error: Please enter a valid count (up to 20).")
        except ValueError:
            print("Invalid input. Please enter an integer value.")

#DISPLAY AN INFORMAL AGREEMENT STATEMENT IF USER WISHES TO BEGIN
def get_user_agreement():
    user_response = input("\nDo you agree to proceed? (yes/no): ").lower()
    return user_response == "yes"

#GET USER INPUT FOR LAUNDH LOCATION
def get_launch_location():
    launch_locations = ['cape canaveral', 'boca chica', 'vandenberg']

    while True:
        chosen_location = input(f"Choose launch location ({', '.join(launch_locations)}): ").lower()
        if chosen_location in launch_locations:
            return chosen_location
        else:
            print("Error: Please choose a valid launch location.")

#SAVE DATA INFORMATION IN NEW FILE        
def save_user_inputs(rocket_height, booster_count, fuel_amount, payload_type, escape_time, total_weight, satellite_size=None, human_count=None, launch_location=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fuel_amount_gallons = fuel_amount * 264.172  # Conversion from liters to gallons

    with open("rocket_design_document.txt", "w") as file:
        file.write("GeoRocket Rocket Design Document\n")
        file.write(f"Timestamp: {timestamp}\n\n")
        file.write("Rocket Simulation Parameters:\n")
        file.write(f"Rocket Height: {rocket_height} meters\n")
        file.write(f"Booster Count: {booster_count}\n")

        booster_weight = booster_count * 192000  # Assuming each booster weighs 192000 lbs
        file.write(f"Total Booster Weight: {booster_weight} lbs\n")

        file.write(f"Fuel Amount: {fuel_amount_gallons:.2f} gallons\n")
        file.write(f"Payload Type: {payload_type}\n")

        if payload_type == 'satellite' and satellite_size is not None:
            file.write(f"Satellite Size: {satellite_size.capitalize()}\n")
        elif payload_type == 'space probe':
            file.write("Space Probe Weight: 5000 kg\n")
        elif payload_type == 'humans' and human_count is not None:
            total_weight = human_count * 160  # Assuming the average weight of a human adult is 160 lbs
            file.write(f"Human Count: {human_count}\n".encode('utf-8'))
            file.write(f"Total Human Weight: {total_weight} lbs\n")

        if launch_location:
            file.write(f"Launch Location: {launch_location.capitalize()}\n")

        file.write("\nRocket Dimension Suggestions:\n")
        file.write("1. Consider optimizing fuel amount for maximum efficiency.\n")
        file.write("2. Evaluate payload weight and adjust force accordingly.\n")
        file.write("3. Ensure booster count aligns with mission requirements.\n")
        
        file.write("\nRocket Simulation Results:\n")
        file.write(f"Time to reach escape velocity: {escape_time:.2f}")

mp3_file_path = '/Users/geolopez/Downloads/launch_countdown.mp3'

#PLAY AUDIO
def play_audio(file_path):
    subprocess.run(['afplay', file_path], check=True)

#RUN COUNTDOWN INCLUDING SOUND
def countdown_with_sound():
    def countdown():
        for i in range(10, -1, -1):
            print(f"Time left: {i} seconds")
            time.sleep(1)

    def play_sound():
        play_audio(mp3_file_path)

    countdown_thread = threading.Thread(target=countdown)
    sound_thread = threading.Thread(target=play_sound)

    countdown_thread.start()
    sound_thread.start()

    countdown_thread.join()
    sound_thread.join()

    print("Liftoff!")

#CALCULATE TIME TO REACH ESCAPE VELOCITY
def time_to_escape_velocity(total_weight):
    gravitational_constant = 9.81  # Gravitational constant in meters/second^2
    escape_velocity = math.sqrt(2 * gravitational_constant * total_weight)
    return escape_velocity / gravitational_constant
       
#CREATE GRAPH FOR TIME TO REACH ESCAPE VELOCITY 
def plot_escape_velocity(total_weight):
    # create list for time values
    time_values = list(range(0, 11))
    velocity_values = [math.sqrt(2 * 9.81 * total_weight * t) for t in time_values]

    plt.plot(time_values, velocity_values)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Escape Velocity (meters/second)')
    plt.title('Rocket Escape Velocity')

    # Display the plot in the terminal
    plt.show()

#MAIN FUNCTION
def main():
    display_welcome_message()

    while True:
        if get_user_agreement():
            rocket_height = get_rocket_height()
            booster_count = get_booster_count()
            fuel_amount = get_fuel_amount()
            payload_type = get_payload_type()
            chosen_location = get_launch_location()
            total_weight = 2340000 + booster_count * 192000 + fuel_amount
            escape_time = time_to_escape_velocity(total_weight)

            print("\nRocket Simulation Parameters:\n")
            print(f"Rocket Height: {rocket_height} meters")
            print(f"Booster Count: {booster_count}")
            print(f"Fuel Amount: {fuel_amount} liters")
            print(f"Payload Type: {payload_type}")
            print(f"Launch Location: {chosen_location}")
            random_temperature = generate_random_temperature()
            print(f"Launch Set: {random_temperature:.0f}\u00b0 F")
            print("\nYour Launch is successful! Congratulations and God Speed!")

            save_user_inputs(
                rocket_height,
                booster_count,
                fuel_amount,
                payload_type,
                escape_time, 
                total_weight,
                satellite_size=get_satellite_size() 
                if payload_type == 'satellite' 
                else None,
                human_count=get_human_count() 
                if payload_type == 'humans' 
                else None,
                launch_location=chosen_location
            )

            break
        else:
            print("Thanks for your time! If you change your mind, feel free to restart the simulation.")

    print("\nCountdown....\n")

    # Sleep for 5 seconds
    time.sleep(5)

    # Countdown and play audio
    countdown_with_sound()

    # Calculate the time to reach escape velocity
    print(f"\nTime to reach escape velocity: {escape_time:.2f} seconds")

    # Plot escape velocity graph
    plot_escape_velocity(total_weight)

if __name__ == "__main__":
    main()