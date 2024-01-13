from flask import Flask, render_template, request, jsonify
import re, json
import time
import subprocess

app = Flask(__name__)

allowed_command_list = [
    'ping',
    'arping',
    'icmp',
    'tcpdump',
    'arp',
    'ifconfig',
]

def is_allowed_command(command):
    for pattern in allowed_command_list:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

@app.route("/")
def index():
    return render_template("index.html")


def get_ifconfig_result():
    return """
        eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500                                                                                                                                                                                  
        inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255                                                                                                                                                                         
        inet6 fe80::25d9:74be:891e:4456  prefixlen 64  scopeid 0x20<link>                                                                                                                                                                   
        ether 08:00:27:53:0c:ba  txqueuelen 1000  (Ethernet)                                                                                                                                                                                
        RX packets 2256  bytes 291304 (284.4 KiB)                                                                                                                                                                                           
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2449  bytes 221528 (216.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.56.101  netmask 255.255.255.0  broadcast 192.168.56.255
        inet6 fe80::c56e:af66:12c4:e206  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:cb:df:1e  txqueuelen 1000  (Ethernet)
        RX packets 20037  bytes 2209990 (2.1 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19481  bytes 3752628 (3.5 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 41335  bytes 4883033 (4.6 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 41335  bytes 4883033 (4.6 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
    """

def get_arp_result():
    return "arp를 구현하겠습니다."

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    return result

def do_simulation(command):

    if "ifconfig" in command:
        result = get_ifconfig_result()
    elif 'arp' in command:
        result = execute_command('arp -a')

    return result

@app.route("/simulate", methods=["POST"])
def simulate():
    command = request.form['command']
    print("입력명령어:", command)

    if is_allowed_command(command):
        result = do_simulation(command)
    else:
        result = "허용되지 않는 명령어 입니다."
    return render_template('index.html', command=command, result=result)

correct_answer = 'FLAG{이이잉 나 이이니♥}'
@app.route('/answer', methods=['POST'])
def check_answer():
    user_input = request.form.get('macAddress', '')
    if user_input == correct_answer:
        return jsonify({'result':'정답입니다. 범인은 이인희 이고 그가 날린 메시지는 FLAG{이이잉 나 이이니♥} 입니다.'})
    else:
        return jsonify({'result':'오답입니다.'})

if __name__=="__main__":
    app.run(debug=True)