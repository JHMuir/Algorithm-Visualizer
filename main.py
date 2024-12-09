from src.visualizer import AlgorithmVisualizer
from gi.repository import Gtk

if __name__ == "__main__":
    app = AlgorithmVisualizer()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()