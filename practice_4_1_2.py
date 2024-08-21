import math

from pyinstrument import Profiler
from flask import (Flask, request, g, make_response)

app = Flask(__name__)


@app.route('/')
def index():
    if g.is_profiling:
        g.profile.start()
    # here we can add any functionality
    result = 0
    for i in range (1, 1000000):
        result += math.sqrt(i)
    if g.is_profiling:
        g.profile.stop()
        # output_html = g.profile.output_html()  # get html report
        # return make_response(output_html)  # return html report
    return 'Drone control'



@app.before_request
def before_request():
    # if "profile" in request.args:
    g.is_profiling = "profile" in request.args
    if g.is_profiling:
        g.profile = Profiler()  # creating object of the class
        # g.profile.start()  # start profiling

@app.after_request
def after_request(response):  # stop profiling
    # if hasattr(g, 'profile'):  # check if object exists
    if g.is_profiling:
        # g.profile.stop()
        output_html = g.profile.output_html()  # get html report
        return make_response(output_html)  # return html report
    return response


if __name__ == '__main__':
    app.run(debug=True)