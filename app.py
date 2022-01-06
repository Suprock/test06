import time
from flask import *
from paramiko import SSHClient, SFTPClient
import _thread
from flask_socketio import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

names =["小张", "小李", "小王", "小乔"]

def print_nums(index:int):
    for i in range(1, 100):
        print("thread{}, number is {}".format(index, i))
        time.sleep(0.1)

def set_nums(name, index):
    for i in range(1, 101):
        socketio.emit("set_num", {"id":"person_{}".format(index), "name":name, "max_num":100, "num":i})
        time.sleep(0.5)    

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return jsonify({"status":200, "result":"OK"})

@socketio.on("connected")
def on_connect(data):
    print("连接成功！")
    for i, name in enumerate(names):
        _thread.start_new_thread(set_nums, (name, i, ))
    
@socketio.on("disconnected")
def on_disconnected():
    print("断开连接成功")