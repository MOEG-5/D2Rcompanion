#!/usr/bin/env python3
"""
D2R Rune Stash → Runeword checker
==================================
Press your assigned hotkey (or run --capture) while your Diablo 2:
Resurrected stash is open on the RUNES tab, and this tool reads which runes
you own and lists the runewords you can craft (rune order + eligible item
types).

How it works
------------
The D2R runes tab renders the 33 runes in a fixed five-row layout.  Runes you own
are rendered as light stone slabs (with a white count digit), runes you do
not own are dark placeholder silhouettes.  The tool screenshots the screen
and samples each of the 33 slots; bright slots = rune present.

Usage
-----
  python3 d2r_runewords.py --capture     # capture screen + analyze (run once)
  python3 d2r_runewords.py --image FILE  # analyze an existing screenshot
  python3 d2r_runewords.py --listen      # stay running; hotkey = capture + analyze
  python3 d2r_runewords.py --calibrate   # print per-slot stats to verify layout
  python3 d2r_runewords.py --list        # dump the built-in runeword database

The hotkey comes from the config file (~/.config/d2r_runewords/config.json,
"hotkey" key, default F8).  Modifier combinations such as Ctrl+J and
Ctrl+Shift+F8 are supported. The GUI (d2rc.py) lets you assign one visually.

Setup / requirements
--------------------
  * Linux (X11): python3, PIL, numpy, python-xlib.  Screen capture uses PIL
    ImageGrab (self-contained); ImageMagick's `import` is only an optional
    fallback and `notify-send` is optional (notifications degrade to
    printing).  Windows: plain Python + PIL + numpy — capture uses PIL
    ImageGrab and the global hotkey uses RegisterHotKey (ctypes), so no
    extra packages are needed.
  * Play Diablo 2: Resurrected in fullscreen (or borderless windowed) at the
    same resolution as the screenshot used to calibrate (1920x1080 by
    default) — the layout scales automatically with the screen size, but the
    game window must fill the screen (or use the offsets in the config file).
  * The stash window must be open with the RUNES tab selected when you hit the
    configured hotkey (F8 by default).

Layout / thresholds live in ~/.config/d2r_runewords/config.json
(created automatically).  Tweak there if your setup differs.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

import numpy as np
from PIL import Image

# --------------------------------------------------------------------------
# Runeword database (name, runes in order, sockets, item types, req level, patch)
# Source: diablo2.io runewords list (D2R, incl. ladder + 2.4/2.6/3.x additions)
# --------------------------------------------------------------------------
# Runeword database (name, runes in order, sockets, item types, req level, patch, mods)
# Single source of truth: d2r_data.py (parsed from diablo2.io, D2R v3.2 / RotW).
try:
    from d2r_data import RUNEWORDS as RW, RUNES
except ImportError:
    sys.exit("d2r_data.py not found next to d2r_runewords.py")

# --------------------------------------------------------------------------
# Layout (calibrated on a 1920x1080 fullscreen screenshot).
# Cell (r, c) is a 46x45 px square at origin + (c*spacing, r*spacing).
# The first three rows are full; the last two wrap around the stash panel.
# --------------------------------------------------------------------------
DEFAULT_CFG = {
    "baseline_w": 1920,
    "baseline_h": 1080,
    "origin_x": 177,
    "origin_y": 240,
    "spacing": 52,
    "cell_w": 46,
    "cell_h": 45,
    "cols": 9,
    "rows": 5,
    "offset_x": 0,   # extra manual offset (multi-monitor / windowed play)
    "offset_y": 0,
    "bright_threshold": 120,     # pixel brightness considered "bright"
    "digit_threshold": 180,       # brighter threshold to isolate the count digit
    "min_present_delta": 12,     # min gap between present/absent cluster means
    "digit_accept": 0.80,        # min IoU to accept a detected count digit
    "result_file": os.path.expanduser("~/d2r_runewords_result.txt"),
    "hotkey": "",                # global scan hotkey (assigned via the GUI)
}

SLOT_COORDS = (
    [(r, c) for r in range(3) for c in range(9)]
    + [(3, c) for c in (0, 1, 7, 8)]
    + [(4, c) for c in (0, 8)]
)

# Quantity digit reference grids (14x10), learned from the calibration screenshots.
# '#' = digit stroke. Weak matches still fall back to 1.
DIGIT_TEMPLATES = {
    0: "....##....|..##..##..|.#.....##.|..........|.#....#..#|#....#...#|..........|#...#....#|#..#.....#|..........|.##.....#.|.##....##.|..........|...####...",
    1: "#........#|#.........|#.........|..........|#.........|#.........|..........|#.........|#.........|..........|#.........|#.........|..........|#........#",
    2: "...#.#....|.#.....#..|#........#|..........|#........#|.........#|..........|.......#..|.....#....|..........|...#......|.#........|..........|##.#.#.#.#",
    3: ".#.#.#.#.#|.......#..|.......#..|..........|.....#....|...#.#.#..|..........|.......#.#|.........#|..........|.........#|##.......#|..........|.#.#.#.#..",
    4: ".......#..|......##..|..........|....#.##..|....#..#..|..........|...#...#..|..........|.#....##..|##.##.##.#|..........|.......#..|..........|.......#..",
    5: ".#.#.#.#..|.#........|.#........|..........|.#........|.#.#.#.#..|..........|.......#.#|.........#|..........|.........#|##.....#.#|..........|.#.#.#.#..",
    6: ".....#.#..|.....#....|...#......|..........|...#......|.#.#.#....|..........|.#.....#..|#........#|..........|#........#|##.......#|..........|.#.#.#.#..",
    7: "##.#.#.#.#|.........#|.........#|..........|.......#..|.......#..|..........|.....#....|.....#....|..........|.....#....|...#......|..........|...#......",
    8: "...#.#.#..|.#.....#..|.#........|..........|.#.#.#.#..|.#.#.#.#..|..........|.#.......#|#........#|..........|#........#|.#.......#|..........|.#.#.#.#..",
    9: "...#.#....|.#.....#..|#........#|..........|#........#|.#.....#.#|..........|...#.#.#..|.....#....|..........|.....#....|...#......|..........|...#......",
}


def load_config():
    path = os.path.expanduser("~/.config/d2r_runewords/config.json")
    cfg = dict(DEFAULT_CFG)
    try:
        with open(path) as f:
            cfg.update(json.load(f))
    except FileNotFoundError:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(cfg, f, indent=2)
    return cfg


def save_config(cfg):
    path = os.path.expanduser("~/.config/d2r_runewords/config.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)


def parse_digit_templates():
    out = {}
    for k, rows in DIGIT_TEMPLATES.items():
        g = np.array([[1.0 if ch == "#" else 0.0 for ch in row]
                      for row in rows.split("|")])
        out[k] = g
    return out


# --------------------------------------------------------------------------
# Screen capture
# --------------------------------------------------------------------------
def capture_screen(cfg):
    """Grab the screen — PIL ImageGrab on Windows and X11.

    Self-contained (no external tools needed).  Falls back to ImageMagick's
    `import` on X11 setups where Pillow lacks XCB support (source installs).
    """
    out = tempfile.mktemp(suffix=".png", prefix="d2r_cap_")
    try:
        from PIL import ImageGrab
        if sys.platform.startswith("win"):
            ImageGrab.grab().save(out)
        else:
            ImageGrab.grab(xdisplay=os.environ.get("DISPLAY", ":0.0")).save(out)
        return out
    except Exception as e:
        if sys.platform.startswith("win"):
            raise RuntimeError("screen capture failed: " + str(e)) from e
    r = subprocess.run(["import", "-window", "root", out],
                       capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        raise RuntimeError("screen capture failed: " + (r.stderr or "?"))
    return out


# --------------------------------------------------------------------------
# Slot analysis
# --------------------------------------------------------------------------
def cell_stats(gray, cfg, scale, r, c):
    ox = (cfg["origin_x"] + cfg["offset_x"]) * scale[0]
    oy = (cfg["origin_y"] + cfg["offset_y"]) * scale[1]
    sp = cfg["spacing"] * scale[0]
    cw = cfg["cell_w"] * scale[0]
    ch = cfg["cell_h"] * scale[1]
    x0 = int(round(ox + c * sp))
    y0 = int(round(oy + r * sp * (scale[1] / scale[0])))
    x1 = int(round(x0 + cw))
    y1 = int(round(y0 + ch))
    # interior = cell minus a ~6px margin so the border/bevel doesn't count
    m = int(6 * scale[0])
    interior = gray[y0 + m:y1 - m, x0 + m:x1 - m]
    if interior.size == 0:
        return None
    mean = float(interior.mean())
    bright = float((interior > cfg["bright_threshold"]).mean())
    return dict(x0=x0, y0=y0, x1=x1, y1=y1, mean=mean, bright=bright)


def otsu(values):
    """Split values into two clusters; return threshold and cluster means."""
    vals = np.asarray(sorted(values), dtype=float)
    if len(vals) < 2:
        return None, None, None
    if vals.max() - vals.min() < 1e-6:
        return None, vals.mean(), vals.mean()
    hist, edges = np.histogram(vals, bins=64)
    centers = (edges[:-1] + edges[1:]) / 2
    total = hist.sum()
    w0 = np.cumsum(hist).astype(float) / total
    w1 = 1.0 - w0
    m0 = np.cumsum(hist * centers) / np.maximum(np.cumsum(hist), 1)
    m1 = (np.cumsum(hist * centers)[-1] - np.cumsum(hist * centers)) / \
         np.maximum(total - np.cumsum(hist), 1)
    bc = w0 * w1 * (m0 - m1) ** 2
    bc[-1] = 0
    k = int(np.argmax(bc))
    th = float(edges[k])
    lo_vals = vals[vals < th]
    hi_vals = vals[vals >= th]
    lo_mean = lo_vals.mean() if len(lo_vals) else None
    hi_mean = hi_vals.mean() if len(hi_vals) else None
    return th, lo_mean, hi_mean


def read_digit_count(gray, cfg, scale, stats, templates):
    """Best-effort stack count from one or two white digits in the slot."""
    x0, y0 = stats["x0"], stats["y0"]
    sx, sy = scale
    # Include enough of the bottom-right corner for two-digit stack counts.
    r0 = int(round(y0 + 30 * sy))
    r1 = int(round(y0 + 44 * sy))
    c0 = int(round(x0 + 25 * sx))
    c1 = int(round(x0 + 46 * sx))
    reg = gray[r0:r1, c0:c1]
    if reg.size == 0:
        return 1
    binary = reg > max(cfg["digit_threshold"], 180)

    # Each digit is a run of occupied columns; the gap between digits stays
    # empty even though some glyphs consist of disconnected strokes.
    runs = []
    for x in np.flatnonzero(binary.any(axis=0)):
        if not runs or x > runs[-1][-1] + 1:
            runs.append([x])
        else:
            runs[-1].append(x)

    digits = []
    for run in runs:
        glyph = binary[:, run[0]:run[-1] + 1]
        ys, xs = np.where(glyph)
        if (len(xs) < max(4, 8 * sx * sy)
                or ys.max() - ys.min() < max(4, 8 * sy)):
            continue
        canvas = np.zeros((14, 10), dtype=float)
        ry = ((ys - ys.min()) / max(ys.max() - ys.min(), 1) * 13).astype(int)
        rx = ((xs - xs.min()) / max(xs.max() - xs.min(), 1) * 9).astype(int)
        canvas[ry, rx] = 1
        scores = {}
        for k, template in templates.items():
            inter = (canvas * template).sum()
            scores[k] = inter / max(canvas.sum() + template.sum() - inter, 1)
        digit = max(scores, key=scores.get)
        if scores[digit] >= cfg["digit_accept"]:
            digits.append(digit)

    return int("".join(map(str, digits[-2:]))) if digits else 1


def analyze_image(path, cfg, verbose=False):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    gray = np.array(img).mean(axis=2)
    scale = (w / cfg["baseline_w"], h / cfg["baseline_h"])

    n_runes = len(RUNES)
    stats = []
    for idx, (r, c) in enumerate(SLOT_COORDS[:n_runes]):
        st = cell_stats(gray, cfg, scale, r, c)
        if st is None:
            continue
        st["rune"] = RUNES[idx]
        st["idx"] = idx
        stats.append(st)

    means = [s["mean"] for s in stats]
    th, lo_mean, hi_mean = otsu(means)

    # A slot is "present" when a decent fraction of its interior pixels are
    # bright (light rune slab) vs. the dark placeholder silhouette.
    # Observed: present 23-54% bright, absent 0-2%.
    min_bright = 0.05
    templates = parse_digit_templates()
    owned = {}      # rune -> count
    warnings = []
    for s in stats:
        if s["bright"] >= min_bright:
            cnt = read_digit_count(gray, cfg, scale, s, templates)
            owned[s["rune"]] = max(owned.get(s["rune"], 0), cnt)

    # Sanity checks for a plausible rune-tab reading
    if th is not None and hi_mean is not None and lo_mean is not None:
        if (hi_mean - lo_mean) < cfg["min_present_delta"]:
            warnings.append("slot brightness is uniform — is the RUNES tab open?")
    else:
        warnings.append("could not analyze slots — is the stash open?")

    n_present = len(owned)
    if n_present > 30:
        warnings.append(f"suspicious: {n_present} of {n_runes} runes detected as present")

    return dict(
        size=(w, h), owned=owned, warnings=warnings,
        threshold=th, lo_mean=lo_mean, hi_mean=hi_mean,
        stats=stats,
    )


# --------------------------------------------------------------------------
# Runeword matching
# --------------------------------------------------------------------------
def match_runewords(owned):
    craftable = []
    for name, runes, socks, types, req, patch, _mods in RW:
        missing = [rn for rn in runes if owned.get(rn, 0) < 1]
        if not missing:
            copies = min(owned[rn] for rn in runes)
            craftable.append((name, runes, socks, types, req, patch, copies))
        else:
            craftable.append((name, runes, socks, types, req, patch, 0, missing))
    return craftable


def fmt_result(res, cfg, show_near=True):
    owned = res["owned"]
    lines = []
    lines.append("=" * 62)
    lines.append("D2R RUNES → RUNEWORDS   (screen %dx%d)" % res["size"])
    lines.append("=" * 62)
    for wmsg in res["warnings"]:
        lines.append("⚠ " + wmsg)
    if not owned:
        lines.append("No runes detected.")
    else:
        owned_sorted = sorted(owned.items(), key=lambda kv: RUNES.index(kv[0]))
        lines.append("Runes owned: " + ", ".join(f"{k} x{v}" for k, v in owned_sorted))
    lines.append("")

    craftable = [c for c in match_runewords(owned) if c[6] > 0]
    near = [c for c in match_runewords(owned) if c[6] == 0 and len(c[7]) == 1]
    craftable.sort(key=lambda c: (c[2], c[4]))
    near.sort(key=lambda c: (c[2], c[4]))

    lines.append(f"CRAFTABLE RUNEWORDS ({len(craftable)}):")
    if not craftable:
        lines.append("  (none — need more runes)")
    for name, runes, socks, types, req, patch, copies in craftable:
        multi = f"  x{copies}" if copies > 1 else ""
        lines.append(f"  {name:<22} {' '.join(runes):<26} {socks} soc  {', '.join(types)}{multi}")
    lines.append("")

    if show_near and near:
        lines.append(f"One rune short ({len(near)}):")
        for name, runes, socks, types, req, patch, copies, missing in near:
            lines.append(f"  {name:<22} {' '.join(runes):<26} {socks} soc  {', '.join(types)}  (missing: {missing[0]})")
        lines.append("")
    lines.append("Rune order matters! Socket in the exact order shown.")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Hotkey listener — XGrabKey on X11, RegisterHotKey on Windows
# --------------------------------------------------------------------------
def _notify(title, text, critical=False):
    """Desktop notification: notify-send on Linux, a beep on Windows.

    Never raises — missing notification tools (e.g. no notify-send on a
    minimal install) are ignored; callers still print the result.
    """
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.user32.MessageBeep(0x10 if critical else 0)
        except Exception:
            pass
        return
    try:
        args = ["notify-send"] + (["-u", "critical"] if critical else ["-t", "8000"])
        subprocess.run(args + [title, text], capture_output=True)
    except Exception:
        pass


# Windows virtual-key codes for the keysyms the GUI accepts as hotkeys.
_WIN_VK = {
    **{f"F{i}": 0x6F + i for i in range(1, 25)},       # VK_F1 = 0x70
    **{str(i): 0x30 + i for i in range(10)},
    **{chr(c): ord(chr(c).upper()) for c in range(ord("a"), ord("z") + 1)},
    "Home": 0x24, "End": 0x23, "Prior": 0x21, "Next": 0x22,
    "Insert": 0x2D,
    **{f"KP_{i}": 0x60 + i for i in range(10)},
    "KP_Divide": 0x6F, "KP_Multiply": 0x6A, "KP_Subtract": 0x6D,
    "KP_Add": 0x6B, "KP_Decimal": 0x6E,
    "comma": 0xBC, "period": 0xBE, "minus": 0xBD, "equal": 0xBB,
    "semicolon": 0xBA, "apostrophe": 0xDE, "slash": 0xBF,
    "backslash": 0xDC, "bracketleft": 0xDB, "bracketright": 0xDD,
    "grave": 0xC0,
    # shifted symbols map to their base key (no modifier is registered)
    "exclam": 0x31, "at": 0x32, "numbersign": 0x33, "dollar": 0x34,
    "percent": 0x35, "asciicircum": 0x36, "ampersand": 0x37,
    "asterisk": 0x38, "parenleft": 0x39, "parenright": 0x30,
    "underscore": 0xBD, "plus": 0xBB, "braceleft": 0xDB, "braceright": 0xDD,
    "bar": 0xDC, "colon": 0xBA, "quotedbl": 0xDE, "question": 0xBF,
    "less": 0xBC, "greater": 0xBE, "asciitilde": 0xC0,
}


def parse_hotkey(hotkey_str):
    """
    Parse a hotkey string like 'Ctrl+J', 'Ctrl+Shift+F8', or 'F8'.
    Returns (mods_set, key_name)
    where mods_set is a set containing any of {'Ctrl', 'Alt', 'Shift', 'Win'}.
    """
    if not hotkey_str:
        return set(), ""
    parts = [p.strip() for p in hotkey_str.split("+") if p.strip()]
    if not parts:
        return set(), ""
    mods = set()
    key = parts[-1]
    for p in parts[:-1]:
        pl = p.lower()
        if pl in ("ctrl", "control"):
            mods.add("Ctrl")
        elif pl in ("alt",):
            mods.add("Alt")
        elif pl in ("shift",):
            mods.add("Shift")
        elif pl in ("win", "super"):
            mods.add("Win")
    return mods, key


def win_vk(keysym):
    """Map a tkinter keysym to a Windows virtual-key code, or None."""
    if keysym in _WIN_VK:
        return _WIN_VK[keysym]
    if len(keysym) == 1 and keysym.isalnum():
        return ord(keysym.upper())
    return None


def hotkey_to_win(hotkey_str):
    """
    Map a hotkey string to Windows (fsModifiers, vk).
    Returns (fsModifiers, vk) or (None, None) if key is unsupported.
    """
    mods, key = parse_hotkey(hotkey_str)
    vk = win_vk(key)
    if vk is None and len(key) == 1 and key.isalnum():
        vk = ord(key.upper())
    if vk is None:
        return None, None
    MOD_ALT = 0x0001
    MOD_CONTROL = 0x0002
    MOD_SHIFT = 0x0004
    MOD_WIN = 0x0008
    MOD_NOREPEAT = 0x4000

    fs = MOD_NOREPEAT
    if "Ctrl" in mods:
        fs |= MOD_CONTROL
    if "Alt" in mods:
        fs |= MOD_ALT
    if "Shift" in mods:
        fs |= MOD_SHIFT
    if "Win" in mods:
        fs |= MOD_WIN
    return fs, vk


def hotkey_to_xlib(hotkey_str, d):
    """
    Map a hotkey string to Xlib (keycode, base_modmask).
    Returns (keycode, mask) or (None, 0) if unmappable.
    """
    from Xlib import X, XK
    mods, key = parse_hotkey(hotkey_str)
    xk = XK.string_to_keysym(key)
    if not xk:
        xk = XK.string_to_keysym(key.lower())
    if not xk:
        return None, 0
    kc = d.keysym_to_keycode(xk)
    if not kc:
        return None, 0
    mask = 0
    if "Ctrl" in mods:
        mask |= X.ControlMask
    if "Alt" in mods:
        mask |= X.Mod1Mask
    if "Shift" in mods:
        mask |= X.ShiftMask
    if "Win" in mods:
        mask |= X.Mod4Mask
    return kc, mask


def _listen_win(cfg, hotkey_str):
    """Global hotkey on Windows: RegisterHotKey + thread message loop."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    fs, vk = hotkey_to_win(hotkey_str)
    if vk is None:
        sys.exit(f"hotkey '{hotkey_str}' is not supported on Windows — "
                 "pick a letter, digit, F-key or numpad key with optional Ctrl/Alt/Shift")
    WM_HOTKEY = 0x0312
    hk_id = 1
    if not user32.RegisterHotKey(None, hk_id, fs, vk):
        sys.exit(f"could not register '{hotkey_str}' (another app owns it?)")
    print(f"D2R companion listening — press {hotkey_str} with the RUNES tab "
          "open (Ctrl-C to quit).")
    sys.stdout.flush()
    try:
        msg = wintypes.MSG()
        while True:
            r = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if r <= 0:
                break
            if msg.message == WM_HOTKEY and msg.wParam == hk_id:
                try:
                    do_capture(cfg, notify=True, verbose=False)
                except Exception as e:
                    _notify("D2R Runewords", f"error: {e}", critical=True)
    finally:
        user32.UnregisterHotKey(None, hk_id)


