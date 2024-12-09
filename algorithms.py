import random

class AlgorithmManager:
    """Handles sorting algorithms and generators."""

    def __init__(self):
        self.data = []
        self.highlight_indices = (-1, -1)
        self.status_message = ""

    def reset_data(self, size=50):
        """Generate a new random dataset."""
        self.data = [random.randint(1, 100) for _ in range(size)]
        self.highlight_indices = (-1, -1)

    def get_generator(self, algorithm):
        """Return a generator for the selected algorithm."""
        if algorithm == "Bubble Sort":
            return self.bubble_sort()
        elif algorithm == "Quick Sort":
            return self.quick_sort(0, len(self.data) - 1)
        elif algorithm == "Merge Sort":
            return self.merge_sort(0, len(self.data) - 1)
        elif algorithm == "Insertion Sort":
            return self.insertion_sort()

    # Sorting algorithms as generators
    def bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.highlight_indices = (j, j + 1)
                self.status_message = f"Comparing indices {j} and {j + 1}"
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                yield

    def quick_sort(self, low, high):
        if low < high:
            pivot_index = yield from self.partition(low, high)
            yield from self.quick_sort(low, pivot_index - 1)
            yield from self.quick_sort(pivot_index + 1, high)

    def partition(self, low, high):
        pivot = self.data[high]
        i = low - 1
        for j in range(low, high):
            self.highlight_indices = (j, high)
            self.status_message = f"Comparing index {j} with pivot {high}"
            if self.data[j] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
            yield
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        return i + 1

    def merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            yield from self.merge_sort(left, mid)
            yield from self.merge_sort(mid + 1, right)
            yield from self.merge(left, mid, right)

    def merge(self, left, mid, right):
        temp = self.data[left:right + 1]
        i, j, k = 0, mid - left + 1, left
        while i <= mid - left and j <= right - left:
            self.highlight_indices = (left + i, left + j)
            self.status_message = f"Merging indices {left + i} and {left + j}"
            if temp[i] <= temp[j]:
                self.data[k] = temp[i]
                i += 1
            else:
                self.data[k] = temp[j]
                j += 1
            k += 1
            yield
        while i <= mid - left:
            self.data[k] = temp[i]
            i += 1
            k += 1
            yield
        while j <= right - left:
            self.data[k] = temp[j]
            j += 1
            k += 1
            yield

    def insertion_sort(self):
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and key < self.data[j]:
                self.highlight_indices = (j, i)
                self.status_message = f"Inserting element {i} at position {j}"
                self.data[j + 1] = self.data[j]
                j -= 1
                yield
            self.data[j + 1] = key
            yield