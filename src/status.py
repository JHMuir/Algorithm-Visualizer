from gi.repository import Gtk


class StatusManager(Gtk.Label):
    """Manages the status bar messages."""

    def __init__(self):
        super().__init__()
        self.set_text("Select an algorithm and press Start.")

    def update_status(self, message):
        self.set_text(message)
