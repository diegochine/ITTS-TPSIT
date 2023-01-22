from threading import Thread, Lock
import tkinter as tk
from tkinter import ttk
import random
import time


class Philosopher(Thread):

    def __init__(self, index, left_fork, right_fork, label):
        super(Philosopher, self).__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.label = label

    def run(self):
        for _ in range(10):
            self.pickup_forks()
            self.eat()
            self.putdown_forks()
            self.think()

    def pickup_forks(self):
        self.left_fork.acquire()
        # time.sleep(0.00001) # remove comment to cause deadlock
        locked = self.right_fork.acquire(False)
        if not locked:
            self.label['text'] = 'HUNGRY [LEFT FORK]'
            self.right_fork.acquire()

    def putdown_forks(self):
        self.left_fork.release()
        self.right_fork.release()

    def think(self):
        self.label['text'] = 'THINKING'
        time.sleep(random.randint(3, 10))
        self.label['text'] = 'HUNGRY'

    def eat(self):
        self.label['text'] = 'EATING'
        time.sleep(random.randint(3, 10))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('600x300')
    root.title('Dining philosophers')
    root.grid()

    forks = [Lock() for n in range(5)]
    philosophers = []

    for i in range(5):
        name_label = ttk.Label(root, text=f'Philosopher {i}', font=("Colibri", 22))
        name_label.grid(column=0, row=i * 2, columnspan=2)
        ttk.Label(root, text='\t').grid(column=2, row=i * 2, columnspan=2)

        status_label = ttk.Label(root, text=f'HUNGRY', font=("Colibri", 22))
        status_label.grid(column=4, row=i * 2, columnspan=3)

        philosopher = Philosopher(i, forks[i % 5], forks[(i + 1) % 5], status_label)
        philosophers.append(philosopher)

    for p in philosophers: p.start()

    root.mainloop()
