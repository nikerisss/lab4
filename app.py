from flask import Flask
from gevent.pywsgi import WSGIServer
app = Flask(__name__)


@app.route('/api/v1/hello-world{14}')
def hello_world():  # put application's code here
    return 'Hello World14'


if __name__ == '__main__':
    app.run()

server = WSGIServer(('127.0.0.1', 5000), app)
server.serve_forever()