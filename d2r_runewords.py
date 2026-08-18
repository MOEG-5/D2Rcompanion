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
The D2R runes tab renders the 33 runes in a fixed 9x4 grid.  Runes you own
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
"hotkey" key, default F8).  The GUI (d2rc.py) lets you assign it visually.

Setup / requirements
--------------------
  * Linux (X11): python3, PIL, numpy, python-xlib, ImageMagick's `import`,
    notify-send.  Windows: plain Python + PIL + numpy — screen capture uses
    PIL ImageGrab and the global hotkey uses RegisterHotKey (ctypes), so no
    extra packages are needed.
  * Play Diablo 2: Resurrected in fullscreen (or borderless windowed) at the
    same resolution as the screenshot used to calibrate (1920x1080 by
    default) — the layout scales automatically with the screen size, but the
    game window must fill the screen (or use the offsets in the config file).
  * The stash window must be open with the RUNES tab selected when you hit F8.

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
    "rows": 4,
    "offset_x": 0,   # extra manual offset (multi-monitor / windowed play)
    "offset_y": 0,
    "bright_threshold": 120,     # pixel brightness considered "bright"
    "digit_threshold": 140,       # brighter threshold to isolate the count digit
    "min_present_delta": 12,     # min gap between present/absent cluster means
    "digit_accept": 0.80,        # min IoU to accept a detected count digit
    "result_file": os.path.expanduser("~/d2r_runewords_result.txt"),
    "hotkey": "",                # global scan hotkey (assigned via the GUI)
}

# Quantity digit reference grids (14x10), learned from the calibration screenshot.
# '#' = digit stroke.  Used to read stack sizes (1/2/3 recognized; anything
# else or a weak match falls back to 1).  Counts are a best-effort extra.
DIGIT_TEMPLATES = {
    1: ["#........#|#........#|#........#|..........|#........#|#........#|..........|#........#|#........#|..........|#.........|#.........|..........|#........#"],
    2: ["...#......|..........|..........|..........|..........|..........|.#.#......|..........|..........|..........|..........|..........|..........|##.#.#.#.#"],
    3: [".....#....|..........|...#.#.#..|..........|.......#.#|..........|.........#|..........|.........#|..........|##.....#.#|..........|..........|.#.#.#.#.."],
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
                      for row in rows[0].split("|")])
        out[k] = g
    return out


# --------------------------------------------------------------------------
# Screen capture
# --------------------------------------------------------------------------
def capture_screen(cfg):
    """Grab the screen — PIL ImageGrab on Windows, `import` on X11."""
    out = tempfile.mktemp(suffix=".png", prefix="d2r_cap_")
    if sys.platform.startswith("win"):
        from PIL import ImageGrab
        ImageGrab.grab().save(out)
        return out
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


def _label_components(binary):
    """4-connected component labeling — scipy.ndimage.label drop-in.

    Two-pass union-find over a small binary patch (<= ~20x20 px), so the
    plain-Python loop is effectively free.  Keeps the scanner free of scipy
    (~150 MB when bundled into a frozen build).
    """
    H, W = binary.shape
    lab = np.zeros((H, W), dtype=np.int32)
    parent = [0]                        # 1-based provisional label -> root
    n = 0

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for y in range(H):
        for x in range(W):
            if not binary[y, x]:
                continue
            left = lab[y, x - 1] if x > 0 else 0
            up = lab[y - 1, x] if y > 0 else 0
            if left and up:
                if left != up:
                    union(left, up)
                lab[y, x] = left
            elif left:
                lab[y, x] = left
            elif up:
                lab[y, x] = up
            else:
                n += 1
                parent.append(n)
                lab[y, x] = n

    # second pass: collapse every pixel to its root, renumber 1..k
    roots = {}
    k = 0
    for y in range(H):
        for x in range(W):
            if lab[y, x]:
                r = find(lab[y, x])
                if r not in roots:
                    k += 1
                    roots[r] = k
                lab[y, x] = roots[r]
    return lab, k


