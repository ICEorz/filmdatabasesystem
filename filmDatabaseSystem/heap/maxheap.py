import operator
class MaxHeap(object):
    def __init__(self, maxsize=None, cmp=operator.le):
        self.maxsize = maxsize
        self._elements = []
        self._count = 0
        self.cmp = cmp

    def __len__(self):
        return self._count

    def push(self, value):
        self._elements.append(value)
        self.siftup(self._count)
        self._count += 1

    def pop(self):
        if self._count < 0:
            raise Exception('empty')
        if self._count == 0:
            return None
        value = self._elements[0]
        self._count -= 1
        self._elements[0] = self._elements[self._count]
        self._elements.pop()
        self.siftdown(0)
        return value

    def siftup(self, idx):
        if idx > 0:
            parent = int((idx-1)/2)
            if self.cmp(self._elements[parent], self._elements[idx]):
                self._elements[idx], self._elements[parent] = self._elements[parent], self._elements[idx]
                self.siftup(parent)

    def siftdown(self, idx):
        left = idx * 2 + 1
        right = idx * 2 + 2
        maxv = idx
        if (left < self._count and
                   self.cmp(self._elements[maxv], self._elements[left]) and
                   self.cmp(self._elements[right], self._elements[left])):
            maxv = left
        elif right < self._count and self.cmp(self._elements[maxv], self._elements[right]):
            maxv = right
        if maxv is not idx:
            self._elements[idx], self._elements[maxv] = self._elements[maxv], self._elements[idx]
            self.siftdown(maxv)


if __name__ == '__main__':
    a = MaxHeap(10)
    a.push(1)
    a.push(5)
    a.push(3)
    print(a.pop())
    print(a.pop())
    print(a.pop())

