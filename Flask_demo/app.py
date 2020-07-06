from flask import Flask, render_template, request, json, jsonify
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer

app=Flask(__name__)

def check_permit(user_socket):
    msg = user_socket.receive()
    user, passwd = msg.split(":")
    if user == "admin" and passwd == "123456":
        response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
        user_socket.send(response_str)
        return True
    else:
        response_str = "sorry, the username or password is wrong, please submit again"
        user_socket.send(response_str)


@app.route("/ws", methods=['GET', 'POST'])
def ws():
    user_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    print("client connected!")
    if check_permit(user_socket):
        while 1:
            msg = user_socket.receive()
           # if msg == "SEND_JSON":
               # jf = open("./json_file.json")
               # jsonStr = jsonify(json.load(jf)) # load json data
               # user_socket.send(json.load(jf))
            user_socket.send("server received: " + msg)
    return "123"
    # else:
    #     pass

if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0', port=80)
    http_serv = WSGIServer(("0.0.0.0", 5678), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()





