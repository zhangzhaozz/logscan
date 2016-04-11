__author__ = 'zhangzhao'

import os
from queue import Queue
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from .check import CheckerChain


class Watcher(FileSystemEventHandler):
    def __init__(self, filename, counter):
        # 获取文件的绝对路径
        self.filename = os.path.abspath(filename)
        # 保存matcher对象
        # self.matcher = Matcher(checker.name, checker.expr)
        # self.checker = checker
        self.queue = Queue()
        self.check_chain = CheckerChain(self.queue, counter)
        self.observer = Observer()
        self.fd = None
        self.offset = 0
        if os.path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = os.path.getsize(self.filename)

    def on_moved(self, event):
        if os.path.abspath(event.src_path) == self.filename:
            self.fd.close()
        if os.path.abspath(event.dest_path) == self.filename and os.path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = os.path.getsize(self.filename)

    def on_created(self, event):
        if os.path.abspath(event.src_path) == self.filename and os.path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = os.path.getsize(self.filename)

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == self.filename:
            self.fd.seek(self.offset, 0)
            # match = getattr(self.matcher, 'match', lambda x: False)
            for line in self.fd:
                line = line.rstrip('\n')
                self.queue.put(line)
                # if self.matcher.match(line):
                #     # print('matched {0}'.format(line))
                #     if self.counter is not None:
                #         self.counter.inc(self.matcher.name)
            self.offset = self.fd.tell()

    def on_deleted(self, event):
        if os.path.abspath(event.src_path) == self.filename:
            self.fd.close()

    def start(self):
        self.check_chain.start()
        self.observer.schedule(self, os.path.dirname(self.filename), recursive=False)
        self.observer.start()
        self.observer.join()

    def stop(self):
        self.check_chain.stop()
        self.observer.stop()
        if self.fd is not None and not self.fd.closed:
            self.fd.close()


if __name__ == '__main__':
    import sys
    import threading

    class Matcher:
        def match(self, line):
            return True

    w = Watcher(sys.argv[1], Matcher())
    w2 = Watcher(sys.argv[2], Matcher())

    try:
        # w.start()
        t1 = threading.Thread(target=w.start)
        t1.start()
        t2 = threading.Thread(target=w2.start)
        t2.start()
    except KeyboardInterrupt:
        w.stop()
        w2.stop()
