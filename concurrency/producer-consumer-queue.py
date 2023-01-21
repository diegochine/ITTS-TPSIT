from threading import Thread
from queue import Queue
import time
import random


class Producer(Thread):
    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue: Queue = queue

    def run(self):
        docs = ['rick.pdf', 'and.pdf', 'morty.pdf', 'wabbalabbadubdub.pdf']
        while True:
            doc = random.choice(docs)
            self.queue.put(doc)
            print(f"Produced {doc}")
            time.sleep(random.random())


class Consumer(Thread):
    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue: Queue = queue

    def run(self):
        while True:
            doc = self.queue.get(block=True)
            print(f"Consumed {doc}")
            time.sleep(random.random())


class Manager:
    def __init__(self):
        super().__init__()
        self.queue = Queue(maxsize=3)
        self.producer = Producer(queue=self.queue)
        self.consumer = Consumer(queue=self.queue)

    def go(self):
        self.producer.start()
        self.consumer.start()
        time.sleep(100)


if __name__ == '__main__':
    manager = Manager()
    manager.go()
