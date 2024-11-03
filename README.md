# Receipt Itemizer App - README

## Overview
Welcome to my first project! This is a simple web app that helps you split restaurant bills among friends, making it easy to keep track of who owes what. You can name your receipt, add people, add items they’ve ordered, and see the final breakdown of costs per person. The app is built using Flask, and it’s accessible remotely via ngrok, so you can share the link with friends if you’re running it locally.

## Features
- **Create a Receipt**: Give the receipt a name and add the people who’ll be splitting the bill.
- **Add Items**: Enter each item’s name, price, and who’s sharing it. You can even type “ALL” to split it across everyone.
- **Calculate Totals**: The app shows each person’s share based on what they ordered and the total bill amount.
- **Easy Access**: Hosted through ngrok, so you can share the link with anyone to view and manage the receipt.

## How to Set It Up
### Requirements
- Python 3.x
- Google Colab or a local setup with Flask and ngrok

### Getting Started
1. Download ngrok:
    ```python
    !wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip -O ngrok.zip
    !unzip -o ngrok.zip
    !chmod +x ./ngrok
    ```
2. Install Flask:
    ```python
    !pip install flask
    ```
3. Replace the ngrok auth token with your own in the code.

### Running the App
After setup, run `app.py` in your environment. Ngrok will provide a public link to your app, which you’ll see printed in the console. Use this link to access the app from any browser.

## Using the App
1. **Go to the ngrok URL**: This will take you to the main receipt manager page.
2. **Initialize the Receipt**:
   - Enter a name for the receipt (e.g., "Pizza Night").
   - Add the names of everyone splitting the bill, separated by commas.
3. **Add Items**:
   - Input each item’s name and price.
   - Choose who’s sharing it (enter specific names or type “ALL” for everyone).
4. **See the Breakdown**:
   - The app calculates each person’s share, showing the total bill and how much each person owes.

### Example
1. **Initialize Receipt**:
   - Receipt Name: "Friends Dinner"
   - Eaters: "Alice, Bob, Carol"
2. **Add Items**:
   - Item: "Pizza", Price: £15, Eaters: "Alice, Bob"
   - Item: "Salad", Price: £10, Eaters: "ALL"
3. **Final Summary**:
   - Total: £25
   - Each person’s share based on what they ordered.

## Code Highlights
- **Class `RestaurantReceipt`**: This does all the heavy lifting, keeping track of items, eaters, and calculating the totals per person.
- **Flask Routes**:
  - **Home (`/`)**: Redirects to the main receipt manager page.
  - **Receipt Manager (`/receipt_manager`)**: Displays the receipt summary.
  - **Initialize Receipt (`/initialize_receipt`)**: Initializes the receipt with a name and eaters.
  - **Add Item (`/add_item`)**: Adds items to the receipt and updates the summary.

## Improvements in the Future
- Add options for tax and tips.
- Downloadable receipts as PDFs.
- More error handling for smoother use.

## Thanks!
Big thanks to ngrok for making remote access easy and to Flask for simplifying the web development side of things. Enjoy the app and happy bill-splitting!
