__author__ = 'zhangzhao'

import threading
import logging
import time



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')

def consumer(cond):
    with cond:
        cond.wait()
        logging.debug("consumer")


def producer(cond):
    with cond:
        time.sleep(2)
        logging.debug("producer")
        cond.notify_all()

if __name__ == '__main__':
    cond = threading.Condition()
    c1 = threading.Thread(target=consumer, args=(cond, ), name='consumer1')
    c1.start()
    c2 = threading.Thread(target=consumer, args=(cond, ), name='consumer2')
    c2.start()

    p = threading.Thread(target=producer, args=(cond, ), name="producer")
    p.start()