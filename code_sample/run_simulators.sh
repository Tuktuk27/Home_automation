#!/bin/bash

# Set the working directory to the script's directory
cd "/home/touktouk/Desktop/operating_system/Simulator_devices"

# File to store the PIDs of the running Flask applications
pid_file="flask_pids.txt"

# Create an empty PID file
> "$pid_file"

# Function to kill running Flask applications
kill_flask() {
    while IFS= read -r pid; do
        echo "Killing process $pid"
        kill "$pid"
    done < "$pid_file"

    # Remove the PID file if it exists
    if [ -e "$pid_file" ]; then
        rm "$pid_file"
    fi
}

# Run the Lamp Simulation on port 5001
python3 lamp_1_simulation.py &
echo $! >> "$pid_file"

# Run the Temperature Simulation on port 5002
python3 temperature_simulation.py &
echo $! >> "$pid_file"

# Run the Lamp Simulation on port 5003
python3 lamp_2_simulation.py &
echo $! >> "$pid_file"

# Run the Lamp Simulation on port 5004
python3 lamp_3_simulation.py &
echo $! >> "$pid_file"

# Run the House State Controller on port 5005
python3 house_simulation.py &
echo $! >> "$pid_file"

# Function to be executed when the script is interrupted or terminated
cleanup() {
    echo "Cleaning up..."
    kill_flask
    exit 1
}

# Register the cleanup function to be called on script termination
trap cleanup EXIT

# Keep the script running
read -rp "Press Enter to stop the simulations." key

# Stop the simulations when Enter is pressed
kill_flask
