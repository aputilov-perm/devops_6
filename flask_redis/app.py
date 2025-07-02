import redis
from flask import Flask, make_response
import socket

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    return int(cache.get('hits') or 0)

def incr_hit_count():
    return cache.incr('hits')

@app.route('/')
def hello():
    incr_hit_count()
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times. My name is: {socket.gethostname()}\n'

@app.route('/metrics')
def metrics():
    count = get_hit_count()
    response = make_response(f'''# HELP view_count Flask visit counter
# TYPE view_count counter
view_count{{service="Flask-Redis-App"}} {count}
''', 200)
    response.mimetype = "text/plain"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
