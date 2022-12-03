class Container:
    def __init__(self):
        self._size = 0

    def __len__(self):
        return self._size

    # abstract method
    def append(self, val):
        raise NotImplementedError

    # abstract method
    def pop(self):
        raise NotImplementedError


class Node:
    def __init__(self, val=None, pre=None, nxt=None):
        self.val = val
        self.pre = pre
        self.next = nxt

    def __str__(self):
        return str(self.val)


class Queue(Container):
    """Just a Double Linked List with the dummy head and tail"""

    def __init__(self):
        """
        head<-->tail
        """

        super().__init__()
        self.__head = Node()  # dummy head
        self.__tail = Node(pre=self.__head)  # dummy tail
        self.__head.next = self.__tail

    def __iter__(self):
        node = self.__head.next
        while node != self.__tail:
            yield node
            node = node.next

    def __str__(self):
        res = ', '.join(map(str, self))
        return f"[{res}]"

    def append(self, item):
        """
        insert the new element to the tail
        """
        # elegant way to insert a node
        node = Node(item, pre=self.__tail.pre, nxt=self.__tail)
        node.next.pre = node
        node.pre.next = node
        self._size += 1

    def pop(self):
        """
        delete and return the first element of the queue
        """
        assert self, 'queue is empty'
        node = self.__head.next
        res = node.val

        # elegant way to delete a node
        node.pre.next = node.next
        node.next.pre = node.pre
        del node
        self._size -= 1

        return res


class Heap(Container):
    """
    Min Heap, a complete binary tree where the key at root
    is always the minimum among all keys present in Binary Heap,
    it supports pop_minimum operations in O(log n) time complexity
    """

    def __init__(self, cmp=None):
        """
        :param cmp: a comparator(function) that the heap ordered by

        """
        super().__init__()
        cmp = cmp or (lambda x: x)
        self._comparator = cmp
        self._list = list()  # store the items of the heap

    def __str__(self):
        return str(self._list)

    def append(self, item):
        self._list.append(item)
        self._size += 1
        self._heapifyUp()

    def pop(self):
        assert self, 'heap is empty'
        self._list[0], self._list[-1] = self._list[-1], self._list[0]
        res = self._list.pop()
        self._size -= 1
        self._heapifyDown()
        return res

    def _isvalid(self, index):
        return 0 <= index < self._size

    def _parent(self, index):
        parent = (index - 1) // 2
        return parent

    def _child(self, index):
        left_child = 2 * index + 1
        if not self._isvalid(left_child):
            return -1

        right_child = left_child + 1

        '''return the smallest child'''
        if self._isvalid(right_child) and \
                self._comparator(self._list[right_child]) < \
                self._comparator(self._list[left_child]):
            return right_child

        return left_child

    def _heapifyUp(self):
        """
        Adjust the heap from bottom to up
        """
        child = self._size - 1
        parent = self._parent(child)
        # Keep adjusting until child is greater than parent
        while self._isvalid(parent):
            # for beautiful code, write in a new if statement instead of while
            if self._comparator(self._list[parent]) < self._comparator(self._list[child]):
                break
            self._list[child], self._list[parent] = self._list[parent], self._list[child]
            child = parent
            parent = self._parent(child)

    def _heapifyDown(self):
        """
        Adjust the heap from up to bottom
        """
        if len(self) == 0:
            return

        parent = 0
        child = self._child(parent)
        # Keep adjusting until parent is smaller than child
        while self._isvalid(child):
            # for beautiful code, write in a new if statement instead of while
            if self._comparator(self._list[parent]) < self._comparator(self._list[child]):
                break
            self._list[child], self._list[parent] = self._list[parent], self._list[child]
            parent = child
            child = self._child(parent)


class DistinctHeap(Heap):
    """
    Distinct Min Heap, where every item in the heap is unique,
    implemented by a list combined with a dict,
    use list to store the items and implement the priority queue by some algorithms,
    use dict to map the item to it's index in the list,
    dict can make sure the items are unique, and can be find in constant time
    """

    def __init__(self, key=None, cmp=None):
        """
        :param key: a function that returns one element as the key of dict,
            if two different items have the same key, the smallest one are preserved,
            if not given, use the whole item as the key(that item must be hashable)

        :param cmp: a comparator(function) that the heap is ordered by, which will return a
                    numerical value as the measure of that item
        """
        super().__init__(cmp)
        key = key or (lambda x: x)
        self.__key = key
        self.__dict = dict()  # store the ({key of the item}, {index of the item}) pairs

    def _heapifyUp(self, index=None):
        """

        :param index: heapifyUp the particular item that the index point to,
                    default is None(begin from the last item)
        :return: None
        """
        child = index or self._size - 1
        parent = self._parent(child)

        while self._isvalid(parent):
            if self._comparator(self._list[parent]) < self._comparator(self._list[child]):
                break
            # adjust the list and dict
            self._list[child], self._list[parent] = self._list[parent], self._list[child]
            self.__dict[self.__key(self._list[child])] = child
            self.__dict[self.__key(self._list[parent])] = parent

            child = parent
            parent = self._parent(child)

    def _heapifyDown(self):
        if len(self) == 0:
            return

        parent = 0
        child = self._child(parent)

        while self._isvalid(child):
            if self._comparator(self._list[parent]) < self._comparator(self._list[child]):
                break
            # adjust the list and dict
            self._list[child], self._list[parent] = self._list[parent], self._list[child]
            self.__dict[self.__key(self._list[child])] = child
            self.__dict[self.__key(self._list[parent])] = parent

            parent = child
            child = self._child(parent)

    def append(self, item):
        key = self.__key(item)
        if key in self.__dict:
            index = self.__dict[key]
            new_val = self._comparator(item)
            old_val = self._comparator(self._list[index])
            if new_val > old_val:  # if new item is greater than the old, just ignore it
                return

            # update the list and dict, then heapifyUp
            self._list[index] = item
            self.__dict[key] = index
            self._heapifyUp(index)
        else:
            self._list.append(item)
            self.__dict[key] = self._size
            self._size += 1
            self._heapifyUp()

    def pop(self):
        assert self, 'heap is empty'
        self._list[0], self._list[-1] = self._list[-1], self._list[0]
        self.__dict[self.__key(self._list[0])] = 0

        res = self._list.pop()
        self.__dict.pop(self.__key(res))

        self._size -= 1
        self._heapifyDown()
        return res


if __name__ == '__main__':
    import random

    def test_queue():
        lst = [random.randint(0, 100) for _ in range(100)]
        queue = Queue()
        for val in lst:
            queue.append(val)
        assert [queue.pop() for _ in range(len(queue))] == lst
        print("queue pass test")


    def test_heap():
        heap = Heap()
        distinct_heap = DistinctHeap()
        # do 1000 times heap sort
        for i in range(1000):
            li = [random.randint(0, 100) for _ in range(1000)]
            for item in li:
                heap.append(item)
                distinct_heap.append(item)
            sorted_1 = [heap.pop() for _ in range(len(heap))]
            sorted_2 = [distinct_heap.pop() for _ in range(len(distinct_heap))]
            assert sorted_1 == sorted(li)
            assert sorted_2 == sorted(set(li))
        print("heap pass test")


    test_queue()
    test_heap()
