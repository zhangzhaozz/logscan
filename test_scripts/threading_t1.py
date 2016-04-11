__author__ = 'zhangzhao'

from threading import Thread, Event
import logging
import time


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            logging.debug(n)
            n -= 1
            time.sleep(2)


# c = CountdownTask()
# t = Thread(target=c.run, args=(10, ))
# t.start()
# # c.terminate()
# t.join()


def Countdown(n, started_evt):
    logging.debug('countdown starting')
    started_evt.set()
    while n > 0:
        logging.debug('T-minus {0}'.format(n))
        n -= 1
        time.sleep(3)

started_evt = Event()
logging.debug('Launching countdown')
t = Thread(target=Countdown, args=(10, started_evt))
t.start()

started_evt.wait()
logging.debug('countdown is running')