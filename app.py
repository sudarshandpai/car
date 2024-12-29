from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Replace this with your ESP32's actual IP address that you saw in the Serial Monitor
# For example: ESP32_IP = "192.168.1.100"
ESP32_IP = "192.168.29.83"  # ← Change this to your ESP32's IP address

def send_command_to_esp32(endpoint):
    try:
        url = f"http://{ESP32_IP}/{endpoint}"
        print(f"Sending request to: {url}")  # Debug print
        response = requests.get(url, timeout=5)  # Added timeout
        print(f"Response received: {response.text}")  # Debug print
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {str(e)}")  # Debug print
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/move/<direction>')
def move(direction):
    if direction not in ['front', 'back', 'left', 'right', 'stop']:
        return jsonify({'status': 'Invalid command'})
    
    response = send_command_to_esp32(direction)
    return jsonify({'status': response})

@app.route('/sensors')
def get_sensors():
    try:
        response = requests.get(f"http://{ESP32_IP}/sensors", timeout=5)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Sensor error: {str(e)}")  # Debug print
        return jsonify({
            'temperature': 'Error',
            'humidity': 'Error',
            'mqValue': 'Error'
        })

if __name__ == '__main__':
    print(f"Attempting to connect to ESP32 at: {ESP32_IP}")
    app.run(debug=True, host='0.0.0.0', port=5000)