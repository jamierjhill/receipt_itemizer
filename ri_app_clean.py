{"cells":[{"cell_type":"code","source":["from flask import Flask, request, redirect, url_for, render_template, jsonify\n","import os\n","\n","app = Flask(__name__, template_folder='templates')  # Use relative path for templates\n","\n","class RestaurantReceipt:\n","    def __init__(self):\n","        self.items = []\n","        self.eaters = set()\n","        self.receipt_name = \"\"\n","\n","    def set_receipt_name(self, name):\n","        self.receipt_name = name\n","\n","    def enter_eaters(self, eaters):\n","        self.eaters = {eater.strip().title() for eater in eaters.split(\",\")}\n","\n","    def add_item(self, item_name, item_price, eaters_input):\n","        if eaters_input.strip().upper() == \"ALL\":\n","            eaters_list = list(self.eaters)\n","        else:\n","            eaters_list = [eater.strip().title() for eater in eaters_input.split(\",\") if eater.strip().title() in self.eaters]\n","\n","        if not eaters_list:\n","            return \"No valid eaters provided. Maybe you should invite them next time. No item added.\"\n","\n","        self.items.append({\n","            'name': item_name,\n","            'price': item_price,\n","            'eaters': eaters_list\n","        })\n","\n","    def calculate_total_sum(self):\n","        return sum(item['price'] for item in self.items)\n","\n","    def calculate_per_person_share(self):\n","        per_person = {eater: 0 for eater in self.eaters}\n","        for item in self.items:\n","            split_cost = item['price'] / len(item['eaters'])\n","            for eater in item['eaters']:\n","                per_person[eater] += split_cost\n","        return per_person\n","\n","    def display_receipt(self):\n","        return {\n","            \"receipt_name\": self.receipt_name,\n","            \"items\": self.items,\n","            \"total_sum\": self.calculate_total_sum(),\n","            \"per_person_share\": self.calculate_per_person_share()\n","        }\n","\n","receipt_manager = RestaurantReceipt()\n","\n","# Redirect root route to receipt manager page\n","@app.route('/')\n","def home():\n","    return redirect(url_for('receipt_manager_page'))\n","\n","@app.route('/receipt_manager')\n","def receipt_manager_page():\n","    receipt_data = receipt_manager.display_receipt()\n","    return render_template('receipt_manager.html', receipt_data=receipt_data)\n","\n","@app.route('/initialize_receipt', methods=['POST'])\n","def initialize_receipt():\n","    name = request.form['name']\n","    eaters = request.form['eaters']\n","    receipt_manager.set_receipt_name(name)\n","    receipt_manager.enter_eaters(eaters)\n","    return redirect(url_for('receipt_manager_page'))\n","\n","@app.route('/add_item', methods=['POST'])\n","def add_item():\n","    item_name = request.form['item_name']\n","    try:\n","        item_price = float(request.form['item_price'])\n","    except ValueError:\n","        return jsonify({\"error\": \"Invalid price format.\"}), 400\n","    eaters_input = request.form['eaters_input']\n","    result = receipt_manager.add_item(item_name, item_price, eaters_input)\n","    if result:\n","        return jsonify({\"error\": result}), 400\n","    return redirect(url_for('receipt_manager_page'))\n","\n","\n","if __name__ == \"__main__\":\n","    app.run(host=\"0.0.0.0\", port=5000)\n","\n","# No need for app.run(); PythonAnywhere uses WSGI configuration\n"],"metadata":{"id":"k6r1TxBQ3zLg","executionInfo":{"status":"ok","timestamp":1730544663071,"user_tz":0,"elapsed":165132,"user":{"displayName":"Jamie Hill","userId":"10831983047187267053"}},"colab":{"base_uri":"https://localhost:8080/"},"outputId":"186d7415-97e1-4020-8910-6e8786dadd58"},"execution_count":null,"outputs":[{"output_type":"stream","name":"stdout","text":["Collecting Flask-WTF\n","  Downloading flask_wtf-1.2.2-py3-none-any.whl.metadata (3.4 kB)\n","Requirement already satisfied: flask in /usr/local/lib/python3.10/dist-packages (from Flask-WTF) (2.2.5)\n","Requirement already satisfied: itsdangerous in /usr/local/lib/python3.10/dist-packages (from Flask-WTF) (2.2.0)\n","Collecting wtforms (from Flask-WTF)\n","  Downloading wtforms-3.2.1-py3-none-any.whl.metadata (5.3 kB)\n","Requirement already satisfied: Werkzeug>=2.2.2 in /usr/local/lib/python3.10/dist-packages (from flask->Flask-WTF) (3.0.6)\n","Requirement already satisfied: Jinja2>=3.0 in /usr/local/lib/python3.10/dist-packages (from flask->Flask-WTF) (3.1.4)\n","Requirement already satisfied: click>=8.0 in /usr/local/lib/python3.10/dist-packages (from flask->Flask-WTF) (8.1.7)\n","Requirement already satisfied: markupsafe in /usr/local/lib/python3.10/dist-packages (from wtforms->Flask-WTF) (3.0.2)\n","Downloading flask_wtf-1.2.2-py3-none-any.whl (12 kB)\n","Downloading wtforms-3.2.1-py3-none-any.whl (152 kB)\n","\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m152.5/152.5 kB\u001b[0m \u001b[31m2.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n","\u001b[?25hInstalling collected packages: wtforms, Flask-WTF\n","Successfully installed Flask-WTF-1.2.2 wtforms-3.2.1\n"," * Serving Flask app '__main__'\n"," * Debug mode: off\n"]},{"output_type":"stream","name":"stderr","text":["INFO:werkzeug:\u001b[31m\u001b[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\u001b[0m\n"," * Running on all addresses (0.0.0.0)\n"," * Running on http://127.0.0.1:5000\n"," * Running on http://172.28.0.12:5000\n","INFO:werkzeug:\u001b[33mPress CTRL+C to quit\u001b[0m\n"]}]}],"metadata":{"colab":{"provenance":[{"file_id":"1viNmg-Df1jQbSoUT15OI5K_fFTMbQLOh","timestamp":1730544434471}],"mount_file_id":"1tV0PbuyXFAeoAM6IElf2XBqwhKRZFXWy","authorship_tag":"ABX9TyN2dlXkS9AWkLNEN2/8SZiq"},"kernelspec":{"display_name":"Python 3","name":"python3"},"language_info":{"name":"python"}},"nbformat":4,"nbformat_minor":0}