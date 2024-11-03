# Download and unzip the latest version of ngrok
!wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip -O ngrok.zip
!unzip -o ngrok.zip
!chmod +x ./ngrok  # Ensure ngrok is executable

# Install Flask
!pip install flask

from flask import Flask, request, redirect, url_for, render_template, jsonify
import subprocess
import requests
import time
import atexit

# Start ngrok as a subprocess with inline auth token
ngrok_process = subprocess.Popen(['./ngrok', 'http', '5000', '--authtoken', '2o4pfmzyiwmBZcY4vhwQiYsOiJS_FsuQB2nueaQ863GcU2ya'])
time.sleep(3)  # Wait for ngrok to initialize

# Retrieve the public URL from ngrok’s local web interface
response = requests.get('http://localhost:4040/api/tunnels')
public_url = response.json()['tunnels'][0]['public_url']
print("Ngrok tunnel URL:", public_url)

# Initialize the Flask app
app = Flask(__name__, template_folder='/content/drive/MyDrive/Colab Notebooks/receipt_itemizer/templates/')

class RestaurantReceipt:
    def __init__(self):
        self.items = []
        self.eaters = set()
        self.receipt_name = ""

    def set_receipt_name(self, name):
        self.receipt_name = name

    def enter_eaters(self, eaters):
        self.eaters = {eater.strip().title() for eater in eaters.split(",")}

    def add_item(self, item_name, item_price, eaters_input):
        if eaters_input.strip().upper() == "ALL":
            eaters_list = list(self.eaters)
        else:
            eaters_list = [eater.strip().title() for eater in eaters_input.split(",") if eater.strip().title() in self.eaters]

        if not eaters_list:
            return "No valid eaters provided. Maybe you should invite them next time. No item added."

        self.items.append({
            'name': item_name,
            'price': item_price,
            'eaters': eaters_list
        })

    def calculate_total_sum(self):
        return sum(item['price'] for item in self.items)

    def calculate_per_person_share(self):
        per_person = {eater: 0 for eater in self.eaters}
        for item in self.items:
            split_cost = item['price'] / len(item['eaters'])
            for eater in item['eaters']:
                per_person[eater] += split_cost
        return per_person

    def display_receipt(self):
        return {
            "receipt_name": self.receipt_name,
            "items": self.items,
            "total_sum": self.calculate_total_sum(),
            "per_person_share": self.calculate_per_person_share()
        }

receipt_manager = RestaurantReceipt()

# Define Flask routes
@app.route('/')
def home():
    return redirect(url_for('receipt_manager_page'))

@app.route('/receipt_manager')
def receipt_manager_page():
    receipt_data = receipt_manager.display_receipt()
    return render_template('receipt_manager.html', receipt_data=receipt_data)

@app.route('/initialize_receipt', methods=['POST'])
def initialize_receipt():
    name = request.form['name']
    eaters = request.form['eaters']
    receipt_manager.set_receipt_name(name)
    receipt_manager.enter_eaters(eaters)
    return redirect(url_for('receipt_manager_page'))

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    try:
        item_price = float(request.form['item_price'])
    except ValueError:
        return jsonify({"error": "Invalid price format."}), 400
    eaters_input = request.form['eaters_input']
    result = receipt_manager.add_item(item_name, item_price, eaters_input)
    if result:
        return jsonify({"error": result}), 400
    return redirect(url_for('receipt_manager_page'))

# Ensure ngrok terminates when the app stops
atexit.register(ngrok_process.terminate)

# Run the app
if __name__ == "__main__":
    app.run(port=5000)
