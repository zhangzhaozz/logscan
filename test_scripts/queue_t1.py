__author__ = 'zhangzhao'

import threading
import queue
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


class Producer(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue

    def run(self):
        num = 1
        while True:
            self.work_queue.put(num)
            num += 1
            time.sleep(1)


class Printer(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue

    def run(self):
        while True:
            num = self.work_queue.get()
            # self.work_queue.task_done()
            logging.debug('num is {0}'.format(num))


def main():
    work_queue = queue.Queue()

    producer = Producer(work_queue)
    producer.daemon = True
    producer.start()

    printer = Printer(work_queue)
    printer.daemon = True
    printer.start()

    work_queue.join()


if __name__ == '__main__':
    main()
