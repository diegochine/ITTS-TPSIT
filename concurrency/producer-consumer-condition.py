from threading import Thread, Condition
from collections import deque
import time
import random


class Producer(Thread):
    def __init__(self, queue, condition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue: deque = queue
        self.condition: Condition = condition

    def run(self):
        docs = ['rick.pdf', 'and.pdf', 'morty.pdf', 'wabbalabbadubdub.pdf']
        while True:
            doc = random.choice(docs)
            self.condition.acquire()
            self.queue.append(doc)
            print(f"Produced {doc}")
            self.condition.notify()  # avvisa il consumer che c'è qualcosa da fare
            self.condition.release()
            time.sleep(random.random())


class Consumer(Thread):
    def __init__(self, queue, condition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue: deque = queue
        self.condition: Condition = condition

    def run(self):
        while True:
            self.condition.acquire()
            if len(self.queue) == 0:
                self.condition.wait()
            doc = self.queue.pop()
            print(f"Consumed {doc}")
            self.condition.release()
            time.sleep(random.random())


class Manager:
    def __init__(self):
        super().__init__()
        self.queue = deque(maxlen=3)
        self.condition = Condition()
        self.producer = Producer(queue=self.queue, condition=self.condition)
        self.consumer = Consumer(queue=self.queue, condition=self.condition)

    def go(self):
        self.producer.start()
        self.consumer.start()
        time.sleep(100)


if __name__ == '__main__':
    manager = Manager()
    manager.go()
