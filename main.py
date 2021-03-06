import socket, time, random, multiprocessing, ipaddress
from threading import Thread

quit_is_called = False
rcvd = False
buffer = []


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
        print(buffer[0])
        buffer.pop(0)


def rcv_msg(name, delay, sk):
    global quit_is_called
    while True:
        d = sk.recv(1024).decode("UTF-8")
        buffer.append(">>" + d)
        print('\a', end="")  # Alarm
        time.sleep(delay)
        if d == "quit":
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
        ln = len(inp)
        if ln < 1024:
            sk.send(bytes(inp, "UTF-8"))
            if inp == "quit":
                quit_is_called = True
                break
        else:
            print("<<Message lenght is not valid.>>")


def recv_bad_port(s, ls):
    data, _ = ls.recvfrom(1024)
    if data == "Bad Port":
        raise Exception("Bad Port")


def listen():
    IP = socket.gethostbyname(socket.gethostname())
    port = 8080
    ls = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # rc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ls.bind((IP, port))
    # while True:
    data, addr = ls.recvfrom(1024)
    print(data.decode("UTF-8"), addr)
    while True:
        try:
            prt = random.randrange(start=1025, stop=65535)
            # prt = 2304
            ls.sendto(bytes(str(prt), "UTF-8"), addr)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            t4 = Thread(target=recv_bad_port, args=(
                "Thread-4", ls), daemon=True)
            t4.start()
            s.connect((addr[0], prt))
            print(s.recv(4096).decode("utf-8"))
        except:
            print("Couldnt establish connection")
        finally:
            # ls.close()
            break
    # if ok lets chat
    # ls.close()
    # rc.sendto(bytes("Hi", "UTF-8"), addr)
    # print("Sent")
    do_the_thread((addr[0], prt), s)


def brdcst(bs, msg, broadcastIP, port):
    while not rcvd:
        bs.sendto(bytes(msg, "UTF-8"), (broadcastIP, port))
        time.sleep(3)
        # print("Boadcast!")


def recv_or_brdcast(bs, msg, broadcastIP, port):
    global rcvd
    th = Thread(target=brdcst, args=(bs, msg, broadcastIP, port))
    th.setDaemon(True)
    th.start()
    a, b = bs.recvfrom(1024)
    rcvd = True
    # t1 = Thread(target=rcv_msg, args=("Thread-1", 2, sk))
    return a, b


def recv_and_block(s, bs):
    while True:
        _, a = bs.recvfrom(1024)
        bs.sendto(bytes("Destination already taken", "UTF-8"), a)


def broadcast(BIP):
    broadcastIP = BIP
    port = 8080
    msg = "Hello"
    bs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bs.sendto(bytes(msg, "UTF-8"), (broadcastIP, port))
    data, addr = recv_or_brdcast(bs, msg, broadcastIP, port)
    print(str(int(data)), addr)
    # bs.close()
    while True:
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cs.bind(('0.0.0.0', int(data)))
            cs.listen(5)
            conn, addr = cs.accept()
            conn.send(bytes("Lets Chat on port" + str(data), "utf-8"))
        except:
            bs.sendto(bytes("Bad Port", "UTF-8"), addr)
        finally:
            break
    t3 = Thread(target=recv_and_block, args=("Thread-3", bs), daemon=True)
    t3.start()
    do_the_thread(addr, conn)


myIP = socket.gethostbyname(socket.gethostname())
print("Your Subnet mask is set to /24 by default. if you want to change enter the mask value:\nelse press Enter.")
mask = input()
BIP = None
try:
    BIP = str(ipaddress.ip_network('192.168.1.0/'+mask).broadcast_address)
except Exception as e:
    print(e)
    print("mask is not changed!")
    BIP = socket.inet_ntoa(socket.inet_aton(myIP)[:3] + b'\xff')
print("-------------------------------------------")
print("Select the mode from the following Choices:\n1)Receiver\n2)Sender")
mode = input()
if mode == "1":  # LSTN
    print("Receiving Selected!")
    listen()
    """ try:
        listen()
    except:
        print("Sending Faced problem!") """
elif mode == "2":  # BRDC
    print("Sending Selected!")
    broadcast(BIP)
    """ try:
        broadcast()
    except:
        print("Sending Faced problem!") """
else:
    print("The Input is not valid.")
