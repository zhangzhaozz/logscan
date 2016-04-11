__author__ = 'zhangzhao'

import threading
import random
import time

queue = []

con = threading.Condition()


class Producer(threading.Thread):
    def run(self):
        while True:
            if con.acquire():
                if len(queue) > 15:
                    con.wait()
                else:
                    elem = random.randrange(100)
                    queue.append(elem)
                    print("Producer a elem {}, Now size is {}".format(elem, len(queue)))
                    time.sleep(random.random())
                    con.notify()
                con.release()


class Consumer(threading.Thread):
    def run(self):
        while True:
            if con.acquire():
                if len(queue) < 1:
                    con.wait()
                else:
                    elem = queue.pop()
                    print("Consumer a elem {}, Now size is {}".format(elem, len(queue)))
                    time.sleep(random.random())
                    con.notify()
                con.release()


def main():

    for _ in range(3):
        Producer().start()

    for _ in range(3):
        Consumer().start()


if __name__ == '__main__':
    main()