__author__ = 'zhangzhao'

import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


def worker(message):
    # time.sleep(10)
    logging.debug("worker is started, {0}".format(message))


if __name__ == '__main__':
    # t = threading.Thread(target=worker, name='worker', args=("ha ha ha", ))
    t = threading.Thread(target=worker, name='worker', kwargs={'message': 'ah ah ah'})
    # print(t.name)
    # print(t.is_alive())
    t.daemon = True
    t.start()
    t.join()
    # logging.debug("i am main thread")
    logging.debug("main thread exiting")
