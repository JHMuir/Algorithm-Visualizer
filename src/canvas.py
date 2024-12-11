from gi.repository import Gtk, cairo
import math


class SortingCanvas(Gtk.DrawingArea):
    """Draws the canvas"""

    def __init__(self, algorithm_manager):
        super().__init__()
        self.algorithm_manager = algorithm_manager
        self.connect("draw", self.on_draw)

    def on_draw(self, widget, cr):
        """Draws the dataset."""
        data = self.algorithm_manager.data
        width = self.get_allocated_width()
        height = self.get_allocated_height()
        bar_width = width / len(data)
        max_value = max(data)

        for i, value in enumerate(data):
            bar_height = (value / max_value) * height
            x = i * bar_width
            y = height - bar_height

            # Highlighting
            if i in self.algorithm_manager.highlight_indices:
                cr.set_source_rgb(0.8, 0.2, 0.2)  # Red for highlights
            else:
                cr.set_source_rgb(0.2, 0.4, 0.8)  # Blue for normal bars

            cr.rectangle(x, y, bar_width - 2, bar_height)
            cr.fill()


class TreeCanvas(Gtk.DrawingArea):
    def __init__(self, algorithm_manager):
        super().__init__()
        self.algorithm_manager = algorithm_manager
        self.current_highlighted = None
        self.connect("draw", self.on_draw)
        self.node_positions = {}

    def calculate_positions(self, node, x, y, level, width):
        if not node:
            return
        self.node_positions[node] = (x, y)

        next_level = level + 1
        spacing = width / (2**next_level)

        if node.left:
            self.calculate_positions(node.left, x - spacing, y + 80, next_level, width)
        if node.right:
            self.calculate_positions(node.right, x + spacing, y + 80, next_level, width)

    def on_draw(self, widget, cr):
        """Draws the binary tree"""
        width = self.get_allocated_width()
        # height = self.get_allocated_height()

        # Calculate positions if we have a tree
        if hasattr(self.algorithm_manager, "tree_algorithms"):
            tree = self.algorithm_manager.tree_algorithms.tree
            if tree:
                self.calculate_positions(tree, width / 2, 50, 1, width / 2)

        # Draw edges first
        cr.set_line_width(2)
        for node, (x, y) in self.node_positions.items():
            if node.left and node.left in self.node_positions:
                child_x, child_y = self.node_positions[node.left]
                cr.move_to(x, y)
                cr.line_to(child_x, child_y)
                cr.stroke()

            if node.right and node.right in self.node_positions:
                child_x, child_y = self.node_positions[node.right]
                cr.move_to(x, y)
                cr.line_to(child_x, child_y)
                cr.stroke()

        # Draw nodes
        for node, (x, y) in self.node_positions.items():
            # Highlight current node
            if node == self.current_highlighted:
                cr.set_source_rgb(0.8, 0.2, 0.2)  # Red for highlighted node
            else:
                cr.set_source_rgb(0.2, 0.4, 0.8)  # Blue for normal nodes

            # Draw node circle
            cr.arc(x, y, 20, 0, 2 * math.pi)
            cr.fill()

            # Draw node value
            cr.set_source_rgb(1, 1, 1)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(14)

            # Center the text
            text = str(node.value)
            text_extents = cr.text_extents(text)
            cr.move_to(x - text_extents.width / 2, y + text_extents.height / 2)
            cr.show_text(text)
