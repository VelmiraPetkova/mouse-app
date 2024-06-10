from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import sqlite3
import time
import os

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')


# Initialize the database
def init_db():
    conn = sqlite3.connect('mouse_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mouse_data (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp TEXT, 
                 x INTEGER, 
                 y INTEGER, 
                 image_path TEXT)''')
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('mouse_event')
def handle_mouse_event(data):
    x = data['x']
    y = data['y']
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    image_path = ''

    if data['button_pressed']:
        image_path = capture_image()

    save_to_db(timestamp, x, y, image_path)
    emit('response', {'status': 'OK'})


def save_to_db(timestamp, x, y, image_path):
    conn = sqlite3.connect('mouse_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO mouse_data (timestamp, x, y, image_path) VALUES (?, ?, ?, ?)',
              (timestamp, x, y, image_path))
    conn.commit()
    conn.close()


def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    image_path = ''
    if ret:
        image_path = f'static/images/{time.time()}.jpg'
        cv2.imwrite(image_path, frame)
    cap.release()
    return image_path


if __name__ == '__main__':
    # Create the static/images directory if it doesn't exist
    if not os.path.exists('static/images'):
        os.makedirs('static/images')

    socketio.run(app, allow_unsafe_werkzeug=True)
