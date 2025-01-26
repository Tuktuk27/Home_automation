#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, Toplevel, Canvas, PhotoImage
from PIL import Image, ImageTk
import subprocess
import threading
import time
import json
import os
from PIL import Image

# Set the working directory to the script's directory
os.chdir("/home/touktouk/Desktop/operating_system/Test_home_script")

# Global variables
lamp_on_1 = False
lamp_on_2 = False
lamp_on_3 = False
temperature = 20  # Initial temperature value
lamp_states = {}

# Initial state: House is unlocked
house_locked = False

# Global variable to store the last temperature set
last_temperature_set = temperature

# Function to handle button clicks
def on_button_click(driver, url, command):
    global last_temperature_set
    try:
        subprocess.run([f"./{driver}", f"{url},{command}"])
        # messagebox.showinfo("Driver Action", f"Driver action executed for URL: {url}")

        # Update the last temperature set when a new temperature is set
        if driver == "temperature_driver":
            last_temperature_set = float(command)
            update_last_temperature_label()

    except Exception as e:
        messagebox.showerror("Error", f"Error executing driver action: {str(e)}")

# Function to update the label with the last temperature set
def update_last_temperature_label():
    last_temperature_label.config(text=f"Last Temperature: {last_temperature_set}")


# Function to toggle lamp state and display light rays
def toggle_lamp(button, on_image, off_image, lamp_url, lamp_id):
    global lamp_states
    # Initialize the lamp state if it doesn't exist in the dictionary
    if lamp_id not in lamp_states:
        lamp_states[lamp_id] = False

    # Toggle the lamp state
    lamp_states[lamp_id] = not lamp_states[lamp_id]

    if lamp_states[lamp_id]:
        button.config(image=on_image)
        on_button_click("lamp_driver", lamp_url, "on")
    else:
        button.config(image=off_image)
        on_button_click("lamp_driver", lamp_url, "off")

# Function to open a thermostat control window
def open_thermostat_control():
    global temperature
    thermostat_control_window = Toplevel(window)
    thermostat_control_window.title("Thermostat Control")

    # Center the thermostat control window on the screen
    window_width = thermostat_control_window.winfo_reqwidth()
    window_height = thermostat_control_window.winfo_reqheight()
    screen_width = thermostat_control_window.winfo_screenwidth()
    screen_height = thermostat_control_window.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    thermostat_control_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a scale (slider) for temperature control
    temperature_scale = tk.Scale(
        thermostat_control_window,
        from_=10,
        to=30,
        orient=tk.HORIZONTAL,
        label="Adjust Temperature",
        variable=tk.DoubleVar(value=temperature),
        resolution=0.5,
    )
    temperature_scale.pack(padx=20, pady=20)

    # Function to update the global temperature variable
    def update_temperature(value):
        global temperature
        temperature = value

    temperature_scale.config(command=lambda value: update_temperature(float(value)))

    # Bind the cursor movement event to update the temperature continuously
    def update_temperature_continuous(event):
        value = temperature_scale.get()
        update_temperature(value)

    temperature_scale.bind("<Motion>", update_temperature_continuous)

    # Function to handle the validation button click
    def validate_temperature():
        on_button_click("temperature_driver", "http://10.0.2.15:5002/temperature", str(temperature))  # Replace "thermostat_url" with actual thermostat URL
        print(f"New temperature: {temperature}")
        thermostat_control_window.destroy()

    # Create a validation button
    validate_button = tk.Button(thermostat_control_window, text="Validate", command=validate_temperature)
    validate_button.pack(pady=10)


def update_current_temperature():
    while True:
        try:
            result = subprocess.run(["./thermostat_state", "http://10.0.2.15:5002/temperature"], capture_output=True, text=True)
            print("Received JSON response from thermostat_state:", result.stdout)

            # Check if the subprocess run was successful
            if result.returncode == 0:
                # Try to parse the JSON response
                try:
                    temperature_data = result.stdout.strip()
                    temperature_json = json.loads(temperature_data)
                    temperature_setpoint = temperature_json.get("temperature_setpoint")

                    # Check if the temperature_setpoint is present in the response
                    if temperature_setpoint is not None:
                        current_temperature_label.config(text=f"Current house temperature: {temperature_setpoint} °C")

                        # Check if the temperature is below 14 or above 28
                        if float(temperature_setpoint) < 14 or float(temperature_setpoint) > 28:
                            # Set the temperature back to 20 degrees
                            on_button_click("temperature_driver", "http://10.0.2.15:5002/temperature", "20.0")

                            # Display a message
                            messagebox.showwarning("Extreme Temperature", "Temperature quite extreme. Please keep reasonable settings.")
                            print("Temperature quite extreme. Please keep reasonable settings.")
                    else:
                        print(f"Error: 'temperature_setpoint' not found in response: {temperature_data}")
                except json.JSONDecodeError as json_error:
                    print(f"Error decoding JSON response: {json_error}")
            else:
                print(f"Error running subprocess: {result.stderr}")

        except Exception as e:
            print(f"Error updating temperature label: {e}")

        # Adjust the interval (in seconds) based on your preferences
        time.sleep(3)


