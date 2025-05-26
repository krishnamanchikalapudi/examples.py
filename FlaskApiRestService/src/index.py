from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify("message": "Hello World")

@app.route("/<int:itemId>")
async def getItem(itemId):
    return jsonify(itemId, message= "Hello World")