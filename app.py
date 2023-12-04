from flask import Flask, render_template, request, jsonify, redirect, url_for
import webbrowser 
import threading 
import os
import csv
import random

app = Flask(__name__)

# opening up browser
def open_browser():
    print("Opening browser")
    webbrowser.open_new('http://127.0.0.1:5000/')

# redirecting to index.html
@app.route('/')
def index():
    return render_template('index.html')

# # admin page
# @app.route('/admin/', methods=('GET', 'POST'))
# def admin():
#     return render_template('admin.html')


# reservation page
@app.route('/reservations/', methods=['GET', 'POST'])
def reservations():
    # generating seating chart
    seating_chart = [['O' for _ in range(4)] for _ in range(12)]  # Initialize seating chart
    # Read reservations and update seating chart
    with open('reservations.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(', ')
                if len(parts) == 4:
                    # Format: 'Lastname, row, seat, idnum'
                    row = int(parts[1]) - 1  # Convert to zero-index
                    seat = int(parts[2]) - 1
                    seating_chart[row][seat] = 'X'  # Mark as reserved
                    
                else:
                    print(f"Invalid line format: {line}")
    return render_template('reservations.html', seating_chart=seating_chart)

# handling whenever user hits submit on reservations.html
@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    if request.method == 'POST':
        last_name = request.form['lastName']
        row = request.form['row']
        seat = request.form['seat']
        eTicket = random.randint(1000, 9999)  # Random 4-digit number

        with open('reservations.txt', 'a') as file:
            file.write(f'{last_name}, {row}, {seat}, {eTicket}\n')

        # Redirect to a confirmation page or back to the form
        return redirect(url_for('reservations'))

    # If the method is not POST, redirect to the form
    return redirect(url_for('reservations'))


if __name__ == '__main__':
    # found that this helped with browser functionality, mainly without it when running the program itll open 2 windows at once, with this code it only opens 1
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
