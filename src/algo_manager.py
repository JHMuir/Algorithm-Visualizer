import random
from .sorting import SortingAlgorithms
from .pathfinding import PathfindingAlgorithms


class AlgorithmManager:
    def __init__(self):
        self.data = [random.randint(1, 100) for num in range(50)]
        self.sorting = SortingAlgorithms(data=self.data)
        self.pathfinding = PathfindingAlgorithms(data=self.data)
        self.highlight_indices = (-1, -1)
        self.status_message = ""

    def reset_data(self):
        """Generates a new random dataset."""
        self.data = [random.randint(1, 100) for num in range(50)]
        self.sorting.data = self.data
        self.pathfinding.data = self.data

    def get_generator(self, algorithm):
        """Return a generator for the selected algorithm."""
        if algorithm == "Bubble Sort":
            return self.sorting.bubble_sort()
        elif algorithm == "Quick Sort":
            return self.sorting.quick_sort(0, len(self.data) - 1)
        elif algorithm == "Merge Sort":
            return self.sorting.merge_sort(0, len(self.data) - 1)
        elif algorithm == "Insertion Sort":
            return self.sorting.insertion_sort()
