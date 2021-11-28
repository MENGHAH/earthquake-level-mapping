import random
from threading import Thread
from Queue import Queue

resqueue = Queue()
aqueue = Queue()
bqueue = Queue()
cqueue = Queue()

def producer():
    list1=list(range(100))

    for _ in range(2000):
        for each in list1:
            x=r.randint(i+30,i+60)+each
            y=r.randint(i+60,i+120)+each
            z=r.randint(i+60,i+180)+each

            res=2.5*x-y-z
            resqueue.put(res)

            if res>=50:
                aqueue.put(each)
            if -50<res<50:
                bqueue.put(each)
            if res<=-50:
                cqueue.put(each)

def consumer_a():
    while True:
        try:
            data = aqueue.get(timeout=5)
        except Queue.Empty:
            return
        else:
            # 耗时操作
            deal_data(data)
            aqueue.task_done()

def consumer_b():
    while True:
        try:
            data = bqueue.get(timeout=5)
        except Queue.Empty:
            return
        else:
            # 耗时操作
            deal_data(data)
            bqueue.task_done()

 def consumer_c():
    while True:
        try:
            data = cqueue.get(timeout=5)
        except Queue.Empty:
            return
        else:
            # 耗时操作
            deal_data(data)
            cqueue.task_done()

 def consumer_res():
    while True:
        try:
            data = resqueue.get(timeout=5)
        except Queue.Empty:
            return
        else:
            # 耗时操作
            deal_data(data)
            resqueue.task_done()

if __name__ == "__main__":
    t1 = Thread(target=producer)
    t2 = Thread(target=consumer_a)
    ...

    t1.start()
    t2.start()