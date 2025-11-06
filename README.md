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


