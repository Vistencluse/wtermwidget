# wtermwidget

Wtermwidget is a very barebones terminal emulator widget for wayland using gtk-layer-shell and python.
Tested on COSMIC DE with cava, tty-clock, btop, pipes.sh and cowsay.

# screenshots

![tty-clock -c -C 3](/img/tty-clock.png)

![neofetch](/img/neofetch.png)

# instalation

just download the python script and run:

```
python3 wtermwidget.py
```

if you don't have gtk-layer-shell globally installed, grab its latest source code and point both GI_TYPELIB_PATH and LD_LIBRARY_PATH variables to it:

```
GI_TYPELIB_PATH=/your/path/build/src LD_LIBRARY_PATH=/your/path/build/src python3 wtermwidget.py 
```

or create a .env file in the same directory as the script with the contents below:

```
GI_TYPELIB_PATH=/your/path/build/src
LD_LIBRARY_PATH=/your/path/build/src 
```

and then run the script.

# usage

```
wtermwidget -h | -(opt) (value) ...

Options:
    -h      display this message
    -c      display custom command (default: tty-clock -c -C 3)
    -a      set background alpha (default: 0.5)
    -fg     set foreground RGBA color (default: \"1.0 0.72 0.15 1.0\")
    -tw     set terminal width (default: 1900)
    -th     set terminal height (default: 1015)
    -tx     set terminal x alignment to left, center or end (default: center)
    -ty     set terminal y alignment to left, center or end (default: center)
    -mt     set terminal margin top (default: 20)
    -ml     set terminal margin left (default: 20)
    -mr     set terminal margin right (default: 20)
    -mb     set terminal margin bottom (default: 20)
    -ts     enable high bg contrast for placement testing
```

# planned features

none. You're welcome to go through the script and modify it, it's quite straightforward.
