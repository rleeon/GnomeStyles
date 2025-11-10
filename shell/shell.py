#!/usr/bin/env python3
import gi
gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gtk, Gdk
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from views import op1, op2, op3, op4, op5, op6


class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.gnomestyles.app")
        Adw.init()

    def do_activate(self):
        win = Adw.ApplicationWindow(application=self)
        win.set_default_size(900, 600)

        # --- Header principal ---
        self.header_bar = Adw.HeaderBar()
        self.page_title = Gtk.Label(label="Inicio")
        self.header_bar.pack_end(self.page_title)

        # --- Panel lateral ---
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        sidebar_box.set_hexpand(False)
        sidebar_box.set_vexpand(True)
        sidebar_box.set_size_request(200, -1)  # ≈ 20%

        title = Gtk.Label(label="Gnome Styles")
        title.add_css_class("title-1")
        title.set_margin_top(20)
        title.set_margin_bottom(20)
        sidebar_box.append(title)

        # Menú lateral
        sidebar = Gtk.ListBox()
        sidebar.set_selection_mode(Gtk.SelectionMode.SINGLE)
        sidebar.add_css_class("navigation-sidebar")
        sidebar.set_vexpand(True)

        opciones = ["Opción 1", "Opción 2", "Opción 3", "Opción 4", "Opción 5", "Opción 6"]
        for i, nombre in enumerate(opciones, 1):
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=nombre, xalign=0)
            label.set_margin_start(15)
            label.set_margin_top(8)
            label.set_margin_bottom(8)
            row.set_child(label)
            row.set_name(f"op{i}")
            sidebar.append(row)

        sidebar_box.append(sidebar)

        # --- Área de contenido ---
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_vexpand(True)
        self.stack.set_hexpand(True)

        # Añadir vistas externas
        self.stack.add_named(op1.View(), "op1")
        self.stack.add_named(op2.View(), "op2")
        self.stack.add_named(op3.View(), "op3")
        self.stack.add_named(op4.View(), "op4")
        self.stack.add_named(op5.View(), "op5")
        self.stack.add_named(op6.View(), "op6")

        # --- Layout principal ---
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        content.append(sidebar_box)
        content.append(self.stack)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(self.header_bar)
        main_box.append(content)

        # --- Estilos y señales ---
        sidebar.connect("row-selected", self.on_sidebar_select)

        # Tema claro/oscuro dinámico
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

        win.set_content(main_box)
        win.present()

    def on_sidebar_select(self, sidebar, row):
        if not row:
            return
        name = row.get_name()
        self.page_title.set_text(row.get_child().get_text())
        self.stack.set_visible_child_name(name)


if __name__ == "__main__":
    app = MyApp()
    app.run()