def read_digit_count(gray, cfg, scale, stats, templates):
    """Best-effort stack count from the white digit in the slot's corner."""
    x0, y0 = stats["x0"], stats["y0"]
    sx, sy = scale
    # digit lives in the bottom-right corner of the slot (calibrated margins)
    r0 = int(round(y0 + 28 * sy))
    r1 = int(round(y0 + 46 * sy))
    c0 = int(round(x0 + 30 * sx))
    c1 = int(round(x0 + 47 * sx))
    reg = gray[r0:r1, c0:c1]
    if reg.size == 0:
        return 1
    binary = reg > cfg["digit_threshold"]
    lab, n = _label_components(binary)
    if n == 0:
        return 1
    sizes = np.bincount(lab.ravel())
    sizes[0] = 0                        # ignore the background class
    best = int(np.argmax(sizes))
    ys, xs = np.where(lab == best)
    H, W = 14, 10
    canvas = np.zeros((H, W), dtype=float)
    h_rng = max(ys.max() - ys.min(), 1)
    w_rng = max(xs.max() - xs.min(), 1)
    ry = ((ys - ys.min()) / h_rng * (H - 1)).astype(int)
    rx = ((xs - xs.min()) / w_rng * (W - 1)).astype(int)
    canvas[ry, rx] = 1
    best_k, best_iou = None, -1.0
    for k, t in templates.items():
        inter = (canvas * t).sum()
        iou = inter / max(canvas.sum() + t.sum() - inter, 1)
        if iou > best_iou:
            best_iou, best_k = iou, k
    if best_iou >= cfg["digit_accept"]:
        return int(best_k)
    return 1


def analyze_image(path, cfg, verbose=False):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    gray = np.array(img).mean(axis=2)
    scale = (w / cfg["baseline_w"], h / cfg["baseline_h"])

    n_runes = len(RUNES)
    stats = []
    for r in range(cfg["rows"]):
        for c in range(cfg["cols"]):
            idx = r * cfg["cols"] + c
            if idx >= n_runes:
                continue
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
    """Desktop notification: notify-send on Linux, a beep on Windows."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.user32.MessageBeep(0x10 if critical else 0)
        except Exception:
            pass
        return
    args = ["notify-send"] + (["-u", "critical"] if critical else ["-t", "8000"])
    subprocess.run(args + [title, text], capture_output=True)


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


def win_vk(keysym):
    """Map a tkinter keysym to a Windows virtual-key code, or None."""
    if keysym in _WIN_VK:
        return _WIN_VK[keysym]
    if len(keysym) == 1 and keysym.isalnum():
        return ord(keysym.upper())
    return None


def _listen_win(cfg, keysym):
    """Global hotkey on Windows: RegisterHotKey + thread message loop."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    vk = win_vk(keysym)
    if vk is None:
        sys.exit(f"key {keysym} is not supported on Windows — "
                 "pick a letter, digit, F-key or numpad key")
    MOD_NOREPEAT, WM_HOTKEY = 0x4000, 0x0312
    hk_id = 1
    if not user32.RegisterHotKey(None, hk_id, MOD_NOREPEAT, vk):
        sys.exit(f"could not register {keysym} (another app owns it?)")
    print(f"D2R companion listening — press {keysym} with the RUNES tab "
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
    keysym = (cfg.get("hotkey") or "F8")
    if sys.platform.startswith("win"):
        _listen_win(cfg, keysym)
        return
    from Xlib import X, display, XK
    d = display.Display()
    # suppress noisy BadAccess errors while probing modifier combos
    try:
        d.set_error_handler(lambda *a: None)
    except Exception:
        pass
    root = d.screen().root
    xk = XK.string_to_keysym(keysym)
    keycode = d.keysym_to_keycode(xk) if xk else None
    if not keycode:
        sys.exit(f"could not map {keysym} keysym")
    grabbed = 0
    for mod in (0, X.LockMask, X.Mod2Mask, X.LockMask | X.Mod2Mask):
        try:
            root.grab_key(keycode, mod, True, X.GrabModeAsync, X.GrabModeAsync)
            grabbed += 1
        except Exception:
            pass
    if not grabbed:
        sys.exit(f"could not grab {keysym} (another app owns it?)")
    d.sync()
    print(f"D2R companion listening — press {keysym} with the RUNES tab open (Ctrl-C to quit).")
    sys.stdout.flush()
    while True:
        try:
            ev = d.next_event()
        except Exception:
            continue
        if ev.type == X.KeyPress and ev.detail == keycode:
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
