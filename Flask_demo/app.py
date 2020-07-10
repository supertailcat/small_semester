from flask import Flask, render_template, request, json, jsonify
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from geventwebsocket.exceptions import WebSocketError
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# 一个控制台监控一个账号的所有客户端
console_dict = {}  # {"username":[console1, console2] , ... }
client_dict = {}  # {"username": [admin1, admin2],  ...}


def check_permit(user_socket):
    key = ""  # 该线程键值
    index = -1  # 该线程索引

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

        #  1. 接入的是console
        if user == "console":
            # 每接入一个客户端就会加进列表中
            # console_list.append(user_socket)
            try:
                # 提示console输入需要监控的客户端编码
                # response_str = "Server: Please send the client name..."
                # user_socket.send(response_str)

                # 收到编码
                key = user_socket.receive()
                print("@@-> " + key)

                # 字典中创建数组
                if not console_dict.__contains__(key):
                    console_dict[key] = []
                console_dict[key].append(user_socket)

                # 连接成功
                response_str = "Server: console@" + key + " log in!"
                user_socket.send(response_str)
                # user_socket.send("*************************************************************************************")

            except WebSocketError:
                print("error in creating console dict.")

        # 2. 接入的是client
        elif user == "admin":
            #  接受识别码作为字典编码
            try:
                key = user_socket.receive()
                print("@@-> " + key)

                # 客户端线程
                if not client_dict.__contains__(key):
                    client_dict[key] = []

                client_dict[key].append(user_socket)
                # 给客户端返回一个编号index
                # TO DO
                index = len(client_dict[key]) - 1

                print(key + "@threads: " + str(len(client_dict[key])))  # print test

            except WebSocketError:
                print("error in creating client dict.")

        print("connected!")
        # response_str = "Server: " + user + " log in!\n"
        # user_socket.send(response_str)
        return key, index
    else:
        # response_str = "Server: \nsorry, the username or password is wrong, please submit again"
        # user_socket.send(response_str)
        return False


'''
publish()
    sender_type:
        0: server
        1: client
    username: account(group)
    index: the index of the group "username"
    msg: message which to be published

'''


def publish(sender_type, username, index, msg):
    if msg is not None:
        i = 0
        try:
            for client in console_dict[username]:
                i += 1
                try:
                    if sender_type:
                        s = username + "@" + str(index + 1) + "->Server: " + msg
                    else:
                        s = "Server->" + username + "@" + str(index + 1) + ": " + msg

                    client.send(s)
                    print(username + "@console read: " + str(i))
                except WebSocketError as e:
                    print(username + "@console " + str(i) + " disconnected.")
                    continue
        except KeyError:
            print("No key: " + str(username))


@app.route("/ws", methods=['GET', 'POST'])
def ws():
    user_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    # user_socket.send("Please send username and passward: (format: \"username:passward\")")
    # 保存该线程的用户名、对应编号
    username, index = check_permit(user_socket)
    while username:  # 用户名密码成功匹配
        # 进入循环
        while 1:
            # 收信息
            try:
                msg = user_socket.receive()
            except WebSocketError:
                print("error2")
                break

            # # 广播信息给控制台
            publish(1, username, index, msg)

            # 打开文件
            try:
                jf = open("../Forecast/json/" + msg + ".json")
                jsonStr = json.dumps(json.load(jf), sort_keys=False)  # convert json data to str
                print(jsonStr)
                # 发信息
                try:
                    user_socket.send(jsonStr)
                    publish(0, username, index, jsonStr)
                except WebSocketError:
                    print("websocket connect failed")  # 异常处理
                    break

            except FileNotFoundError as e:
                publish(0, username, index, "cannot find the city.")



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
