class MinHeap:
    """
    A Min-Heap implementation using an array.
    Provides insertion while counting operations.
    """
    def __init__(self):
        self.heap = []
        self.comparisons = 0  # Count total comparisons
        self.swaps = 0        # Count total swaps

    def insert(self, element):
        """
        Insert a new element into the heap.
        Time Complexity: O(log n) worst case, O(1.7645) average case.
        """
        self.heap.append(element)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """
        Move the element at index up to restore the heap property.
        """
        while index > 0:
            parent = (index - 1) // 2
            self.comparisons += 1  # One comparison per loop
            if self.heap[index] < self.heap[parent]:
                # Swap if child is smaller than parent
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                self.swaps += 1
                index = parent
            else:
                break

    def print_heap(self):
        """
        Print the current heap and operation counts.
        """
        print("Heap elements:", self.heap)
        print("Total comparisons:", self.comparisons)
        print("Total swaps:", self.swaps)
        print("Total operations:", self.comparisons + self.swaps)

    def reset_operations(self):
        """
        Reset operation counters.
        """
        self.comparisons = 0
        self.swaps = 0

# Example usage:
h = MinHeap()
h.insert(100)
h.insert(70)
h.insert(50)
h.insert(125)
h.insert(45)
h.insert(60)
h.insert(10)
h.print_heap()
