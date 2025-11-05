import Gtk from 'gi://Gtk';
import Gio from 'gi://Gio';

export function fillPreferencesWindow(window) {
    const settings = new Gio.Settings({ schema_id: 'org.gnome.shell.extensions.gnomestyles' });

    const box = new Gtk.Box({ orientation: Gtk.Orientation.VERTICAL, spacing: 10, margin_top: 20, margin_start: 20 });
    window.set_child(box);

    const label = new Gtk.Label({ label: 'Nombre del estilo:', halign: Gtk.Align.START });
    box.append(label);

    const entry = new Gtk.Entry({ text: settings.get_string('style-name') });
    entry.connect('changed', () => {
        settings.set_string('style-name', entry.text);
    });
    box.append(entry);
}
