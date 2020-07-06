from flask import Flask, render_template, request
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer

app=Flask(__name__)

@app.route("/ws")
def ws():
    user_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    while 1:
        msg = user_socket.receive()
        print(msg)
    return "123"

if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0', port=80)
    http_serv = WSGIServer(("0.0.0.0", 9999), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()





