import threading
import logging
import time


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


def worker():
    time.sleep(2)
    logging.debug('i am worker')

def wrap(s):
    with s:
        worker()


if __name__ == '__main__':
    s = threading.BoundedSemaphore(3)
    for x in range(10):
        threading.Thread(target=wrap, args=(s, ), name='worker-{0}'.format(x)).start()