# Start the thread to update the temperature label in the background
threading.Thread(target=update_current_temperature, daemon=True).start()

# Add this function to turn off all lamps and set the temperature back to 20 degrees
def reset_house():
    global temperature, lamp_states

    # Turn off all lamps
    lamp_states["lamp_1"] = False
    lamp_states["lamp_2"] = False
    lamp_states["lamp_3"] = False
    lamp1_button.config(image=lamp_off_image)
    on_button_click("lamp_driver", "http://10.0.2.15:5001/lamp_1", "off")
    lamp2_button.config(image=lamp_off_image)
    on_button_click("lamp_driver", "http://10.0.2.15:5003/lamp_2", "off")
    lamp3_button.config(image=lamp_off_image)
    on_button_click("lamp_driver", "http://10.0.2.15:5004/lamp_3", "off")

    # Set the temperature back to 20 degrees
    temperature = 20
    on_button_click("temperature_driver", "http://10.0.2.15:5002/temperature", "20.0")



# Function to lock the house
def lock_house(closed_locker_image, house_url):
    global house_locked

    house_locked = True

    # Turn off all lamps and Set the temperature back to 20 degrees
    reset_house()
    on_button_click("house_driver", house_url, "lock")
    # Update locker image
    locker_button.config(image=closed_locker_image)


# Function to unlock the house to be defined so house security is safe. Probably only possible using key (no home automation for this)
def unlock_house():
    global house_locked

    house_locked = False

    # Update locker image
    locker_label.config(image=open_locker_image)

# ...


# Create a simple GUI window
window = tk.Tk()
window.title("Home Automation Interface")
window.geometry("1000x800")  # Set a standard GUI size

# Load and configure the background image
background_image = Image.open("background.jpg")  # Replace with your background image
background_image = background_image.convert("RGBA")
background_image.putalpha(150)  # Adjust the transparency level (0: fully transparent, 255: fully opaque)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load locker images
open_locker_image = ImageTk.PhotoImage(Image.open("open_locker.png").resize((50, 50)))  # Resize to a standard size
closed_locker_image = ImageTk.PhotoImage(Image.open("closed_locker.png").resize((50, 50)))  # Resize to a standard size


# Load lamp images
lamp_on_image = ImageTk.PhotoImage(Image.open("lamp_on.jpg").resize((50, 50)))  # Resize to a standard size
lamp_off_image = ImageTk.PhotoImage(Image.open("lamp_off.jpg").resize((50, 50)))  # Resize to a standard size

# Create buttons for thermostat and lamps with corresponding URLs
thermostat_button = tk.Button(window, text="Thermostat", command=open_thermostat_control)

lamp1_button = tk.Button(window, bd=0, command=lambda: toggle_lamp(lamp1_button, lamp_on_image, lamp_off_image, "http://10.0.2.15:5001/lamp_1", "lamp_1"))
lamp1_button.image = lamp_off_image  # Store the image as an attribute
lamp1_button.config(image=lamp_off_image)

lamp2_button = tk.Button(window, bd=0, command=lambda: toggle_lamp(lamp2_button, lamp_on_image, lamp_off_image,"http://10.0.2.15:5003/lamp_2", "lamp_2"))
lamp2_button.image = lamp_off_image  # Store the image as an attribute
lamp2_button.config(image=lamp_off_image)

lamp3_button = tk.Button(window, bd=0, command=lambda: toggle_lamp(lamp3_button, lamp_on_image, lamp_off_image, "http://10.0.2.15:5004/lamp_3", "lamp_3"))
lamp3_button.image = lamp_off_image  # Store the image as an attribute
lamp3_button.config(image=lamp_off_image)

# Create a label for the locker
locker_button = tk.Button(window, bd=0, command=lambda: lock_house(closed_locker_image, "http://10.0.2.15:5005/house"))
locker_button.image = open_locker_image  # Store the image as an attribute
locker_button.config(image=open_locker_image)
locker_button.place(relx=0.9, rely=0.85, anchor="center")


# Create a button for resetting the house
reset_button = tk.Button(window, text="Reset House", command=reset_house)
reset_button.place(relx=0.5, rely=0.9, anchor="center")

# Place labels for rooms
tk.Label(window, text="Living Room").place(relx=0.2, rely=0.25, anchor="center")
tk.Label(window, text="Bedroom").place(relx=0.5, rely=0.25, anchor="center")
tk.Label(window, text="Bathroom").place(relx=0.8, rely=0.25, anchor="center")

# Create a label for the last temperature set
last_temperature_label = tk.Label(window, text=f"Last Temperature: {last_temperature_set}")
last_temperature_label.place(relx=0.5, rely=0.1, anchor="center")

# Place buttons for lamps and thermostat
thermostat_button.place(relx=0.5, rely=0.05, anchor="n")
lamp1_button.place(relx=0.2, rely=0.2, anchor="center")
lamp2_button.place(relx=0.5, rely=0.2, anchor="center")
lamp3_button.place(relx=0.8, rely=0.2, anchor="center")

# Create a label for the current house temperature
current_temperature_label = tk.Label(window, text="Current house temperature: N/A")
current_temperature_label.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()