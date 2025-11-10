from gi.repository import Gtk

class View(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        label = Gtk.Label(label="Contenido de Opción 6")
        label.set_margin_top(20)
        self.append(label)
