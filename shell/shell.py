#!/usr/bin/env python3
import gi
import os
import sys

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gtk, Gio, GLib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa todas las ventanas, de momento importa muchas aunque no se usen.
try:
    from views import op1, op2, op3, op4, op5, op6
except Exception as e:
    print(f"Error importando vistas: {e}")
    sys.exit(1)


class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="io.gnomestyles.App")

    # El metodo principal que abre la ventana
    def do_activate(self):
        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_default_size(900, 600)
        self.win.set_title("GnomeStyles")

        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if not os.path.exists(icon_path):
            icon_path = None

        sidebar_box, sidebar = self._build_sidebar()

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_vexpand(True)
        self.stack.set_hexpand(True)

        for config in self.views_config:
            view = config['view_module'].View()
            self.stack.add_named(view, config['id'])

        self.content = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.content.set_start_child(sidebar_box)
        self.content.set_end_child(self.stack)
        self.content.set_resize_start_child(False)
        self.content.set_resize_end_child(True)
        self.content.set_shrink_start_child(True)
        self.content.set_shrink_end_child(False)
        self.content.set_position(240)

        self.toggle_button = Gtk.Button()
        self.toggle_button.set_icon_name("go-next-symbolic")  # Flechita para mostrar sidebar
        self.toggle_button.add_css_class("circular")
        self.toggle_button.set_size_request(32, 32)
        self.toggle_button.connect("clicked", self.on_toggle_left)
        self.toggle_button.set_visible(False)

        self.main_header = self._build_main_header(icon_path, self.toggle_button)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.append(self.main_header)
        main_box.append(self.content)

        sidebar.connect("row-selected", self.on_sidebar_select)

        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

        self.left_visible = True
        self.min_window_width = 480
        self.grace_period_end = 0  # Para evitar colapso inmediato después de expandir manualmente

        first_row = sidebar.get_row_at_index(0)
        if first_row:
            sidebar.select_row(first_row)
            self.on_sidebar_select(sidebar, first_row)

        # Tiempo para chequear tamaño de ventana cada 100ms, modificar al gusto, lo de hacer pequeña la parte izquierda falla un huevo.
        self.check_size_id = GLib.timeout_add(100, self.check_window_size)

        self.win.set_content(main_box)
        self.win.present()

    # AÑADIR VENTANAAAAS
    views_config = [
        {'name': 'PACKS', 'id': 'op1', 'view_module': op1},  # CAMBIAR NAME E ID SEGUN VENTANA
        # Copia y pega para añadir otra ventana, pero modificalo, porque sino solo la duplicas.



        # view_module es el nombre de el import osea de el archivo.py de la ventana.
        # Ejemplo para añadir: {'name': 'Nueva Opción', 'id': 'op7', 'view_module': op7},
    ]

    def check_window_size(self):
        current_time = GLib.get_monotonic_time()
        width = self.win.get_width()
        if width < self.min_window_width and self.left_visible and current_time > self.grace_period_end:
            self.collapse_left()
        elif width >= self.min_window_width and not self.left_visible:
            self.expand_left()
        return True

    def collapse_left(self):
        # Ocultar sidebar con set_position(0)
        self.content.set_position(0)
        self.left_box.set_visible(False)

        # Mostrar flechita en header derecho
        self.toggle_button.set_visible(True)
        self.toggle_button.set_icon_name("go-next-symbolic")

        self.left_visible = False

    def expand_left(self):
        self.content.set_position(240)

        self.left_box.set_visible(True)

        # Ocultar flechita
        self.toggle_button.set_visible(False)

        # Establecer período de gracia para evitar colapso inmediato (3 segundos)
        self.grace_period_end = GLib.get_monotonic_time() + 3000000  # Son microsegundos, osea se divide entre 1.000.000, asi que aqui son 3s, o el primer numero son los segundos.

        self.left_visible = True

    def on_toggle_left(self, button):
        if self.left_visible:
            self.collapse_left()
        else:
            self.expand_left()

    # Construye la barra de titulo principal, osea el header
    def _build_main_header(self, icon_path, toggle_button):
        header_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # IZQUIERDA: Box simple (sin controles de ventana, ancho fijo 240px)
        self.left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.left_box.set_halign(Gtk.Align.START)
        self.left_box.set_hexpand(False)
        self.left_box.set_size_request(240, -1)  # Ancho fijo para izquierda

        if icon_path:
            try:
                self.icon_image = Gtk.Image.new_from_file(icon_path)
                self.icon_image.set_pixel_size(44)
                self.left_box.append(self.icon_image)
            except Exception:
                self.icon_image = Gtk.Image.new_from_icon_name("application-x-executable")
                self.icon_image.set_pixel_size(44)
                self.left_box.append(self.icon_image)

        self.app_label = Gtk.Label(label="GnomeStyles")
        self.app_label.add_css_class("title-1")
        self.left_box.append(self.app_label)

        header_container.append(self.left_box)

        # DERECHA: HeaderBar oficial (con controles de ventana, título centrado en su área)
        right_header = Adw.HeaderBar()
        right_header.add_css_class("titlebar")
        right_header.set_hexpand(True)

        right_header.pack_start(toggle_button)

        self.page_title = Gtk.Label(label="")
        self.page_title.add_css_class("title-2")
        self.page_title.set_hexpand(True)
        self.page_title.set_halign(Gtk.Align.CENTER)

        right_header.set_title_widget(self.page_title)
        header_container.append(right_header)

        return header_container

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

        for config in self.views_config:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=config['name'], xalign=0)
            label.set_margin_start(16)
            label.set_margin_top(10)
            label.set_margin_bottom(10)
            row.set_child(label)
            row.set_name(config['id'])
            sidebar.append(row)

        clamp.set_child(sidebar)
        sidebar_box.append(clamp)
        return sidebar_box, sidebar

    def on_sidebar_select(self, sidebar, row):
        if not row:
            return
        name = row.get_name()
        title = row.get_child().get_text()
        self.page_title.set_text(title)
        self.stack.set_visible_child_name(name)
        if self.win.get_width() < self.min_window_width and GLib.get_monotonic_time() > self.grace_period_end:
            self.collapse_left()


if __name__ == "__main__":
    app = MyApp()
    app.run()