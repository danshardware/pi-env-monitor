import threading
import sys

class sampleRing:
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.pos = -1
        self.data = [None] * maxSize
        self.lock = threading.Lock()

    def push(self, data):
        try:
            self.lock.acquire()
            if hasattr(data, "__len__"):
                for i in data:
                    self.pos = (self.pos + 1) % self.maxSize
                    self.data[self.pos] = i
            else:
                self.pos = (self.pos + 1) % self.maxSize
                self.data[self.pos] = data
        except:
            print("[Error] Problem pushing to array", file = sys.stderr)
        if self.lock.locked:
            self.lock.release()
    
    def clear(self):
        self.lock.acquire()
        self.data = None
        self.data = [None] * self.maxSize
        self.pos = -1
        self.lock.release()

    def stats(self):
        sum = 0
        output = {
            'max': self.data[0],
            'min': self.data[0],
            'avg': 0,
            'num': 0,
            'last': (self.data[self.pos], None)[self.pos == -1]
        }
        self.lock.acquire()
        try:
            for i in self.data:
                if not i is None:
                    output["num"] += 1
                    sum += i
                    if (i > output["max"]):
                        output["max"] = i
                    if (i < output["min"]):
                        output["min"] = i
                    if (output["num"] > 0):
                        output["avg"] = sum / output["num"]
        except:
            print ('[Error] Failed to get stats', file = sys.stderr)
            print (self.data)
        self.lock.release()
        return output  

# Tests
if __name__ == "__main__":
    myRing = sampleRing(6)
    myRing.push([2, 4, 6, 8, 10, 12, 14])
    stats = myRing.stats()
    print(stats)
    assert stats["max"] == 14, "Max should be 14"
    assert stats["min"] == 4, "Min should be 4"
    assert stats["avg"] == 9, "Avg should be 9"
    assert stats["num"] == 6, "Num should be 6"

    myRing = None
    myRing = sampleRing(6)
    myRing.push([2, 4, 6])
    stats = myRing.stats()
    print(stats)
    assert stats["max"] == 6, "Max should be 6"
    assert stats["min"] == 2, "Min should be 2"
    assert stats["avg"] == 4, "Avg should be 4"
    assert stats["num"] == 3, "Num should be 3"

    myRing.clear()
    myRing.push([2, 4, 6])
    stats = myRing.stats()
    print(stats)
    assert stats["max"] == 6, "Max should be 6"
    assert stats["min"] == 2, "Min should be 2"
    assert stats["avg"] == 4, "Avg should be 4"
    assert stats["num"] == 3, "Num should be 3"
