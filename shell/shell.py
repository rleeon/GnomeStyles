#!/usr/bin/env python3
import gi
import os
import sys

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gtk, Gio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from views import op1, op2, op3, op4, op5, op6
except Exception as e:
    print(f"Error importando vistas: {e}")
    sys.exit(1)


class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="io.gnomestyles.App")
        Adw.init()

    # El metodo principal que abre la ventana
    def do_activate(self):
        win = Adw.ApplicationWindow(application=self)
        win.set_default_size(900, 600)
        win.set_title("GnomeStyles")

        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if not os.path.exists(icon_path):
            icon_path = None

        main_header = self._build_main_header(icon_path)

        sidebar_box, sidebar = self._build_sidebar()

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_vexpand(True)
        self.stack.set_hexpand(True)

        self.stack.add_named(op1.View(), "op1")
        self.stack.add_named(op2.View(), "op2")
        self.stack.add_named(op3.View(), "op3")
        self.stack.add_named(op4.View(), "op4")
        self.stack.add_named(op5.View(), "op5")
        self.stack.add_named(op6.View(), "op6")

        content = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        content.set_start_child(sidebar_box)
        content.set_end_child(self.stack)
        content.set_resize_start_child(False)
        content.set_resize_end_child(True)
        content.set_shrink_start_child(False)
        content.set_shrink_end_child(False)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.append(main_header)
        main_box.append(content)

        sidebar.connect("row-selected", self.on_sidebar_select)

        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

        first_row = sidebar.get_row_at_index(0)
        if first_row:
            sidebar.select_row(first_row)

        win.set_content(main_box)
        win.present()

    # Construye la barra de titulo principal, osea el header
    def _build_main_header(self, icon_path):
        header = Adw.HeaderBar()
        header.add_css_class("titlebar")

        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        left_box.set_halign(Gtk.Align.START)
        left_box.set_hexpand(False)

        if icon_path:
            try:
                image = Gtk.Image.new_from_file(icon_path)
                image.set_pixel_size(44)
                left_box.append(image)
            except Exception:
                    pass

        app_label = Gtk.Label(label="GnomeStyles")
        app_label.add_css_class("title-1")

        left_box.append(app_label)
        left_box.set_size_request(240, -1)

        self.page_title = Gtk.Label(label="")
        self.page_title.add_css_class("title-2")
        self.page_title.set_hexpand(True)
        self.page_title.set_halign(Gtk.Align.CENTER)

        header.set_title_widget(self.page_title)
        header.pack_start(left_box)
        return header

    # Construye la barra lateral de navegacion, osea el sidebar
    def _build_sidebar(self):
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_size_request(240, -1)
        sidebar_box.set_hexpand(False)
        sidebar_box.set_vexpand(True)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(240)
        clamp.set_tightening_threshold(240)

        sidebar = Gtk.ListBox()
        sidebar.set_selection_mode(Gtk.SelectionMode.SINGLE)
        sidebar.add_css_class("navigation-sidebar")
        sidebar.set_vexpand(True)

        opciones = [
            "Opción 1", "Opción 2", "Opción 3",
            "Opción 4", "Opción 5", "Opción 6"
        ]

        for i, nombre in enumerate(opciones, 1):
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=nombre, xalign=0)
            label.set_margin_start(16)
            label.set_margin_top(10)
            label.set_margin_bottom(10)
            row.set_child(label)
            row.set_name(f"op{i}")
            sidebar.append(row)

        clamp.set_child(sidebar)
        sidebar_box.append(clamp)
        return sidebar_box, sidebar

    # Construye un header dividido en dos partes (izquierda y derecha)
    def _build_split_header(self, left_header, right_header):
        container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # izquierda fijo
        left_wrapper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        left_wrapper.set_hexpand(False)
        left_wrapper.append(left_header)

        # derecha expande y centra
        right_wrapper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        right_wrapper.set_hexpand(True)
        right_wrapper.append(right_header)

        container.append(left_wrapper)
        container.append(right_wrapper)

        return container

    # Manejador de seleccion en el sidebar
    def on_sidebar_select(self, sidebar, row):
        if not row:
            return
        name = row.get_name()
        title = row.get_child().get_text()
        self.page_title.set_text(title)
        self.stack.set_visible_child_name(name)


if __name__ == "__main__":
    app = MyApp()
    app.run()