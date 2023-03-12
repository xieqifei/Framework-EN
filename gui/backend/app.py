
import sys
import os

# add the project path to sys.path, so that model file can be found in .common/solve.py 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir =os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from flask import Flask, Response, request
from flask_cors import CORS
import json
from common import MessageAnnouncer
from common import Optimization

DEBUG = True
 
app = Flask(__name__,static_folder='../fronted/dist')
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
announcer = MessageAnnouncer()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/solve', methods=['POST'])
def solve_model():
    data = request.json
    optimization = Optimization(announcer)
    optimization.handle_solution(data)
    return {}, 200


@app.route('/test', methods=['POST'])
def test_model():
    data = request.json
    
    return {}, 200

@app.route('/stream')
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg
    return Response(stream(), mimetype='text/event-stream')

@app.route('/<path:fallback>')
def fallback(fallback):       # Vue Router 的 mode 为 'hash' 时可移除该方法
    if fallback.startswith('css/') or fallback.startswith('js/')\
            or fallback.startswith('img/') or fallback == 'favicon.ico'\
            or fallback.startswith('assets/'):
        return app.send_static_file(fallback)
    else:
        return app.send_static_file('index.html')
 
 
if __name__ == '__main__':
    app.run()