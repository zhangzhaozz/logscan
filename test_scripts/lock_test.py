__author__ = 'zhangzhao'


import threading
import time

balance = 0
muxlock = threading.Lock()


def change_it(n):
    muxlock.acquire()
    global balance
    balance = balance + n
    balance = balance - n
    muxlock.release()


def run_thread(n):
    for i in range(20):
        change_it(n)


t1 = threading.Thread(target=change_it, args=(5,))
t2 = threading.Thread(target=change_it, args=(8,))
t3 = threading.Thread(target=change_it, args=(9,))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()

print(balance)