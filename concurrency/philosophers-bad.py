from threading import Thread, Lock
import random
import time


class Philosopher(Thread):

    def __init__(self, index, left_fork, right_fork):
        super(Philosopher, self).__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        for i in range(10):
            print(f'Philosopher {self.index} is hungry.')
            self.dine()
            time.sleep(5)

    def dine(self):
        self.left_fork.acquire()
        self.right_fork.acquire()

        print(f'Philosopher {self.index} starts eating.')
        time.sleep(5)
        print(f'Philosopher {self.index} finishes eating and leaves to think.')

        self.left_fork.release()
        self.right_fork.release()


if __name__ == "__main__":
    locks = [Lock() for n in range(5)]

    philosophers = [Philosopher(i, locks[i % 5], locks[(i + 1) % 5])
                    for i in range(5)]

    for p in philosophers: p.start()
    for p in philosophers: p.join()