def listen(cfg):
    hotkey_str = (cfg.get("hotkey") or "F8")
    if sys.platform.startswith("win"):
        _listen_win(cfg, hotkey_str)
        return
    from Xlib import X, display, XK
    d = display.Display()
    # suppress noisy BadAccess errors while probing modifier combos
    try:
        d.set_error_handler(lambda *a: None)
    except Exception:
        pass
    root = d.screen().root
    keycode, mask = hotkey_to_xlib(hotkey_str, d)
    if not keycode:
        sys.exit(f"could not map '{hotkey_str}'")
    grabbed = 0
    for mod in (mask, mask | X.LockMask, mask | X.Mod2Mask, mask | X.LockMask | X.Mod2Mask):
        try:
            root.grab_key(keycode, mod, True, X.GrabModeAsync, X.GrabModeAsync)
            grabbed += 1
        except Exception:
            pass
    if not grabbed:
        sys.exit(f"could not grab '{hotkey_str}' (another app owns it?)")
    d.sync()
    print(f"D2R companion listening — press {hotkey_str} with the RUNES tab open (Ctrl-C to quit).")
    sys.stdout.flush()
    while True:
        try:
            ev = d.next_event()
        except Exception:
            continue
        if ev.type == X.KeyPress and ev.detail == keycode:
            clean_state = ev.state & ~(X.LockMask | X.Mod2Mask)
            if clean_state == mask:
                try:
                    do_capture(cfg, notify=True, verbose=False)
                except Exception as e:
                    _notify("D2R Runewords", f"error: {e}", critical=True)


