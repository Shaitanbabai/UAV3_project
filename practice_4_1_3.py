from pyinstrument import Profiler
from flask import (Flask, request, g, make_response)
import time
import random

app = Flask(__name__)

def get_sensor_data():
    # here we can add any functionality
    time.sleep(0.05)
    return {
        "altitude": random.randint(0, 500),
        "speed": random.randint(0, 70)
            }

def process(data):
    time.sleep(0.1)
    return {
        "altitude": data["altitude"] /39.37, # convert feet to m
        "speed": data["speed"] * 0.609344 # convert miles to km
    }

def make_decision(data):
    time.sleep(0.2)
    if data["altitude"] <50:  # or set cycle FOR for altitude range
        return "Get higher"
    return "Keep height"

def motor_control(decision):
    time.sleep(0.3)
    return f"Motor tsk: {decision}"

@app.route('/sensor')

@app.route('/')
def index():
    data = get_sensor_data()
    process_data = process(data)
    decision = make_decision(process_data)
    motor = motor_control(decision)

    return f'Drone control\n{motor}'

@app.before_request
def before_request():
    # if "profile" in request.args:
    g.is_profiling = "profile" in request.args
    if g.is_profiling:
        g.profile = Profiler()  # creating object of the class
        g.profile.start()  # start profiling

@app.after_request
def after_request(response):  # stop profiling
    # if hasattr(g, 'profile'):  # check if object exists
    if g.is_profiling:
        g.profile.stop()
        output_html = g.profile.output_html()  # get html report
        return make_response(output_html)  # return html report
    return response


if __name__ == '__main__':
    app.run(debug=True)