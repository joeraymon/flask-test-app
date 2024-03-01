import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NOTION_SECRET = os.getenv('NOTION_SECRET')
DATABASE_ID = "a003f6b477814191b2e53c428cb4c3e5"

url = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {NOTION_SECRET}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",  # Use the latest supported API version
}

@app.route('/')
def home():
    return 'hello world!'

@app.route('/test', methods=['POST'])
def test():
    body = request.json
    print(body)

    data = body['data'].split('\n')
    print(data)

    payload = {
        "parent": { "database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{
                    "text": {
                        "content": "test data"
                    }
                }]
            },
            "Date": {
                "date": {
                    "start": "2024-02-27"
                }
            },
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.text)

    return jsonify({"message": "Data received"}), 200

if __name__ == '__main__':
    app.run(debug=True)