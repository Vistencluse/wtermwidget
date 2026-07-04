# wtermwidget

Wtermwidget is a very barebones terminal emulator widget for wayland using gtk-layer-shell and python. 

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

# usage

```
wtermwidget -h | -(opt) (value) ... 

Options:
    -h      display this message
    -c      display custom command (default: tty-clock -c -C 3)
    -a      set background alpha (default: 0.5)
    -fg     set foreground RGBA color (default: \"1.0 0.72 0.15 1.0\") 
    -tw     set terminal width (default: 1920)
    -th     set terminal height (default: 1080)
    -tx     set terminal x alignment to left, center or end (default: center)
    -ty     set terminal y alignment to left, center or end (default: center)
    -mt     set terminal margin top (default: 20)
    -ml     set terminal margin left (default: 20)
    -mr     set terminal margin right (default: 20)
    -mb     set terminal margin bottom (default: 20)
```

# planned features

the plan was custom commands, position control and color control, all of which is done. I may fix some of the issues below but don't expect anything else. You're welcome to go through the script and modify it, it's quite straightforward.

# known issues

doesn't work with pipes.sh, cowsay and probably many more programs (unlikely to change)
the cursor shows up in apps that output pure text instead of opening screens (I will probably fix this soon)