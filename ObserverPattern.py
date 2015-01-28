__author__ = 'tristan_dev'


class Subject:

    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def unregister(self, observer):
        self._observers.remove(observer)

    def update_state(self):
        for observer in self._observers:
            observer.update()


class Observer:

    def __init__(self, subject):
        self._subject = subject
        subject.register(self)

    def update(self):
        pass