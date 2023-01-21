from threading import Thread, Lock
import time


def thread_a(lock1: Lock, lock2: Lock):
    print('Thread A waiting to acquire lock 1.')
    lock1.acquire()
    print('Thread A has acquired lock 1, performing some calculation...')
    time.sleep(2)
    print('Thread A waiting to acquire lock 2.')
    lock2.acquire()
    print('Thread A has acquired lock 2, performing some calculation...')
    time.sleep(2)
    print('Thread A releasing both locks.')
    lock1.release()
    lock2.release()


def thread_b(lock1: Lock, lock2: Lock):
    print('Thread B waiting to acquire lock 2.')
    lock2.acquire()
    print('Thread B has acquired lock 2, performing some calculation...')
    time.sleep(5)
    print('Thread B waiting to acquire lock 1.')
    lock1.acquire()
    print('Thread B has acquired lock 1, performing some calculation...')
    time.sleep(5)
    print('Thread B releasing both locks.')
    lock2.release()
    lock1.release()


if __name__ == '__main__':
    lock1 = Lock()
    lock2 = Lock()
    thread1 = Thread(target=thread_a, args=(lock1, lock2))
    thread2 = Thread(target=thread_b, args=(lock1, lock2))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    print('Finished.')
