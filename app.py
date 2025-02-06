from flask import Flask, request, redirect, url_for, render_template, jsonify, flash

# Initialize the Flask app

app = Flask(__name__, template_folder='templates')  # Ensure 'templates' folder is in the same directory

app.secret_key = "secret123"  # Replace with a secure key


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
            eaters_list = [
                eater.strip().title()
                for eater in eaters_input.split(",")
                if eater.strip().title() in self.eaters
            ]

        if not eaters_list:
            return "No valid eaters provided. Maybe you should invite them next time. No item added."

        self.items.append({
            "name": item_name,
            "price": item_price,
            "eaters": eater_list,
        })

    def remove_item(self, item_name):
        for item in self.items:
            if item["name"].lower() == item_name.lower():
                self.items.remove(item)
                return f"Item '{item_name}' removed successfully."
        return f"Item '{item_name}' not found."

    def calculate_total_sum(self):
        return sum(item["price"] for item in self.items)

    def calculate_per_person_share(self):
        per_person = {eater: 0 for eater in self.eaters}
        for item in self.items:
            split_cost = item["price"] / len(item["eaters"])
            for eater in item["eaters"]:
                per_person[eater] += split_cost
        return per_person

    def display_receipt(self):
        return {
            "receipt_name": self.receipt_name,
            "items": self.items,
            "total_sum": self.calculate_total_sum(),
            "per_person_share": self.calculate_per_person_share(),
        }



# Create a global instance of RestaurantReceipt
receipt_manager = RestaurantReceipt()

# Define Flask routes
@app.route("/")
def home():
    return redirect(url_for("receipt_manager_page"))


@app.route("/receipt_manager")
def receipt_manager_page():
    receipt_data = receipt_manager.display_receipt()
    return render_template("receipt_manager.html", receipt_data=receipt_data)


@app.route("/initialize_receipt", methods=["POST"])
def initialize_receipt():
    name = request.form["name"]
    eaters = request.form["eaters"]
    receipt_manager.set_receipt_name(name)
    receipt_manager.enter_eaters(eaters)
    flash("Receipt initialized successfully!", "success")
    return redirect(url_for("receipt_manager_page"))

@app.route("/remove_item", methods=["POST"])
def remove_item():
    item_name = request.form["item_name"]
    message = receipt_manager.remove_item(item_name)
    if "successfully" in message:
        flash(message, "success")
    else:
        flash(message, "error")
    return redirect(url_for("receipt_manager_page"))

@app.route("/reset_receipt", methods=["POST"])
def reset_receipt():
    global receipt_manager
    receipt_manager = RestaurantReceipt()  # Reset the receipt manager to a new instance
    flash("Receipt has been reset successfully.", "success")
    return redirect(url_for("receipt_manager_page"))



@app.route("/add_item", methods=["POST"])
def add_item():
    item_name = request.form["item_name"]
    try:
        item_price = float(request.form["item_price"])
    except ValueError:
        flash("Invalid price format. Please enter a valid number.", "error")
        return redirect(url_for("receipt_manager_page"))

    eaters_input = request.form["eaters_input"]
    result = receipt_manager.add_item(item_name, item_price, eaters_input)
    if result:
        flash(result, "error")
        return redirect(url_for("receipt_manager_page"))

    flash("Item added successfully!", "success")
    return redirect(url_for("receipt_manager_page"))

@app.route("/export_receipt_txt", methods=["GET"])
def export_receipt_txt():
    # Get the receipt data
    receipt_data = receipt_manager.display_receipt()
    
    # Format the data as a string
    text_output = f"Receipt Name: {receipt_data['receipt_name']}\n\n"
    text_output += "Items:\n"
    for item in receipt_data["items"]:
        text_output += f"- {item['name']}: £{item['price']:.2f} (shared by {', '.join(item['eaters'])})\n"
    
    text_output += f"\nTotal: £{receipt_data['total_sum']:.2f}\n\n"
    text_output += "Cost Breakdown Per Person:\n"
    for person, amount in receipt_data["per_person_share"].items():
        text_output += f"- {person}: £{amount:.2f}\n"
    
    # Create a response with the text data
    response = app.response_class(
        response=text_output,
        mimetype="text/plain",
    )
    response.headers["Content-Disposition"] = "attachment; filename=receipt.txt"
    return response

# Entry point for running the app locally
if __name__ == "__main__":
    app.run(debug=True)