import random
import inspect
from .sorting import SortingAlgorithms
from .tree import TreeAlgorithms


class AlgorithmManager:
    def __init__(self):
        self.data = [random.randint(1, 100) for num in range(50)]
        self.highlight_indices = (-1, -1)
        self.status_message = ""
        self.sorting = SortingAlgorithms()
        self.tree = TreeAlgorithms()
        self.sorting_algos, self.tree_algos = self.get_algo_names()
        print(self.sorting_algos)
        print(self.tree_algos)
        # print(self.pathfinding_algos)

    def get_algo_names(self):
        sorting_algos = dict()
        tree_algos = dict()
        for name, member in inspect.getmembers(SortingAlgorithms()):
            if inspect.isfunction(member) or inspect.ismethod(member):
                if member.__doc__ is not None:
                    sorting_algos.update({member.__doc__: member})
        for name, member in inspect.getmembers(TreeAlgorithms()):
            if inspect.isfunction(member) or inspect.ismethod(member):
                if member.__doc__ is not None:
                    tree_algos.update({member.__doc__: member})
        return sorting_algos, tree_algos

    def reset_data(self):
        """Generates a new random dataset."""
        self.data = [random.randint(1, 100) for num in range(50)]

    def get_generator(self, algorithm):
        """Return a generator for the selected algorithm."""
        if algorithm in self.sorting_algos:
            self.status_message = f"{algorithm}ing..."
            params = inspect.signature(self.sorting_algos[algorithm]).parameters
            if len(params) > 1:
                return self.sorting_algos[algorithm](0, len(self.data) - 1, self.data)
            else:
                return self.sorting_algos[algorithm](self.data)

        if algorithm in self.tree_algos:
            self.status_message = f"{algorithm}"
            return self.tree_algos[algorithm](self.tree.tree)
            return None
