from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient("mongodb+srv://immortal:immortalduck@gooner.fnw1yio.mongodb.net/?appName=gooner")
db = client["mydatabase"]
collection = db["mycollection"]

@app.route('/')
def form():
    return render_template('entry.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']

        # Insert into MongoDB Atlas
        collection.insert_one({"name": name, "email": email})

        # Redirect to success page
        return redirect(url_for('success'))

    except Exception as e:
        # Show error on same page
        return render_template('entry.html', error=str(e))

@app.route('/success')
def success():
    return render_template('out.html')

@app.route('/api')
def api():
    try:
        with open('api_data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)