from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_password"

is_admin_logged_in = False


TICKET_PRICE = 75

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reservations/', methods=['GET', 'POST'])
def reservations():
    global is_admin_logged_in

    if not is_admin_logged_in:
        return redirect(url_for('admin_login'))

    seating_chart = [['O' for _ in range(4)] for _ in range(12)]
    
    with open('reservations.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(', ')
                if len(parts) == 4:
                    
                    row = int(parts[1]) - 1
                    seat = int(parts[2]) - 1
                    seating_chart[row][seat] = 'X'
                    
                else:
                    print(f"Invalid line format: {line}")
    return render_template('reservations.html', seating_chart=seating_chart)


@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    if request.method == 'POST':
        last_name = request.form['lastName']
        row = request.form['row']
        seat = request.form['seat']
        eTicket = random.randint(1000, 9999)

        with open('reservations.txt', 'a') as file:
            file.write(f'{last_name}, {row}, {seat}, {eTicket}\n')

       
        return redirect(url_for('reservations'))

    
    return redirect(url_for('reservations'))

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    global is_admin_logged_in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

       
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            is_admin_logged_in = True
            return redirect(url_for('reservations'))
        else:
            return render_template('admin_login.html', error="Invalid username or password")

    return render_template('admin_login.html', error=None)


@app.route('/admin/logout/')
def admin_logout():
    global is_admin_logged_in
    is_admin_logged_in = False
    return redirect(url_for('index'))


@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    if request.method == 'POST':
        last_name = request.form['lastName']
        row = request.form['row']
        seat = request.form['seat']
        eTicket = random.randint(1000, 9999)
        
        total_price = TICKET_PRICE

        with open('reservations.txt', 'a') as file:
            file.write(f'{last_name}, {row}, {seat}, {eTicket}, {total_price}\n')

       
        return redirect(url_for('reservations'))

    
    return redirect(url_for('reservations'))

if __name__ == '__main__':
    app.run(debug=True)
