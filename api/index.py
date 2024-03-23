import os
from flask import Flask, request, jsonify
from datetime import datetime
from sqlalchemy import create_engine, text

app = Flask(__name__)

db_url = os.getenv('POSTGRES_URL')
engine = create_engine(db_url)

@app.route('/')
def home():
    return 'hello world!'

@app.route('/test', methods=['POST'])
def test():
    body = request.json
    data = body['data'].split('\n')

    engine.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT,
            timestamp TIMESTAMP
        )
    """)

    for item in data:
        engine.execute(
            text("INSERT INTO items (name, timestamp) VALUES (:name, :timestamp)"),
            {"name": item, "timestamp": datetime.now()}
        )

    return jsonify({"message": "Data received and stored in PostgreSQL"}), 200

if __name__ == '__main__':
    app.run(debug=True)