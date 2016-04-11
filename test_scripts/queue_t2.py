__author__ = 'zhangzhao'

import threading
import queue
import random
import time
import logging



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


class Producer(threading.Thread):
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        for i in range(10):
            randomnum = random.randint(1, 99)
            self.queue.put(randomnum)
            logging.debug('put num {0} in Queue'.format(randomnum))
            time.sleep(1)
        logging.debug('put queue none!')


class ConsumeEven(threading.Thread):
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        while True:
            try:
                queue_val = self.queue.get()
            except Exception as e:
                logging.error(e)
                break

            if queue_val % 2 == 0:
                logging.debug('Get Even Num {0}'.format(queue_val))
            else:
                self.queue.put(queue_val)


if __name__ == '__main__':
    queue = queue.Queue()
    pt = Producer('producer', queue)
    pt.start()
    pt.join()
    ce = ConsumeEven('consumeeven', queue)
    ce.start()
    ce.join()
