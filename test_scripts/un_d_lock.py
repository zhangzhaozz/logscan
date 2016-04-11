__author__ = 'zhangzhao'

import threading
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')

_local = threading.local()


@contextmanager
def acquire(*locks):
    locks = sorted(locks, key=lambda x: id(x))

    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('lock Order violation')

    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


if __name__ == '__main__':

    x_lock = threading.Lock()
    y_lock = threading.Lock()


    def thread_1():
        while True:
            with acquire(x_lock, y_lock):
                logging.debug('Thread-1')


    def thread_2():
        while True:
            with acquire(y_lock, x_lock):
                logging.debug('Thread-2')


    # t1 = threading.Thread(target=thread_1)
    # t1.daemon = True
    # t1.start()
    #
    # t2 = threading.Thread(target=thread_2)
    # t2.daemon = True
    # t2.start()

    def philosopher(left, right):
        while True:
            with acquire(left, right):
                logging.debug('{0} eating'.format(threading.currentThread()))

    NSTICKS = 5
    chopsticks = [threading.Lock() for n in range(NSTICKS)]

    for n in range(NSTICKS):
        t = threading.Thread(target=philosopher, args=(chopsticks[n], chopsticks[(n+1) % NSTICKS]))
        t.start()