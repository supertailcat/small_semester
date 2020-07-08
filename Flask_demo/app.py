from flask import Flask, render_template, request, json, jsonify
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from geventwebsocket.exceptions import WebSocketError
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
console_list = []
admin_socket = []


def check_permit(user_socket):
    try:
        msg = user_socket.receive()
        print("@@-> " + msg)
    except WebSocketError:
        print("error1")
        return False

    try:
        user, passwd = msg.split(":")
    except ValueError or AttributeError:
        # response_str = "Server: \nsorry, the username or password is wrong, please submit again"
        # user_socket.send(response_str)
        return False

    # 两个客户端：admin和console，admin可以与服务端交互收发信息，console监控前两者的交互数据
    if (user == "admin" and passwd == "123456") or (user == "console" and passwd == "123456"):

        if user == "console":
            # 每接入一个客户端就会加进列表中
            console_list.append(user_socket)
        elif user == "admin":
            if not admin_socket:
                admin_socket.append(user_socket)
            else:
                admin_socket[0].close()
                admin_socket[0] = user_socket

        print(str(user) + " connected!")
        # response_str = "Server: " + user + " log in!\n"
        # user_socket.send(response_str)
        return True
    else:
        # response_str = "Server: \nsorry, the username or password is wrong, please submit again"
        # user_socket.send(response_str)
        return False


def publish(user, msg):
    if msg is not None:
        i = 0
        for client in console_list:
            i += 1
            try:
                s = user + ": " + msg
                client.send(s)
                print("@console read: " + str(i))
            except WebSocketError as e:
                print("@console " + str(i) + " disconnected.")
                continue


@app.route("/ws", methods=['GET', 'POST'])
def ws():
    user_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    # user_socket.send("Please send username and passward: (format: \"username:passward\")")

    while check_permit(user_socket):  # 用户名密码成功匹配
        # 进入循环
        while 1:
            # 收信息
            try:
                msg = user_socket.receive()
            except WebSocketError:
                print("error2")
                break

            # 广播信息给控制台
            publish("Admin", msg)

            # 打开文件
            try:
                jf = open("../Forecast/json/" + msg + ".json")
                jsonStr = json.dumps(json.load(jf))  # convert json data to str
                print(jsonStr)
            except FileNotFoundError as e:
                publish("Server", "cannot find the city.")

            # 发信息
            try:
                user_socket.send(jsonStr)
                if user_socket == admin_socket[0]:  # 发送给控制台监控
                    publish("Server", jsonStr)
            except WebSocketError:
                print("websocket connect failed")  # 异常处理
                break

@app.route("/console")
def console_run():
    return render_template("console.html")
@app.route("/client")
def client_run():
    return render_template("client.html")

if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0', port=80)
    http_serv = WSGIServer(("0.0.0.0", 5678), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
