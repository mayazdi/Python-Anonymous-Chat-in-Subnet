import socket, time, random, select
from threading import Thread

quit_is_called = False
buffer = []

print("Select the mode from the following Choices:\n1)Receiver\n2)Sender")
mode = input()


def run():
    while True: 
        global quit_is_called
        if quit_is_called:
            break


def do_the_thread(addr, sk):
    t0 = Thread(target=run)
    t1 = Thread(target=rcv_msg, args=("Thread-1", 2, sk))
    t2 = Thread(target=snd_msg, args=("Thread-2", addr, sk))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t0.start()
    t1.start()
    t2.start()
    t0.join()


def write_buffer():
    while len(buffer) > 0:
        print (buffer[0])
        buffer.pop(0)


def rcv_msg(name, delay, sk):
    global quit_is_called
    while True:
        d = sk.recv(1024).decode("UTF-8")
        buffer.append(">>" + d)
        time.sleep(delay)
        if d=="quit":
            quit_is_called = True
            break
        

def snd_msg(name, addr, sk):
    global quit_is_called
    while True:
        write_buffer()
        print("<<", end="")
        inp = input()
        if inp == '\n':
            continue
        sk.send(bytes(inp, "UTF-8"))
        if inp == "quit":
            quit_is_called = True
            break


def listen():
    IP = socket.gethostbyname(socket.gethostname())
    port = 8080
    ls = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # rc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ls.bind((IP, port))
    # while True:
    data, addr = ls.recvfrom(1024)
    print(data.decode("UTF-8"), addr)
    prt = random.randrange(start=1025, stop=65535)
    prt = 2304
    ls.sendto(bytes(str(prt), "UTF-8"), addr)
    ls.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr[0], prt))
    print(s.recv(4096).decode("utf-8"))
    #if ok lets chat
    # ls.close()
    # rc.sendto(bytes("Hi", "UTF-8"), addr)
    # print("Sent")
    do_the_thread((addr[0], prt), s)


def broadcast():
    myIP = socket.gethostbyname(socket.gethostname())
    broadcastIP = socket.inet_ntoa(socket.inet_aton(myIP)[:3] + b'\xff' )
    port = 8080
    msg = "Hello"
    bs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bs.sendto(bytes(msg, "UTF-8"), (broadcastIP, port))
    data, addr = bs.recvfrom(1024)
    print(str(int(data)), addr)
    bs.close()

    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.bind(('0.0.0.0', int(data)))
    cs.listen(5)
    conn, addr = cs.accept()
    conn.send(bytes("Lets Chat on port" + str(data), "utf-8"))
    # Ta yek daghighe check konim ke jadid oomad block konim
    do_the_thread(addr, conn)



if mode=="1": #LSTN
    print("Receiving Selected!")
    listen()
elif mode=="2": #BRDC
    print("Sending Selected!")
    broadcast()
else:
    print("The Input is not valid.")
