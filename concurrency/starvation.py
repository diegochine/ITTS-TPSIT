import threading
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread, Lock


def thread_fun(lock: Lock, pb: ttk.Progressbar):
    p = 0
    while True:
        with lock:
            p = (p + 1) % 100
            print(f'{threading.current_thread()}, {p}')
            pb['value'] = p
            pb.update_idletasks()
            root.update_idletasks()
            time.sleep(0.1)  # execute computations


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x300')
    root.title('Starvation demo')
    root.grid()

    lock = Lock()

    for i in range(5):
        pb = ttk.Progressbar(
            root,
            orient='horizontal',
            mode='determinate',
            length=600
        )
        pb.grid(column=3, row=i, columnspan=10, padx=10, pady=20)
        pb['maximum'] = 100

        label = ttk.Label(root, text=f'Thread {i}')
        label.grid(column=0, row=i, columnspan=2)

        t = Thread(target=thread_fun, args=(lock, pb))
        t.start()

    root.mainloop()
