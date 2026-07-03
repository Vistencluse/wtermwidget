#!/usr/bin/env python3

import os
import sys
import gi

GTK_LAYER_SHELL_DIR = os.path.expanduser(
    "~/gtk-layer-shell-0.10.1/build/src"
)

os.environ["GI_TYPELIB_PATH"] = GTK_LAYER_SHELL_DIR + ":" + \
    os.environ.get("GI_TYPELIB_PATH", "")

os.environ["LD_LIBRARY_PATH"] = GTK_LAYER_SHELL_DIR + ":" + \
    os.environ.get("LD_LIBRARY_PATH", "")


gi.require_version("Gtk", "3.0")
gi.require_version("Vte", "2.91")

try:
    gi.require_version("GtkLayerShell", "0.1")
except ValueError:
    raise RuntimeError(
        "\nCould not load GtkLayerShell typelib.\n"
        f"Expected build dir:\n{GTK_LAYER_SHELL_DIR}\n"
    )

from gi.repository import Gtk, Vte, GLib, Gdk, Pango
from gi.repository import GtkLayerShell as LayerShell

class ClockWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(1920, 1080)

        #
        # transparency
        #
        self.set_app_paintable(True)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()

        if visual and screen.is_composited():
            self.set_visual(visual)

        #
        # layer shell
        #
        LayerShell.init_for_window(self)

        LayerShell.set_layer(self, LayerShell.Layer.BACKGROUND)

        #
        # terminal widget
        #
        term = Vte.Terminal()

        self.add(term)

        term.set_size(500, 200)

        palette = [
            Gdk.RGBA(0,0,0,1),          # black
            Gdk.RGBA(0.8,0.2,0.2,1),    # red
            Gdk.RGBA(0.2,0.8,0.2,1),    # green
            Gdk.RGBA(1.0,0.72,0.15,1),  # yellow/orange
            Gdk.RGBA(0.3,0.5,1.0,1),    # blue
            Gdk.RGBA(0.8,0.3,0.8,1),    # magenta
            Gdk.RGBA(0.3,0.8,0.8,1),    # cyan
            Gdk.RGBA(0.9,0.9,0.9,1),    # white
        ]
        
        term.set_colors(
            Gdk.RGBA(1.0, 0.72, 0.15, 1.0),  # foreground
            Gdk.RGBA(0, 0, 0, 0.70),          # transparent background
            palette
        )

        term.set_font(
            Pango.FontDescription("monospace 15")
        )

        #
        # launch terminal
        #
        term.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            ["/usr/bin/tty-clock", "-c", "-C", "3"],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None
        )

        self.show_all()

win = ClockWindow()

Gtk.main()
