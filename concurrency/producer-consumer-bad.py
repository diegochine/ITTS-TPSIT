from threading import Thread, Lock
from collections import deque
import time
import random


class Producer(Thread):
    def __init__(self, queue, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.lock = lock

    def run(self):
        docs = ['rick.pdf', 'and.pdf', 'morty.pdf', 'wabbalabbadubdub.pdf']
        while True:
            doc = random.choice(docs)
            while len(self.queue) == self.queue.maxlen:
                print('Producer is busy waiting')  # bad!
            self.lock.acquire()
            self.queue.append(doc)
            print(f"Produced {doc}")
            self.lock.release()
            time.sleep(random.random())


class Consumer(Thread):
    def __init__(self, queue, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.lock = lock

    def run(self):
        while True:
            while len(self.queue) == 0:
                print('Consumer is busy waiting')  # bad!
            self.lock.acquire()
            doc = self.queue.pop()
            print(f"Consumed {doc}")
            self.lock.release()
            time.sleep(random.random())


class Manager:
    def __init__(self):
        super().__init__()
        self.queue = deque(maxlen=3)
        self.lock = Lock()
        self.producer = Producer(queue=self.queue, lock=self.lock)
        self.consumer = Consumer(queue=self.queue, lock=self.lock)

    def go(self):
        self.producer.start()
        self.consumer.start()
        time.sleep(10)


if __name__ == '__main__':
    manager = Manager()
    manager.go()
