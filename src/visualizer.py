from gi.repository import Gtk, GLib
from .status import StatusManager
from .algo_manager import AlgorithmManager
from .canvas import SortingCanvas, TreeCanvas


class AlgorithmVisualizer(Gtk.Window):
    """Main application class."""

    def __init__(self):
        super().__init__(title="Algorithm Visualizer")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        # Components
        self.algorithm_manager = AlgorithmManager()
        self.sorting_canvas = SortingCanvas(self.algorithm_manager)
        self.tree_canvas = TreeCanvas(self.algorithm_manager)
        self.current_canvas = self.sorting_canvas
        self.status_manager = StatusManager()

        # Layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.main_box)

        # Toolbar
        self.toolbar = Gtk.Box(spacing=10)
        self.main_box.pack_start(self.toolbar, False, False, 0)

        # Visualization Selection
        self.visualization_type = Gtk.ComboBoxText()
        self.visualization_type.append_text("Sorting")
        self.visualization_type.append_text("Tree Traversal")
        self.visualization_type.set_active(0)
        self.visualization_type.connect("changed", self.on_visualization_type_changed)
        self.toolbar.pack_start(self.visualization_type, False, False, 0)

        # Algorithm selection
        self.dropdown = Gtk.ComboBoxText()
        self.update_algorithm_dropdown()
        self.toolbar.pack_start(self.dropdown, False, False, 0)

        # Buttons
        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.start_visualization)
        self.toolbar.pack_start(self.start_button, False, False, 0)

        self.reset_button = Gtk.Button(label="Reset")
        self.reset_button.connect("clicked", self.reset_visualizer)
        self.toolbar.pack_start(self.reset_button, False, False, 0)

        # Canvas and Status
        self.main_box.pack_start(self.current_canvas, True, True, 0)
        self.main_box.pack_start(self.status_manager, False, False, 0)

        # Initialize
        # self.reset_visualizer()

    def update_algorithm_dropdown(self):
        self.dropdown.remove_all()

        if self.visualization_type.get_active_text() == "Sorting":
            for algo in self.algorithm_manager.sorting_algos.keys():
                self.dropdown.append_text(algo)
        else:
            for algo in self.algorithm_manager.tree_algos.keys():
                self.dropdown.append_text(algo)
        self.dropdown.set_active(0)

    def on_visualization_type_changed(self, widget):
        self.main_box.remove(self.current_canvas)

        if widget.get_active_text() == "Sorting":
            self.current_canvas = self.sorting_canvas
        else:
            self.current_canvas = self.tree_canvas
            self.algorithm_manager.tree.create_sample_tree()

        self.main_box.pack_start(self.current_canvas, True, True, 0)
        self.main_box.reorder_child(self.current_canvas, 1)
        self.update_algorithm_dropdown()
        self.current_canvas.queue_draw()

    def reset_visualizer(self, widget):
        """Reset the dataset."""
        self.algorithm_manager.reset_data()
        self.status_manager.update_status("Visualizer has been reset.")
        self.current_canvas.queue_draw()

    def start_visualization(self, widget):
        """Start the sorting animation."""
        if self.algorithm_manager.get_generator(self.dropdown.get_active_text()):
            self.algorithm_manager.highlight_indices = (-1, -1)
            generator = self.algorithm_manager.get_generator(
                self.dropdown.get_active_text()
            )
            print(self.dropdown.get_active_text())
            print(generator)

            self.animate_visualization(generator)

    def animate_visualization(self, generator):
        """Animate the sorting process."""

        def step():
            try:
                if self.current_canvas == self.tree_canvas:
                    node = next(generator)
                    if isinstance(node, self.algorithm_manager.tree.Node):
                        self.tree_canvas.current_highlighted = node
                        self.status_manager.update_status(f"Visiting node {node.value}")
                    self.current_canvas.queue_draw()
                    return True
                else:
                    next(generator)
                    self.status_manager.update_status(
                        self.algorithm_manager.status_message
                    )
                    self.current_canvas.queue_draw()
                    return True
            except StopIteration:
                self.status_manager.update_status("Sorting complete!")
                return False

        GLib.timeout_add(int(10), step)
