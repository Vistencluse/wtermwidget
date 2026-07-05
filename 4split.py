#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv(override=True)

import sys
import gi
import os

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
Usage: 4split -h | -(opt) (value) ...

Options:
    -h      display this message
    -c1     command for top left terminal (default: tty-clock -c -C 3)
    -c2     command for top right terminal (default: cava)
    -c3     command for bottom left terminal (default: cowsay test)
    -c4     command for bottom right terminal (default: pipes.sh)
    -a      set background alpha (default: 0.5)
    -fg     set foreground RGBA color (default: \"1.0 0.72 0.15 1.0\")
"""

CMD1 = "tty-clock -c -C 3"
CMD2 = "cava"
CMD3 = "cowsay test"
CMD4 = "pipes.sh"
BG_ALPHA = 0.5
TERM_ALPHA = 0.5
FG_COLOR = "1.0 0.72 0.15 1.0"
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

class WidgetWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_decorated(False)
        self.set_resizable(False)

        # transparency

        self.set_app_paintable(True)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()

        if visual and screen.is_composited():
            self.set_visual(visual)

        # init layer shell

        LayerShell.init_for_window(self)

        LayerShell.set_layer(self, LayerShell.Layer.BACKGROUND)

        # make host screen anchored to all sides (fullscreen)
        for edge in (
            LayerShell.Edge.LEFT,
            LayerShell.Edge.RIGHT,
            LayerShell.Edge.TOP,
            LayerShell.Edge.BOTTOM,
        ):
            LayerShell.set_anchor(self, edge, True)

        # bgpane background css
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(
            ("#bgpane { background-color: rgba(0, 0, 0, %.3f); }" % BG_ALPHA).encode()
        )
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # create background pane that fills whole screen
        overlay = Gtk.Overlay()
        self.add(overlay)

        bg = Gtk.Box()
        bg.set_name("bgpane")
        overlay.add(bg)

        # terminal widgets

        terms = [
            self.create_term_tl(),
            self.create_term_tr(),
            self.create_term_bl(),
            self.create_term_br()
        ]

        for term in terms:
            overlay.add_overlay(term)

        self.show_all()

    def create_term_tl(self):
        term = Vte.Terminal()

        term.set_size_request(950, 507)
        term.set_halign(Gtk.Align.START)
        term.set_valign(Gtk.Align.START)
        term.set_margin_top(0)
        term.set_margin_left(0)

        fgcolor = [float(num) for num in FG_COLOR.split()]
        term.set_colors(
            Gdk.RGBA(fgcolor[0], fgcolor[1], fgcolor[2], fgcolor[3]),  # foreground
            Gdk.RGBA(0, 0, 0, TERM_ALPHA),     # background
            palette
        )

        term.set_font(
            Pango.FontDescription("monospace 15")
        )

        term.set_cursor_shape(Vte.CursorShape.IBEAM)

        # launch terminal

        term.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            [Vte.get_user_shell() or "/bin/bash", "-c", CMD1],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None
        )

        return term

    def create_term_tr(self):
        term = Vte.Terminal()

        term.set_size_request(950, 507)
        term.set_halign(Gtk.Align.END)
        term.set_valign(Gtk.Align.START)
        term.set_margin_top(0)
        term.set_margin_right(0)

        fgcolor = [float(num) for num in FG_COLOR.split()]
        term.set_colors(
            Gdk.RGBA(fgcolor[0], fgcolor[1], fgcolor[2], fgcolor[3]),  # foreground
            Gdk.RGBA(0, 0, 0, TERM_ALPHA),     # background
            palette
        )

        term.set_font(
            Pango.FontDescription("monospace 15")
        )

        term.set_cursor_shape(Vte.CursorShape.IBEAM)

        # launch terminal

        term.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            [Vte.get_user_shell() or "/bin/bash", "-c", CMD2],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None
        )

        return term

    def create_term_bl(self):
        term = Vte.Terminal()

        term.set_size_request(950, 507)
        term.set_halign(Gtk.Align.START)
        term.set_valign(Gtk.Align.END)
        term.set_margin_bottom(0)
        term.set_margin_left(0)

        fgcolor = [float(num) for num in FG_COLOR.split()]
        term.set_colors(
            Gdk.RGBA(fgcolor[0], fgcolor[1], fgcolor[2], fgcolor[3]),  # foreground
            Gdk.RGBA(0, 0, 0, TERM_ALPHA),     # background
            palette
        )

        term.set_font(
            Pango.FontDescription("monospace 15")
        )

        term.set_cursor_shape(Vte.CursorShape.IBEAM)

        # launch terminal

        term.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            [Vte.get_user_shell() or "/bin/bash", "-c", CMD3],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None
        )

        return term

    def create_term_br(self):
        term = Vte.Terminal()

        term.set_size_request(950, 507)
        term.set_halign(Gtk.Align.END)
        term.set_valign(Gtk.Align.END)
        term.set_margin_bottom(0)
        term.set_margin_right(0)

        fgcolor = [float(num) for num in FG_COLOR.split()]
        term.set_colors(
            Gdk.RGBA(fgcolor[0], fgcolor[1], fgcolor[2], fgcolor[3]),  # foreground
            Gdk.RGBA(0, 0, 0, TERM_ALPHA),     # background
            palette
        )

        term.set_font(
            Pango.FontDescription("monospace 15")
        )

        term.set_cursor_shape(Vte.CursorShape.IBEAM)

        # launch terminal

        term.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            [Vte.get_user_shell() or "/bin/bash", "-c", CMD4],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None
        )

        return term

if len(sys.argv) > 1:
    args = sys.argv[1:]
    opts = [arg for arg in args if arg.startswith("-")]
    try:
        for opt in opts:
            idx = args.index(opt)

            match opt:
                case "-h":
                    print(HELP)
                    quit()
                case "-c1":
                    CMD1 = args[idx+1]
                case "-c2":
                    CMD2 = args[idx+1]
                case "-c3":
                    CMD3 = args[idx+1]
                case "-c4":
                    CMD4 = args[idx+1]
                case "-a":
                    BG_ALPHA = float(args[idx+1])
                    TERM_ALPHA = BG_ALPHA
                case "-fg":
                    FG_COLOR = args[idx+1]
                case _:
                    print(f"Unknown option: {1}", opt)
    except IndexError:
        print('option selected but no value given.')

win = WidgetWindow()
Gtk.main()