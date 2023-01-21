from threading import Thread, Lock
import random
import time


class Philosopher(Thread):

    def __init__(self, index, left_fork, right_fork, semaphore):
        super(Philosopher, self).__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.semaphore = semaphore

    def run(self):
        for i in range(10):
            print(f'Philosopher {self.index} is hungry.')
            self.dine()
            time.sleep(5)

    def pickup_forks(self):
        self.left_fork.acquire()
        self.right_fork.acquire()

    def putdown_forks(self):
        self.left_fork.release()
        self.right_fork.release()

    def dine(self):
        with self.semaphore:
            self.pickup_forks()

        print(f'Philosopher {self.index} starts eating.')
        time.sleep(5)
        print(f'Philosopher {self.index} finishes eating and leaves to think.')

        self.putdown_forks()


if __name__ == "__main__":
    forks = [Lock() for n in range(5)]
    semaphore = Lock()

    philosophers = [Philosopher(i, forks[i % 5], forks[(i + 1) % 5], semaphore)
                    for i in range(5)]

    for p in philosophers: p.start()
    for p in philosophers: p.join()
