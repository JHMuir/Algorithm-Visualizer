from gi.repository import Gtk, GLib
from .algo_manager import AlgorithmManager
from .canvas import VisualizerCanvas, StatusManager


class AlgorithmVisualizer(Gtk.Window):
    """Main application class."""

    def __init__(self):
        super().__init__(title="Algorithm Visualizer")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        # Components
        self.algorithm_manager = AlgorithmManager()
        self.visualizer_canvas = VisualizerCanvas(self.algorithm_manager)
        self.status_manager = StatusManager()

        # Layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.main_box)

        # Toolbar
        self.toolbar = Gtk.Box(spacing=10)
        self.main_box.pack_start(self.toolbar, False, False, 0)

        # Algorithm selection
        self.algorithm_dropdown = Gtk.ComboBoxText()
        for algo in ["Bubble Sort", "Quick Sort", "Merge Sort", "Insertion Sort"]:
            self.algorithm_dropdown.append_text(algo)
        self.algorithm_dropdown.set_active(0)
        self.toolbar.pack_start(self.algorithm_dropdown, False, False, 0)

        # Buttons
        self.start_button = Gtk.Button(label="Start Sorting")
        self.start_button.connect("clicked", self.start_sorting)
        self.toolbar.pack_start(self.start_button, False, False, 0)

        self.reset_button = Gtk.Button(label="Reset Data")
        self.reset_button.connect("clicked", self.reset_data)
        self.toolbar.pack_start(self.reset_button, False, False, 0)

        # Canvas and Status
        self.main_box.pack_start(self.visualizer_canvas, True, True, 0)
        self.main_box.pack_start(self.status_manager, False, False, 0)

        # Initialize data
        self.reset_data()

    def reset_data(self, widget=None):
        """Reset the dataset."""
        self.algorithm_manager.reset_data()
        self.status_manager.update_status(
            "Data reset. Select an algorithm and press Start."
        )
        self.visualizer_canvas.queue_draw()

    def start_sorting(self, widget):
        """Start the sorting animation."""
        if self.algorithm_manager.get_generator(
            self.algorithm_dropdown.get_active_text()
        ):
            self.algorithm_manager.highlight_indices = (-1, -1)
            generator = self.algorithm_manager.get_generator(
                self.algorithm_dropdown.get_active_text()
            )
            self.animate_sorting(generator)

    def animate_sorting(self, generator):
        """Animate the sorting process."""

        def step():
            try:
                next(generator)
                self.status_manager.update_status(self.algorithm_manager.status_message)
                self.visualizer_canvas.queue_draw()
                return True
            except StopIteration:
                self.status_manager.update_status("Sorting complete!")
                return False

        GLib.timeout_add(int(10), step)
