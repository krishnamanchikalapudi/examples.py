from flask import Flask
from datetime import date
"""
Session: 10
Topic: Web page example

Commands to execute this code
``````
pip3 install Flask
python3 webpage.py
``````
open browser http://127.0.0.1:5000/
"""

app = Flask(__name__)

today = date.today()

@app.route('/')
def hello_world():
    d1 = today.strftime("%B %d, %Y")
    msg = '<H1>Hello, World web page!</H1>'
    return (msg + "<br/> Date: "+ d1)

@app.route('/app1')
def app_fn():
    d1 = today.strftime("%B %d, %Y")
    msg = '<H1>App function!</H1>'
    return (msg + "<br/> Date: "+ d1)


if __name__ == '__main__':
    app.run()