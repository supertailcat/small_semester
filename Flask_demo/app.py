from flask import Flask, render_template, request, json, jsonify
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
client_list = []


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
        return False


@app.route("/ws", methods=['GET', 'POST'])
def ws():
    user_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    # 每接入一个客户端就会加进列表中
    client_list.append(user_socket)
    print("client " + str(len(client_list)) + "connected!")
    # jf = open("./json_file.json")
    # jsonStr = json.dumps(json.load(jf)) # load json data
    # print(jsonStr)
    # user_socket.send(jsonStr)

    while 1:
        if check_permit(user_socket):
            msg = user_socket.receive()
            if msg == "SEND_JSON":
                jf = open("./json_file.json")
                jsonStr = json.dumps(json.load(jf))  # convert json data to str
                print(jsonStr)
                for client in client_list:  # 服务端给多客户端传消息
                    client.send(jsonStr)
                    
    return "123"
    # else:
    #     pass


if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0', port=80)
    http_serv = WSGIServer(("0.0.0.0", 5678), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
