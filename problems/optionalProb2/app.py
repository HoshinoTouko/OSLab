import random
import threading
import time


class Producer(threading.Thread):
    def __init__(self, name="producer", breakpoint=None, reason=None, status=None):
        threading.Thread.__init__(self)
        self.name = name
        self.reason = reason
        self.breakpoint = breakpoint
        self.status = status    #status=["run", "ready", "wait", "finish"]

    def produce(self):
        temp = random.randint(0, 100)
        self.status = "ready"
        self.reason = None
        return temp

    def P(self):
        global s1
        s1 = s1 - 1
        while s1 < 0:
            self.status = "wait"
            self.reason = "Product list full."
            time.sleep(1)
        self.status = "run"
        self.reason = None

    def V(self):
        global s2
        s2 = s2 + 1
        while s2 > 10:
            self.status = "wait"
            self.reason = "Product list full"
            time.sleep(1)

    def put(self, C):
        global IN, x
        x[IN] = C
        IN = (IN+1) % 10
        print("put %s" % C)

    def run(self):
        PC = 0
        global x
        while True:
            time.sleep(0.5)
            self.breakpoint = PC
            if PC == 0:
                C = self.produce()
            elif PC == 1:
                self.P()
            elif PC == 2:
                self.put(C)
            elif PC == 3:
                self.V()
            elif PC == 4:
                PC = -1
            PC += 1


class Consumer(threading.Thread):
    def __init__(self, name="consumer", breakpoint=None, reason=None, status=None):
        threading.Thread.__init__(self)
        self.name = name
        self.reason = reason
        self.breakpoint = breakpoint
        self.status = status    #status=["run", "ready", "wait", "finish"]

    def P(self):
        global s2
        s2 = s2 - 1
        while s2 < 0:
            self.status = "wait"
            self.reason = "Product list empty."
            time.sleep(1)
        self.status = "run"
        self.reason = None

    def V(self):
        global s1
        s1 = s1 + 1
        while s1 > 10:
            self.status = "wait"
            self.reason = "Product list empty"
            time.sleep(1)
        self.status = "finish"
        self.reason = None

    def get(self):
        global OUT, x
        temp = x[OUT]
        x[OUT] = None
        OUT = (OUT+1)%10
        return temp

    def consume(self):
        global x
        print(x)

    def run(self):
        PC = 0

        while True:
            time.sleep(0.5)
            if PC == 0:
                self.P()
            elif PC == 1:
                C = self.get()
                print("get %s" % C)
            elif PC == 2:
                self.V()
            elif PC == 3:
                self.consume()
            elif PC == 4:
                PC = -1
            PC += 1
            self.breakpoint = PC


class Timethread(threading.Thread):
    def __init__(self, producer, consumer):
        threading.Thread.__init__(self)
        self.producer = producer
        self.consumer = consumer

    def run(self):
        while True:
            time.sleep(0.5)
            print((self.producer.name, self.producer.status, self.producer.reason, self.producer.breakpoint))
            print((self.consumer.name, self.consumer.status, self.consumer.reason, self.consumer.breakpoint))


if __name__ == "__main__":
    s1 = 10
    s2 = 0
    IN = 0
    OUT = 0
    x = [None] * 10
    producer = Producer()
    consumer = Consumer()
    time_thread = Timethread(producer, consumer)
    time_thread.start()
    producer.start()
    consumer.start()
