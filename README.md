# CTF_Platform

## 1. Development

### 1) 환경 구축
![Frame 1 (1)](https://github.com/S-SIRIUS/CTF_Platform/assets/109223193/c0749320-d396-4868-b25b-15c06f255e9a)



### 2) IRC(Internet Relay Chat)
#### 가. Irc_Chat
```
irc_criminal1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc_criminal2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc_criminal1.connect((server, 6667))
irc_criminal2.connect((server, 6667))
```
소켓 생성 및 서버 연결: 코드는 두 개의 소켓(irc_criminal1, irc_criminal2)을 생성하고, 주어진 IRC 서버(irc.freenode.net)에 연결한다. 두 개의 독립된 사용자를 서버에 연결한다.

```
irc_criminal1.send(bytes('NICK ' + nick_criminal1 + '\r\n', 'UTF-8'))
irc_criminal1.send(bytes('USER ' + nick_criminal1 + ' 0 * :' + nick_criminal1 + '\r\n', 'UTF-8'))
irc_criminal2.send(bytes('NICK ' + nick_criminal2 + '\r\n', 'UTF-8'))
irc_criminal2.send(bytes('USER ' + nick_criminal2 + ' 0 * :' + nick_criminal2 + '\r\n', 'UTF-8'))
```
사용자 정보 전송: 각 소켓을 통해 서버에 사용자 정보를 전송한다. 이 정보에는 닉네임(NICK)과 사용자 설명(USER)이 포함된다. 이 단계에서 각 사용자는 서버에 자신의 신원을 등록한다.

```
irc_criminal1.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))
irc_criminal2.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))
response_criminal1 = irc_criminal1.recv(2048).decode('UTF-8')
irc_criminal1.send(bytes('PRIVMSG ' + channel + ' :' + 'HI! ^^  RkxBR3vsnbTsnbTsnokg64KYIOydtOydtOuLiOKZpX0K' + '\r\n', 'UTF-8'))
```
각 사용자는 특정 채널(#channel)에 접속하고, 채널에서 초기응답 메시지를 수신하고 메시지를 송신한다.

```
nick_criminal2 = random.choice(top30_list)
```
랜덤 닉네임 선택: 코드는 top30_list에서 랜덤하게 하나의 닉네임을 선택하여 두 번째 사용자의 닉네임으로 사용한다. 이것은 두 번째 사용자의 신원을 동적으로 변화시키는 데 사용한다.
정상 채팅에서는 두 사용자 모두를 랜덤으로 선택한다.

### 2) Back_end Code
#### 가. 허용된 명령어
```
allowed_command_list = [
    'ping',
    'icmp',
    'tcpdump',
    'ifconfig',
]
```
tcpdump에 쓸 인터페이스 카드 확인 용도 명령어만 허용한다.

#### 나. 핵심 로직
```
def do_simulation(command):
    if 'tcpdump' in command:
        if '-w' in command:
            try:
                return "send_file"
            except Exception as e:
                return f"파일 다운로드 중 오류가 발생했습니다: {str(e)}"
        else:
            return "-w로 pcap을 캡처하세요"
    else:
        result = execute_command(command)
    return result

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

```
원래 tcpdump를 통해 동적으로 패킷의 오고감을 프론트에까지 전달해보고 싶었지만 시간관계상 하지 못했다. 
그래서 결국 따라서 tcpdump에서 -w 옵션을 사용자에게 힌트로 주어서 pcap파일을 다운로드 받게끔 수정하였다.

## 2. Simple Write Up
### 1) 인터페이스 카드 확인
> ifconfig
![스크린샷 2024-01-14 173128](https://github.com/S-SIRIUS/CTF_Platform/assets/109223193/1961472f-15fb-4d33-89d0-02879fb34b74)

### 2) 패킷 다운로드

> tcpdump -i ens33 -w network_info.pcap

와이어 샤크에서 분석 가능!

### 3) IRC 패킷만 추출


### 3) IRC 패킷에서 메시지 담긴 패킷만 추출

### 4) 범인 추적

### 5) Base 64 디코딩

### 6) 범인, FLAG 입력
