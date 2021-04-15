# selector

This is a simple GTK selector with filters similar to dmenu (https://wiki.archlinux.org/index.php/dmenu).

I needed a replacement for dmenu on Gnome and decided to go for a solution having the Gnome look and feel. This is a simple script that launches a UI for selecting a single entry from a list of options, also providing a simple text filter.

# Usage

```bash
echo -e "Option 1\nOption 2\nOption 3" | ./selector.py
```

- Pressing ENTER (or the OK button) prints the selected entry to STDOUT (or the first shown entry if nothing is selected).
- Pressing QUIT causes the dialog to vanish without printing anything.
