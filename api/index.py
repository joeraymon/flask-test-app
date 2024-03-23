import os
from flask import Flask, request, jsonify
from datetime import datetime
import pg8000
import ssl

app = Flask(__name__)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False  # Disable hostname checking if needed
ssl_context.verify_mode = ssl.CERT_NONE  # Adjust verification mode as needed


def open_connection():
    return pg8000.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        ssl_context=ssl_context
    )

@app.route('/')
def home():
    return 'hello world!'

@app.route('/test', methods=['POST'])
def test():
    body = request.json
    data = body['data'].split('\n')

    conn = open_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT,
            timestamp TIMESTAMP
        )
    """)

    for item in data:
        cur.execute(
            "INSERT INTO items (name, timestamp) VALUES (%s, %s)",
            (item, datetime.now())
        )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Data received and stored in PostgreSQL"}), 200

if __name__ == '__main__':
    app.run(debug=True)