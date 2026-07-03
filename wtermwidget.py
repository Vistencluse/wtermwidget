#!/usr/bin/env python3

import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version("Vte", "2.91")

try:
    gi.require_version('GtkLayerShell', '0.1')
except ValueError:
    import sys
    raise RuntimeError('\n\n' +
        'If you haven\'t installed GTK Layer Shell, you need to point Python to the\n' +
        'library by setting GI_TYPELIB_PATH and LD_LIBRARY_PATH to <build-dir>/src/.\n' +
        'For example you might need to run:\n\n' +
        'GI_TYPELIB_PATH=build/src LD_LIBRARY_PATH=build/src python3 ' + ' '.join(sys.argv))

from gi.repository import Gtk, Vte, GLib, Gdk, Pango
from gi.repository import GtkLayerShell as LayerShell

HELP = """
Usage: wtermwidget -h | -c (COMMAND)

Options:
    -h      display this message
    -c      display custom command (default: tty-clock -c -C 3)
"""

CMD = ["tty-clock", "-c", "-C", "3"]

class WidgetWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(1920, 1080)


        # transparency

        self.set_app_paintable(True)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()

        if visual and screen.is_composited():
            self.set_visual(visual)

        # init layer shell

        LayerShell.init_for_window(self)

        LayerShell.set_layer(self, LayerShell.Layer.BACKGROUND)

        # terminal widget

        term = Vte.Terminal()

        self.add(term)

        term.set_size(500, 200)

        palette = [
            Gdk.RGBA(0,0,0,1),          # 0: black
            Gdk.RGBA(0.8,0.2,0.2,1),    # 1: red
            Gdk.RGBA(0.2,0.8,0.2,1),    # 2: green
            Gdk.RGBA(1.0,0.72,0.15,1),  # 3: yellow/orange
            Gdk.RGBA(0.3,0.5,1.0,1),    # 4: blue
            Gdk.RGBA(0.8,0.3,0.8,1),    # 5: magenta
            Gdk.RGBA(0.3,0.8,0.8,1),    # 6: cyan
            Gdk.RGBA(0.9,0.9,0.9,1),    # 7: white
        ]
        
        term.set_colors(
            Gdk.RGBA(1.0, 0.72, 0.15, 1.0),  # foreground
            Gdk.RGBA(0, 0, 0, 0.70),         # background
            palette
        )

        term.set_font(
            Pango.FontDescription("monospace 15")
        )

        # launch terminal

        term.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            CMD,
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None
        )

        self.show_all()

if len(sys.argv) > 1:
    args = sys.argv[1:]
    for arg in args:
        if arg == "-h":
            print(HELP)
            quit()
        if arg == "-c":
            try:
                idx = args.index(arg)
                CMD = args[idx+1].split()
            except IndexError:
                print('"-c" option selected but no command given.')

win = WidgetWindow()
Gtk.main()