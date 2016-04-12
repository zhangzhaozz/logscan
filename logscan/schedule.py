__author__ = 'zhangzhao'

import logging
from os import path
from watchdog.observers import Observer
from base64 import urlsafe_b64decode
from .count import Counter
from .notification import Notifier
from .watch import WatcherHandler
from .persistence import OffsetPersistence


class Schedule:
    def __init__(self, config):
        self.observer = Observer()
        self.watchers = {}
        self.handlers = {}
        self.counter = Counter()
        self.notifier = Notifier(config)
        self.offset_db = OffsetPersistence(config)

    def __make_key(self, filename):
        return path.abspath(urlsafe_b64decode(filename).decode())

    def add_watcher(self, filename):
        filename = self.__make_key(filename)
        if path.abspath(filename) not in self.handlers.keys():
            handler = WatcherHandler(filename, counter=self.counter,
                                     notifier=self.notifier, offset_db=self.offset_db)
            if path.dirname(handler.filename) not in self.watchers.keys():
                self.watcher[path.dirname(handler.filename)] = self.observer.schedule(handler,
                                                                                      path.dirname(handler.filename),
                                                                                      recursive=False)
            else:
                watch = self.watchers[path.dirname(handler.filename)]
                self.observer.add_handler_for_watch(handler, watch)
            self.handlers[handler.filename] = handler
            handler.start()

    def remove_watcher(self, filename):
        key = self.__make_key(filename)
        handler = self.handlers.pop(key)
        if handler is None:
            watch = self.watchers[path.dirname(key)]
            self.observer.remove_handler_for_watch(handler, watch)
            handler.stop()
            if not self.observer._handlers[watch]:
                self.observer.unschedule(watch)
                self.watchers.pop(path.dirname(handler.filename))

    def add_monitor(self, filename, name, src):
        key = self.__make_key(filename)
        handler = self.handlers.get(key)
        if handler is None:
            logging.warning('watcher {0} not found, auto add it'.format(filename))
            self.add_watcher(filename)
            handler = self.handlers.get(key)
        handler.monitor.add(filename, name, src)

    def remove_monitor(self, filename, name):
        key = self.__make_key(filename)
        handler = self.handlers.get(key)
        if handler is None:
            logging.warning('watcher {0} not found'.format(filename))
            return
        handler.monitor.remove(name)

    def start(self):
        self.observer.start()
        self.notifier.start()

    def join(self):
        self.observer.join()

    def stop(self):
        self.observer.stop()
        for handler in self.handlers.values():
            handler.stop()
        self.notifier.stop()
        self.offset_db.close()
