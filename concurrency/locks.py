import threading
import time


class FakeDB:

    def __init__(self):
        self.value: int = 0
        self.mutex: threading.Lock = threading.Lock()

    def update(self):
        print(f'Thread {threading.get_native_id()} starting update')
        self.mutex.acquire()
        data = self.value
        data += 1
        time.sleep(0.1)
        self.value = data
        self.mutex.release()
        print(f'Thread {threading.get_native_id()} finished update')


def update_db(db: FakeDB) -> None:
    print(f"Thread {threading.get_native_id()} updating DB")
    db.update()


if __name__ == '__main__':
    db = FakeDB()
    t1 = threading.Thread(target=update_db, args=(db,))
    t2 = threading.Thread(target=update_db, args=(db,))
    t3 = threading.Thread(target=update_db, args=(db,))
    print(f"Starting threads, current DB value: {db.value}\n")
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print(f'Threads finished, current DB value: {db.value}')
