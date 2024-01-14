import socket
import time
import random

server = 'irc.freenode.net'
channel = '#channel'
nick_criminal1 = 'In-Hee Lee'
top30_list = ["Soo-Min Lee", "Chang-Wook Song", "Young-Won Seo", "Gyo-Hyun Lee", "Je-Hyun Hwang", "Joo-Won Cho", "Yong-Hoon Shin"]
nick_criminal2 = random.choice(top30_list)

while True:
    # 소켓 생성
    irc_criminal1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_criminal2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 같은 서버에 연결한다.
    irc_criminal1.connect((server, 6667))
    irc_criminal2.connect((server, 6667))

    # 유저정보를 전송한다
    irc_criminal1.send(bytes('NICK ' + nick_criminal1 + '\r\n', 'UTF-8'))
    irc_criminal1.send(bytes('USER ' + nick_criminal1 + ' 0 * :' + nick_criminal1 + '\r\n', 'UTF-8'))

    irc_criminal2.send(bytes('NICK ' + nick_criminal2 + '\r\n', 'UTF-8'))
    irc_criminal2.send(bytes('USER ' + nick_criminal2 + ' 0 * :' + nick_criminal2 + '\r\n', 'UTF-8'))

    time.sleep(3) # 약간의 딜레이 추가

    # 채널에 조인한다
    irc_criminal1.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))
    irc_criminal2.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

    response_criminal1 = irc_criminal1.recv(2048).decode('UTF-8')
    print(f"Criminal1 response: {response_criminal1}")

    response_criminal2 = irc_criminal2.recv(2048).decode('UTF-8')
    print(f"Criminal2 response: {response_criminal2}")

    irc_criminal1.send(bytes('PRIVMSG ' + channel + ' :' + 'HI! ^^  RkxBR3vsnbTsnbTsnokg64KYIOydtOydtOuLiOKZpX0K' + '\r\n', 'UTF-8'))
    print("Criminal1 sent: hi")

    time.sleep(1) #  약간의 딜레이 추가

    irc_criminal2.send(bytes('PRIVMSG ' + channel + ' :' + 'Go Away Fuck!' + '\r\n', 'UTF-8'))
    print("Criminal2 sent: bye")
