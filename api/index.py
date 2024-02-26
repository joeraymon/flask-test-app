from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'hello world!'

@app.route('/test')
def test():
    print(request.json())

    return jsonify({"message": "Data received"}), 200

if __name__ == '__main__':
    app.run(debug=True)