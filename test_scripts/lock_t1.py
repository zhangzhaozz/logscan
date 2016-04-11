__author__ = 'zhangzhao'

import threading
import time
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


class ShareCounter:
    def __init__(self, initial_value = 0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self, delta = 1):
        with self._value_lock:
            self._value += delta
            logging.debug('incr_value is {0}'.format(self._value))

    def decr(self, delta = 1):
        with self._value_lock:
            self._value -= delta
            logging.debug('decr_value is {0}'.format(self._value))

sc = ShareCounter()

threading.Thread(target=sc.incr, name='t1', args=(5, )).start()
threading.Thread(target=sc.decr, name='t2', args=(3, )).start()