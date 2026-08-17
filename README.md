# D2R Companion

A dark-themed companion app for **Diablo 2: Resurrected** that reads your
rune stash straight from the screen and shows you exactly which runewords you
can craft right now — runes in the correct order, sockets, eligible item
types, and full effect descriptions. Plus the runewords you're **one rune
short** of, the complete runeword list by level, and all Horadric cube
recipes.

![D2R Companion — my runes view](d2screenshot.png)

## Features

- **My runes** — the default tab. After a scan it shows your runes, then
  every runeword you can craft (with its full effect list), then the ones
  missing a single rune (missing rune highlighted in red).
- **All runewords** — the complete list (100 runewords incl. 2.4/2.6/3.0
  additions) sorted by required level.
- **Cube recipes** — 159 Horadric cube recipes grouped by category
  (Socketing, Crafting, Rune/Gem upgrading, Item upgrading, Repair &
  recharge, Rerolling, Quest & special).
- **Live search** — filters the active tab as you type; partial words match
  names, runes, item types, effect text and recipe ingredients.
- **Global hotkey** — press a key once and it's your scan key forever
  (remembered across runs). Press it in-game to re-scan instantly.
- **CLI** — the same scanning engine without the GUI.

## Quick start (GUI)

```bash
python3 d2rc.py
```

1. On first run, click **Assign hotkey** and press the key you want to use
   for scanning (ESC, Enter, Tab, Space, Delete and modifier keys are
   refused so you don't steal important in-game buttons).
2. Open Diablo 2: Resurrected, open your stash on the **RUNES** tab.
3. Press your hotkey — the app screenshots the screen and lists what you
   can craft.

Pre-load a screenshot instead of scanning (useful for testing):

```bash
python3 d2rc.py --image screenshot.png
```

## CLI

```bash
python3 d2r_runewords.py --capture     # scan the screen right now
python3 d2r_runewords.py --image x.png # analyze an existing screenshot
python3 d2r_runewords.py --listen      # daemon: hotkey = capture + analyze
python3 d2r_runewords.py --list        # dump the runeword database
python3 d2r_runewords.py --image x.png --all   # also show "one rune short"
```

The `--listen` daemon uses the hotkey from the config file (set it via the
GUI, or add `"hotkey": "F8"` to `~/.config/d2r_runewords/config.json`).

## How it works

The D2R **RUNES** stash tab renders all 33 runes in a fixed 9×4 grid. Runes
you own show as light stone slabs with a white count digit; runes you don't
own show as dark placeholder silhouettes. The tool screenshots the screen
(ImageMagick `import`) and checks the brightness of each of the 33 slots —
bright slot = rune present. Stack sizes are read from the count digit via
embedded templates (best effort; presence detection is the reliable part).

## Files

```
d2rc.py            GUI (main entry — python3 d2rc.py)
d2r_runewords.py   CLI + scanning core + hotkey grab
d2r_data.py        runeword + cube recipe database (single source of truth)
d2screenshot.png   calibration / demo screenshot
```

## Requirements

- X11 session (Xfce etc.), Python 3, Pillow, numpy, scipy, python-xlib
- ImageMagick's `import` (screen capture) and `notify-send` (CLI
  notifications)
- The game should run fullscreen (or borderless) on one monitor at the
  resolution used for calibration (1920×1080) — the layout auto-scales, and
  windowed/multi-monitor setups can be tuned via
  `~/.config/d2r_runewords/config.json` (`offset_x`/`offset_y`).
- Exclusive-fullscreen games sometimes render to an overlay X11 cannot
  capture (black image) — switch D2R to Windowed / Borderless Windowed.

## Data source

Runeword + recipe data parsed from [diablo2.io](https://diablo2.io)
(D2R v3.2 / Reign of the Warlock, incl. Authority, Coven, Void, Vigilance,
Ritual, Hysteria, Mania). Slot layout and thresholds were calibrated from
`d2screenshot.png`.

## License

[MIT](LICENSE)
