# Descripción/Ideas

La idea es que la extensión no sea más que una especie de biblioteca en la que hay múltiples estilos visuales, como un pack que trae cosas como temas de grub, terminal, otras extensiones como "Dash to Dock" o "Desktop Cube" si es posible.

Todo esto dentro de la propia configuración de la extensión dentro de la app de extensiones.

Dentro de configuración la idea es que te encuentres con varias ventanas una de ellas con packs que traigan todo en uno sin tener que leer mucho, y otras ventanas donde ya puedes modificar todo más manualmente.

Además me gustaría explorar el poder colocar gif o parecido para poder mostrar el como se ve, o una imagen, esto dentro de el apartado de configuración de la propia app de extensiones.


# GnomeStyles

4/11/25
/home/rleon/.local/share/gnome-shell/extensions

Direccion de las ext, para quein lo lea, esto es solo para mi, para recordar etc.


5/11/25
╭─ ~/.lo/sh/gnome-shell/extensions/gnomestyles@rleeon.github ── ✔  12:16:06 ─╮

╰─ tree                                                                      ─╯

.

├── extension.js         Esto es como el corazon de la extension, donde ocurren las cosas que yo quiero, osea como si yo quiero un icono nuevo pues aqui lo hago.

├── metadata.json      Describe la extension

├── prefs.js        Esto define la ventana de configuración que se abre al pulsar “Configuración” en la app de extensiones.

├── schemas        Esto es lo que hay dentro de esa configuracion, casi que lo mas importante.

│   ├── gschemas.compiled          Esto es lo mismo que abajo pero copilado, osea no lo tengo que tocar creo, simplemente se genera solo.

│   └── org.gnome.shell.extensions.gnomestyles.gschema.xml      Son las cosas que puede modificar el usuario como botones, definido con "keys" creo.

└── stylesheet.css        CSS para definir como se ve la extension

6/11/25

Con fallos a la hora de darle al botón de Configuración dentro de la app de extensiones, se debe a algo que no cuadra con la versión de la gnome-shell, tendré que mirar info o videos.


