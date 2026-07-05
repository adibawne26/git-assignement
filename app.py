from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DATABASE_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api')
def api():
    with open('data.json', 'r') as file:
        data = json.load(file)
    from flask import jsonify
    return jsonify(data)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        student = {
            "name": request.form['name'],
            "email": request.form['email']
        }

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template("index.html", error=error_message)

    collection.insert_one(student)

    return redirect('/success')

@app.route('/submittodoitem', methods=['POST'])
def submitTodo():

    item = {
        "itemName": request.form['itemName'],
        "itemDescription": request.form['itemDescription']
    }

    collection.insert_one(item)

    return "Stored Successfully"

@app.route('/success')
def success():
    return render_template("success.html")

if __name__ == '__main__':
    app.run(debug=True)