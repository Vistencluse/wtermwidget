# wtermwidget

Wtermwidget is a very barebones terminal emulator widget for wayland using gtk-layer-shell and python. 

# instalation

just download the python script and run:

```
python3 wtermwidget.py
```

if you don't have gtk-layer-shell globally installed, grab its latest source code and point both GI_TYPELIB_PATH and LD_LIBRARY_PATH variables to it:

```
GI_TYPELIB_PATH=/your/path/build/src LD_LIBRARY_PATH=/your/path/build/src python3 wtermwidget.py 
```

# usage

use the -h option to show syntax and available options. Use the -c option plus a command to display this command on the terminal. If you run the script without providing a command, it defaults to "tty-clock -c -C 3". If your command takes arguments, don't forget to pass it in quotes:

```
python3 wtermwidget.py -c "tty-clock -c -C 3"
```

that's it for now.

# planned features

this script was always intended to be barebones, but positioning and color control is planned.

# known issues

doesn't work with pipes.sh unfortunately. Don't know why but I don't think I will attempt to fix it.