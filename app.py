from flask import Flask, render_template, request, jsonify, send_file
import re, json
import time
import subprocess
import pexpect

app = Flask(__name__)

allowed_command_list = [
    'ping',
    'icmp',
    'tcpdump',
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

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    return result

def do_simulation(command):
    if 'tcpdump' in command:
        if '-w' in command:
            try:
                # pcap 파일을 응답으로 전송합니다.
                return "send_file"
            except Exception as e:
                return f"파일 다운로드 중 오류가 발생했습니다: {str(e)}"
        else:
            return "-w로 pcap을 캡처하세요"
    else:
        result = execute_command(command)
    return result

@app.route("/simulate", methods=["POST"])
def simulate():
    command = request.form['command']
    print("입력명령어:", command)

    if is_allowed_command(command):
        result = do_simulation(command)
        if result == 'send_file':
            return send_file("pcap/network_info.pcap", as_attachment=True)
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
    app.run(host='0.0.0.0', debug=True)