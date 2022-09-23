from threading import Thread
import random 
import socket

# address family,socketType
#ipv4(AF_INET) and ipv6(AF_INET6)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 5500

# tuple
server.bind((ip_address, port))
server.listen()

list_of_clients = []
nick_names=[]
print("server is running.......")

question=[
    "what is the italian word for pie? \n a.mozarella\n b.pasty\n c.patty\n d.pizza",
    "water boils at 212 units at which scale? \n a.F\n b.C\n c.K\n d.R",
    "which sea creature has 3 hearts? \n a.dolphin\n b.octopus\n c.walrus\n d.seal",
]

answers=["d","a","b"]


def remove_question(index):
    question.pop(index)
    answers.pop(index)

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

def remove_nicknames(nickname):
    if nickname in nick_names:
        nick_names.remove(nickname)

def get_random(conn):
    random_index=random.randint(0,len(question)-1)
    random_question=question[random_index]
    random_answer=answers[random_index]
    conn.send(random_question.encode('utf-8'))
    print(random_question)
    return random_index,random_question,random_answer

def clientThread(conn,nickname):
    score=0
    conn.send("Welcome to the quizgame".encode("utf-8"))
    conn.send("you will recieve a question.The answer to that question should be one of a,b,c,d\n".encode("utf-8"))
    conn.send("good luck!\n\n".encode("utf-8"))
    index,question,answer=get_random(conn)
    print(answer)

    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower()==answer:
                    score+=1
                    conn.send(f"bravo your score is {score}\n\n".encode("utf-8"))
                else:
                    conn.send("incorrect answer\n\n".encode("utf-8"))
                remove_question(index)
                index,question,answer=get_random(conn)
                print(answer)

            else:
                remove(conn)
                remove_nicknames(nickname)
        except:
            continue

# accept function
while True:
    conn, address = server.accept()
    conn.send("NICKNAME".encode('utf-8'))
    nickname=conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nick_names.append(nickname)
    print(nickname+' connected')

    newThread = Thread(target=clientThread, args=(conn, nickname))
    newThread.start()
