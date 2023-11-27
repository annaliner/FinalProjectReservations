from flask import Flask, render_template, request, jsonify
import webbrowser 
import threading 
import os
import csv

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

# # # reservations page
# @app.route('/reservations/', methods=('GET', 'POST'))
# def admin():
#     return render_template('reservations.html')

if __name__ == '__main__':
    # found that this helped with browser functionality, mainly without it when running the program itll open 2 windows at once, with this code it only opens 1
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
