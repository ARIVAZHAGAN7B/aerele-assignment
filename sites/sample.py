import threading
import time

lock = threading.Lock()

def work(name):
    print(name, "waiting")

    with lock:
        print(name, "started")
        time.sleep(5)
        print(name, "finished")

t1 = threading.Thread(target=work, args=("Worker 1",))
t2 = threading.Thread(target=work, args=("Worker 2",))

t1.start()
t2.start()

t1.join()
t2.join()