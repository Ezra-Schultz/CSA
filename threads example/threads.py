import threading

x = 0
def increment():
    global x
    x += 1

def thread_task(lock):
    for _ in range(100000):
        lock.acquire()
        increment()
        lock.release()

def main_task():
    global x
    # setting global variable x as 0
    x = 0

    # creating a lock
    lock = threading.Lock()

    # creating threads example
    thread1 = threading.Thread(target=thread_task, args=(lock,))
    thread2 = threading.Thread(target=thread_task, args=(lock,))

    # start threads example
    thread1.start()
    thread2.start()

    # wait until threads example finish their job
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    for i in range(10):
        main_task()
        print("Iteration {0}: x = {1}".format(i,x))