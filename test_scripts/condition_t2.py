__author__ = 'zhangzhao'

from threading import Thread, Condition
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = Condition()

    def start(self):
        t = Thread(target=self.run)
        t.daemon = True

        t.start()

    def run(self):
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1
                self._cv.notify_all()

    def wait_for_tick(self):
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()


def countdown(nticks, ptimer):
    while nticks > 0:
        ptimer.wait_for_tick()
        logging.debug('T-minus {0}'.format(nticks))
        nticks -= 1


def countup(last, ptimer):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        logging.debug('Counting {0}'.format(n))
        n += 1


ptimer = PeriodicTimer(5)
ptimer.start()

Thread(target=countdown, args=(10, ptimer)).start()
Thread(target=countup, args=(5, ptimer)).start()
