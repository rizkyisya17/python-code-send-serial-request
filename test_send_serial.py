import requests
import time
import serial
from requests.auth import HTTPBasicAuth

def send_data(data):
    url = f"http://localhost:8080/serial/{data}"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(url, headers=headers)  # Change to POST if needed
        print(f"Sent data: {data}, Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

def connect_to_weight_bridge(port, baudrate=9600, timeout=1):
    try:
        # Establish a serial connection
        ser = serial.Serial(port, baudrate, timeout=timeout)
        ser.reset_input_buffer()  # Clear input buffer after connection
        print(f"Connected to weight bridge on {port} at {baudrate} bps")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to the weight bridge: {e}")
        return None

def read_weight(ser):
    try:
        ser.reset_input_buffer()  # Clear input buffer after connection
        # Send a command to read weight (this may vary based on your device's protocol)
        ser.write(b'STATUS\n')  # Replace with the actual command as per device protocol

        # Wait for a response
        time.sleep(0.5)
        
        # Read response from weight bridge
        response = ser.readline().decode('utf-8').strip()
        return response
    except Exception as e:
        print(f"Error reading weight: {e}")
        return None

def main():
    # data_value = 0  # Initialize your data value
    port = 'COM5'  # Replace with your serial port (e.g., '/dev/ttyUSB0' on Linux)
    weight_bridge = connect_to_weight_bridge(port)

    if weight_bridge:
        try:
            while True:
                weight = read_weight(weight_bridge)
                parts = weight.split()
                if weight:
                    try:
                        data_to_send = parts[1] + ' ' + parts[2]
                    except IndexError:
                        data_to_send = "0"
                    # print(data_to_send)
                    send_data(data_to_send)
                # data_value += 1  # Update your data as needed
                # time.sleep(1)  # Wait for 5 seconds before sending the next data
        except KeyboardInterrupt:
            print("\nScript interrupted by user. Exiting...")

if __name__ == "__main__":
    main()