def do_capture(cfg, notify=False, verbose=False):
    path = capture_screen(cfg)
    try:
        res = analyze_image(path, cfg, verbose=verbose)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    text = fmt_result(res, cfg)
    if verbose:
        print(text)
    with open(cfg["result_file"], "w") as f:
        f.write(text + "\n")
    n_craft = len([c for c in match_runewords(res["owned"]) if c[6] > 0])
    if notify:
        summary = f"{n_craft} craftable runewords"
        if res["warnings"]:
            summary += " — " + res["warnings"][0]
        _notify("D2R Runewords", summary)
        print(text)
    return text


def main():
    ap = argparse.ArgumentParser(description="D2R rune stash → runeword checker")
    ap.add_argument("--capture", action="store_true", help="screenshot the screen and analyze")
    ap.add_argument("--image", metavar="FILE", help="analyze an existing screenshot")
    ap.add_argument("--listen", action="store_true", help="run as daemon; F8 = capture+analyze")
    ap.add_argument("--calibrate", action="store_true", help="print per-slot stats (verify layout)")
    ap.add_argument("--list", action="store_true", help="print the runeword database")
    ap.add_argument("--verbose", action="store_true", help="print everything")
    ap.add_argument("--all", action="store_true", help="also list runewords one rune short")
    args = ap.parse_args()

    cfg = load_config()

    if args.list:
        for name, runes, socks, types, req, patch, _mods in RW:
            print(f"{name:<22} {' '.join(runes):<26} {socks} soc  {', '.join(types):<42} lvl {req}  patch {patch}")
        return

    if args.listen:
        listen(cfg)
        return

    if args.capture:
        do_capture(cfg, notify=False, verbose=True)
        return

    if args.image:
        res = analyze_image(args.image, cfg, verbose=args.verbose)
        print(fmt_result(res, cfg, show_near=args.all))
        if args.verbose:
            print("\nPer-slot stats (mean brightness / bright %):")
            for s in res["stats"]:
                print(f"  {s['rune']:<6} mean={s['mean']:6.1f}  bright={s['bright']*100:5.1f}%")
        return

    if args.calibrate:
        # same as --image but only print stats
        if not args.image:
            ap.error("--calibrate needs --image FILE (or use --capture)")
        res = analyze_image(args.image, cfg, verbose=True)
        print(fmt_result(res, cfg))
        print("\nPer-slot stats (mean brightness / bright %):")
        for s in res["stats"]:
            print(f"  {s['rune']:<6} mean={s['mean']:6.1f}  bright={s['bright']*100:5.1f}%")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
