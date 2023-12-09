from flask import Flask, render_template, request, jsonify, redirect, url_for
import webbrowser 
import threading 
import os
import csv
import random

app = Flask(__name__)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_password"
TICKET_PRICE = 75

is_admin_logged_in = False

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for _ in range(12)]
    return cost_matrix


# opening up browser
def open_browser():
    print("Opening browser")
    webbrowser.open_new('http://127.0.0.1:5000/')

# redirecting to index.html
@app.route('/')
def index():
    return render_template('index.html')

# reservation page
@app.route('/reservations/', methods=['GET', 'POST'])
def reservations():

    global is_admin_logged_in

    if not is_admin_logged_in:
        return redirect(url_for('admin_login'))
    
    # if is_admin_logged_in:
    #     return redirect(url_for('reservations'))
    total_sales = 0 
    cost_matrix = get_cost_matrix()

    try:
        with open('reservations.txt', 'r') as file: 
            for line in file: 
                parts = line.strip().split(', ')
                if len(parts) >= 4:
                    row = int(parts[1]) - 1
                    seats = int(parts[2]) - 1
                    total_sales += cost_matrix[row][seat]
    except Exception as e:
        print(f"Error reading file: {e}")
    # generating seating chart
    seating_chart = [['O' for _ in range(4)] for _ in range(12)]  # Initialize seating chart

    # Read reservations and update seating chart
    with open('reservations.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(', ')
                if len(parts) >= 4:
                    # Format: 'Lastname, row, seat, idnum'
                    row = int(parts[1]) - 1  # Convert to zero-index
                    seat = int(parts[2]) - 1
                    seating_chart[row][seat] = 'X'  # Mark as reserved
                    total_sales += cost_matrix[row][seat]
                    
                else:
                    print(f"Invalid line format: {line}")
    return render_template('reservations.html', seating_chart=seating_chart, is_admin_logged_in=is_admin_logged_in, total_sales=total_sales)

# handling whenever user hits submit on reservations.html
@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    if request.method == 'POST':
        last_name = request.form['lastName']
        row = request.form['row']
        seat = request.form['seat']
        eTicket = random.randint(1000, 9999)  # Random 4-digit number

        total_price = TICKET_PRICE

        with open('reservations.txt', 'a') as file:
            file.write(f'{last_name}, {row}, {seat}, {eTicket}, {total_price}\n')

        # Redirect to a confirmation page or back to the form
        return redirect(url_for('reservations'))

    # If the method is not POST, redirect to the form
    return redirect(url_for('reservations'))

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    global is_admin_logged_in
    # Read admin credentials from file


    credentials = {}
    try: 
        with open('final_project_files/passcodes.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(', ')
                credentials[username.strip()] = password.strip()
                print(f"Loaded credential: Username={username.strip()}, Password={password.strip()}")  # Debugging print

    except Exception as e:
        print(f"Error reading file: {e}")
        return render_template('admin_login.html', error="Error reading credentials file.")

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        print(f"Username: {username}, Password: {password}")

        if credentials.get(username) == password:
            is_admin_logged_in = True
            return redirect(url_for('reservations'))
        else:
            return render_template('admin_login.html', error="Invalid username or password")

        # Check credentials
        # if credentials.get(username) == password:
        #     is_admin_logged_in = True
        #     return redirect(url_for('reservations'))
        # else:
        #     return render_template('admin_login.html', error="Invalid username or password")

    return render_template('admin_login.html', error=None)


@app.route('/admin/logout/')
def admin_logout():
    global is_admin_logged_in
    is_admin_logged_in = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    # found that this helped with browser functionality, mainly without it when running the program itll open 2 windows at once, with this code it only opens 1
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
