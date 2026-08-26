#!/usr/bin/env python3
"""
D2R Companion — rune stash → runeword finder (GUI)
===================================================
Tkinter companion app for Diablo 2: Resurrected.  Reads the rune stash
(RUNES tab) straight from the screen and shows:

  * Tab 1 "My runes"       — runewords you can craft right now (with full
                             effect descriptions), and below them the ones
                             one rune short (missing rune highlighted).
  * Tab 2 "All runewords"  — complete list sorted by required level.
  * Tab 3 "Cube recipes"   — Horadric cube recipes (socketing, crafting,
                             rune & gem upgrades, rerolling, ...).
  * Tab 4 "Unique items"   — every unique item with full stats, grouped by
                             item category.
  * Tab 5 "Set items"      — every set with its pieces/stats plus the
                             partial and complete set bonuses.

A search box at the top filters the ACTIVE tab live (partial words match
names, runes, item types, effect text, recipe ingredients, ...).

Scanning is hotkey-driven: click "Assign hotkey", press a key, and from
then on that key is grabbed globally (always on, remembered across runs).
With the stash open on the RUNES tab in D2R, press the hotkey to re-scan.

Usage:
  python3 d2rc.py                # start the app
  python3 d2rc.py --image FILE   # start with a screenshot pre-loaded
"""

import argparse
import os
import queue
import sys
import threading
import time

# make sibling modules importable regardless of CWD
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import tkinter as tk
from tkinter import ttk, font as tkfont

import d2r_data
import d2r_items
import d2r_runewords as core

# --------------------------------------------------------------------------
# palette / fonts
# --------------------------------------------------------------------------
BG      = "#1b1b20"   # app background
BG2     = "#232329"   # panels
PANEL   = "#2c2c36"   # buttons / fields / selected tab
PANEL2  = "#373742"   # hover / scrollbar thumb
BORDER  = "#3f3f4b"   # separators / field borders
FG      = "#d9d9de"   # body text
DIM     = "#8a8a93"   # muted text
GOLD    = "#d4af37"
NAME    = "#e8c86a"
RUNEC   = "#7ec8ff"
BASEC   = "#9fd0a0"
SKILLC  = "#d0a0e8"
MISS    = "#ff6b6b"
SEC     = "#ffffff"
EFF     = "#c9c9c9"
OK      = "#7ddc7d"

CAT_COLORS = {
    "Crafting":          "#e8a06a",
    "Socketing":         "#a0d8ef",
    "Rune upgrading":    "#c9a6f0",
    "Gem upgrading":     "#9be89b",
    "Item upgrading":    "#e8e89b",
    "Repair & recharge": "#d9a0d0",
    "Rerolling":         "#e8c06a",
    "Quest & special":   "#b0b0b8",
}

# keys that must never become the hotkey (they'd be stolen from the game)
MODIFIER_KEYS = {
    "Alt_L", "Alt_R", "Control_L", "Control_R", "Shift_L", "Shift_R",
    "Super_L", "Super_R", "Meta_L", "Meta_R", "Hyper_L", "Hyper_R",
    "Caps_Lock", "Num_Lock", "Scroll_Lock", "ISO_Level3_Shift",
    "Mode_switch", "Multi_key", "Menu", "Win_L", "Win_R",
}
BLOCKED_KEYS = {"Escape", "Return", "KP_Enter", "Tab", "space",
                "BackSpace", "Delete"}


def _setup_style():
    """Dark ttk theme — kills the default light-grey buttons/borders."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=BG)

    # notebook — flat, no grey frame around the pages
    style.configure("TNotebook", background=BG, borderwidth=0,
                    tabmargins=(0, 0, 0, 0))
    style.configure("TNotebook.Tab", background=BG2, foreground=DIM,
                    padding=(22, 9), borderwidth=0, focuscolor=BG)
    # NOTE: no "expand" on select, and clam's own padding map is overridden
    # (it adds 2px top padding on "selected") — tabs must keep a constant
    # size; the colour change alone signals the active tab.
    style.map("TNotebook.Tab",
              background=[("selected", PANEL), ("active", PANEL)],
              foreground=[("selected", GOLD), ("active", FG)],
              lightcolor=[("selected", BG2), ("active", BG2)],
              darkcolor=[("selected", BG2), ("active", BG2)],
              padding=[("selected", (22, 9)), ("active", (22, 9))])

    # buttons — flat, dark
    style.configure("TButton", background=PANEL, foreground=FG,
                    bordercolor=PANEL, lightcolor=PANEL, darkcolor=PANEL,
                    focuscolor=PANEL, padding=(14, 7), relief="flat")
    style.map("TButton",
              background=[("active", PANEL2), ("pressed", BG2)],
              foreground=[("active", GOLD), ("pressed", GOLD)],
              bordercolor=[("active", PANEL2), ("pressed", PANEL2)])

    # the hotkey button — slightly golden
    style.configure("Accent.TButton", background=BG2, foreground=GOLD,
                    bordercolor="#4c421e", lightcolor="#4c421e",
                    darkcolor="#4c421e", focuscolor=BG2, padding=(14, 7),
                    relief="flat")
    style.map("Accent.TButton",
              background=[("active", PANEL2), ("pressed", BG2)],
              foreground=[("active", "#f0d98c"), ("pressed", "#f0d98c")],
              bordercolor=[("active", "#6a5c28"), ("pressed", "#4c421e")])

    # search field — dark, gold border on focus
    style.configure("TEntry", fieldbackground=BG2, foreground=FG,
                    insertcolor=FG, bordercolor=BORDER, lightcolor=BORDER,
                    darkcolor=BORDER, padding=(8, 6))
    style.map("TEntry",
              bordercolor=[("focus", GOLD)],
              lightcolor=[("focus", GOLD)],
              darkcolor=[("focus", GOLD)])

    # scrollbars — dark, no arrows look
    style.configure("Vertical.TScrollbar", background=PANEL2,
                    troughcolor=BG, bordercolor=BG, arrowcolor=FG,
                    relief="flat", width=13)
    style.map("Vertical.TScrollbar",
              background=[("active", PANEL2), ("pressed", PANEL2)],
              arrowcolor=[("active", GOLD)])


def pretty_key(keysym):
    """Human-friendly label for a tkinter keysym."""
    if keysym == "space":
        return "Space"
    if len(keysym) == 1:
        return keysym.upper()
    return keysym


class App:
    def __init__(self, root, preload_image=None):
        self.root = root
        root.title("D2R Companion — runeword finder")
        root.geometry("1080x760")
        root.configure(bg=BG)

        self.cfg = core.load_config()
        self.owned = None          # last scan: rune -> count
        self.last_scan_info = None

        # hotkey state
        self.hotkey_keysym = ""
        self.hotkey_on = False
        self.assigning = False
        self._grab_display = None
        self._grab_keycode = None
        self._win_hk_tid = None          # Windows RegisterHotKey thread id
        self._win_hk_result = None       # Windows registration result queue
        self._hotkey_thread = None
        self._hotkey_q = queue.Queue()   # hotkey thread -> main thread

        self._fonts()
        _setup_style()
        self._build_ui()
        self._refresh_timer = None

        # always-on hotkey (persisted in the config); first run = unassigned
        self._update_hotkey_button()
        if self.cfg.get("hotkey"):
            self._start_hotkey(self.cfg["hotkey"])
        else:
            self._set_status("No hotkey assigned yet — click “Assign hotkey” "
                             "to choose your scan key.", DIM)

        # drain hotkey events on the main thread (queue is thread-safe)
        self.root.after(150, self._poll_hotkey_events)

        if preload_image:
            self.do_scan(file=preload_image)

    # ------------------------------------------------------------------
    def _fonts(self):
        base = tkfont.nametofont("TkDefaultFont").actual("family")
        self.f_base = tkfont.Font(family=base, size=10)
        self.f_bold = tkfont.Font(family=base, size=10, weight="bold")
        self.f_sec  = tkfont.Font(family=base, size=12, weight="bold")
        self.f_name = tkfont.Font(family=base, size=11, weight="bold")
        self.f_small = tkfont.Font(family=base, size=9)

    # ------------------------------------------------------------------
    def _build_ui(self):
        # header: title + search + hotkey button
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=12, pady=(10, 6))
        tk.Label(header, text="D2R Companion", font=self.f_sec, fg=GOLD,
                 bg=BG).pack(side="left")
        tk.Label(header, text="  search: ", font=self.f_base, fg=DIM,
                 bg=BG).pack(side="left", padx=(26, 2))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        self.search_entry = ttk.Entry(header, textvariable=self.search_var,
                                      width=42)
        self.search_entry.pack(side="left")
        tk.Label(header, text="(filters active tab — partial words OK)",
                 font=self.f_small, fg=DIM, bg=BG).pack(side="left", padx=8)

        self.hotkey_btn = ttk.Button(header, style="Accent.TButton",
                                     command=self._assign_hotkey)
        self.hotkey_btn.pack(side="right", padx=(12, 0))

        # notebook
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=12, pady=(2, 4))
        self.tab_mine = ttk.Frame(self.nb)
        self.tab_all  = ttk.Frame(self.nb)
        self.tab_cube = ttk.Frame(self.nb)
        self.tab_uni  = ttk.Frame(self.nb)
        self.tab_set  = ttk.Frame(self.nb)
        self.nb.add(self.tab_mine, text="  My runes  ")
        self.nb.add(self.tab_all,  text="  All runewords  ")
        self.nb.add(self.tab_cube, text="  Cube recipes  ")
        self.nb.add(self.tab_uni,  text="  Unique items  ")
        self.nb.add(self.tab_set,  text="  Set items  ")
        self.nb.bind("<<NotebookTabChanged>>", lambda e: self.refresh())

        # footer status bar
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")
        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=12, pady=(6, 10))
        self.status = tk.Label(footer, text="", font=self.f_small, fg=DIM,
                               bg=BG, anchor="w")
        self.status.pack(fill="x")

        # text areas
        self.txt_mine = self._make_text(self.tab_mine)
        self.txt_all  = self._make_text(self.tab_all)
        self.txt_cube = self._make_text(self.tab_cube)
        self.txt_uni  = self._make_text(self.tab_uni)
        self.txt_set  = self._make_text(self.tab_set)
        self._tag_configure_all()

        # stats bar for the item tabs
        self.n_uni = len(d2r_items.UNIQUES)
        self.n_set = len(d2r_items.SETS)
        n_set_items = sum(len(s['items']) for s in d2r_items.SETS)
        self._set_status(
            f"Loaded {self.n_uni} unique items and {self.n_set} sets "
            f"({n_set_items} set items) - Reign of the Warlock (D2R v3.x).")

    def _make_text(self, parent):
        wrap = tk.Frame(parent, bg=BG)
        wrap.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        txt = tk.Text(wrap, bg=BG, fg=FG, insertbackground=FG, relief="flat",
                      wrap="word", font=self.f_base, padx=10, pady=8,
                      highlightthickness=0, borderwidth=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)
        txt.configure(state="disabled")
        return txt

    def _tag_configure_all(self):
        for txt in (self.txt_mine, self.txt_all, self.txt_cube,
                    self.txt_uni, self.txt_set):
            txt.tag_configure("name",  font=self.f_name, foreground=NAME)
            txt.tag_configure("runes", font=self.f_bold, foreground=RUNEC)
            txt.tag_configure("base",  font=self.f_bold, foreground=BASEC)
            txt.tag_configure("skill", font=self.f_bold, foreground=SKILLC)
            txt.tag_configure("miss",  font=self.f_bold, foreground=MISS)
            txt.tag_configure("sec",   font=self.f_sec,  foreground=SEC)
            txt.tag_configure("dim",   font=self.f_small, foreground=DIM)
            txt.tag_configure("ok",    font=self.f_bold, foreground=OK)
            txt.tag_configure("eff",   foreground=EFF)
            for cat, col in CAT_COLORS.items():
                txt.tag_configure("cat:" + cat, font=self.f_small,
                                  foreground=col)

    def _poll_hotkey_events(self):
        try:
            while True:
                fn = self._hotkey_q.get_nowait()
                try:
                    fn()
                except Exception:
                    pass
        except queue.Empty:
            pass
        self.root.after(150, self._poll_hotkey_events)

    # ------------------------------------------------------------------
    def _set_status(self, text, color=None):
        self.status.config(text=text, fg=color or DIM)

    # ------------------------------------------------------------------
    # rendering helpers
    # ------------------------------------------------------------------
    def _set_text(self, txt, segments):
        txt.configure(state="normal")
        txt.delete("1.0", "end")
        text = "".join(s for s, _ in segments)
        txt.insert("1.0", text)
        pos = "1.0"
        for s, tag in segments:
            if s and tag:
                txt.tag_add(tag, pos, f"{pos}+{len(s)}c")
            pos = txt.index(f"{pos}+{len(s)}c")
        txt.configure(state="disabled")
        txt.yview_moveto(0.0)

    # ------------------------------------------------------------------
    # content builders
    # ------------------------------------------------------------------
    def _rw_card(self, seg, rw, missing=None):
        name, runes, socks, types, req, patch, mods = rw
        seg.append(("  ✧ ", "name"))
        seg.append((name, "name"))
        meta = f"   [lvl {req if req else '?'} · {socks} socket"
        meta += f"{'s' if socks != 1 else ''}"
        if patch:
            meta += f" · {patch}"
        meta += "]"
        seg.append((meta + "\n", "dim"))
        seg.append(("     Runes: ", "dim"))
        seg.append((" + ".join(runes), "runes"))
        seg.append(("\n", None))
        if missing:
            seg.append(("     ⚠ missing: ", "miss"))
            seg.append((", ".join(missing), "miss"))
            seg.append(("\n", None))
        seg.append((f"     Item types: {', '.join(types)}\n", "eff"))
        if mods:
            if len(mods) == 1:
                seg.append(("     Effects:\n", "dim"))
                for line in mods[0]:
                    seg.append((f"       {line}\n", "eff"))
            else:
                for i, lines in enumerate(mods):
                    tname = types[i] if i < len(types) else f"variant {i+1}"
                    seg.append((f"     Effects ({tname}):\n", "dim"))
                    for line in lines:
                        seg.append((f"       {line}\n", "eff"))
        seg.append(("\n", None))

    def _rec_card(self, seg, rec):
        title, cat, ingredients, output = rec
        seg.append(("  ✧ ", "name"))
        seg.append((title, "name"))
        seg.append((f"   [{cat}]", "cat:" + cat))
        seg.append(("\n", None))
        ing = " + ".join(f"{q} {n}" for q, n in ingredients)
        out = " → " + " + ".join(f"{q} {n}" for q, n in output)
        seg.append((f"     {ing}{out}\n", "eff"))
        rolls = d2r_data.CRAFT_ROLLS.get(title)
        if rolls:
            seg.append(("     Always rolls:\n", "dim"))
            for line in rolls:
                seg.append((f"       {line}\n", "eff"))
            seg.append(("     Plus 1-4 random affixes (magic/rare pool — "
                        "more at higher item level)\n", "dim"))
        seg.append(("\n", None))

    # ------------------------------------------------------------------
    # data views
    # ------------------------------------------------------------------
    def _view_mine(self, seg, q):
        if not self.owned:
            seg.append(("  No scan yet.\n\n", "sec"))
            seg.append(("  Open Diablo 2: Resurrected, open your stash on the "
                        "RUNES tab,\n  then press your scan hotkey (see the "
                        "button in the top-right corner).\n", "eff"))
            return
        owned = self.owned
        if not owned:
            seg.append(("  (no runes detected yet)\n", "dim"))
        else:
            owned_sorted = sorted(owned.items(),
                                  key=lambda kv: d2r_data.RUNES.index(kv[0]))
            line = "  YOUR RUNES:  " + "  ".join(
                f"{k} ×{v}" for k, v in owned_sorted)
            seg.append((line + "\n\n", "ok"))

        def matches(rw):
            name, runes, socks, types, req, patch, mods = rw
            hay = " ".join([name] + list(runes) + list(types)
                           + [m for mod in mods for m in mod]
                           + [patch or ""])
            return q in hay.lower()

        craft = [rw for rw in d2r_data.RUNEWORDS
                 if matches(rw) and all(owned.get(r, 0) >= 1 for r in rw[1])]
        near = [rw for rw in d2r_data.RUNEWORDS
                if matches(rw) and not all(owned.get(r, 0) >= 1 for r in rw[1])
                and sum(1 for r in rw[1] if owned.get(r, 0) < 1) == 1]
        craft.sort(key=lambda r: (r[2], r[4] or 0))
        near.sort(key=lambda r: (r[2], r[4] or 0))

        seg.append((f"CRAFTABLE RUNEWORDS ({len(craft)})\n", "sec"))
        if not craft:
            seg.append(("  (none — you need more runes)\n\n", "dim"))
        for rw in craft:
            self._rw_card(seg, rw)

        seg.append((f"ONE RUNE SHORT ({len(near)})\n", "sec"))
        if not near:
            seg.append(("  (none)\n", "dim"))
        for rw in near:
            missing = [r for r in rw[1] if owned.get(r, 0) < 1]
            self._rw_card(seg, rw, missing=missing)
        seg.append(("  Runewords need their runes in the exact order shown!\n",
                    "dim"))

    def _view_all(self, seg, q):
        rws = sorted(d2r_data.RUNEWORDS, key=lambda r: (r[4] or 0, r[0]))
        if q:
            rws = [rw for rw in rws if self._rw_matches(rw, q)]
        if not rws:
            seg.append(("  (nothing matches)\n", "dim"))
            return
        last_lvl = None
        for rw in rws:
            lvl = rw[4] or 0
            if lvl != last_lvl:
                seg.append((f"── Level {lvl} ──\n", "sec"))
                last_lvl = lvl
            self._rw_card(seg, rw)

    def _view_cube(self, seg, q):
        recs = d2r_data.RECIPES
        if q:
            recs = [r for r in recs if self._rec_matches(r, q)]
        if not recs:
            seg.append(("  (nothing matches)\n", "dim"))
            return
        cats = [c for c in CAT_COLORS]
        for cat in cats:
            group = [r for r in recs if r[1] == cat]
            if not group:
                continue
            seg.append((f"── {cat.upper()} ({len(group)}) ──\n", "sec"))
            for rec in group:
                self._rec_card(seg, rec)

    # ------------------------------------------------------------------
    # unique / set items
    # ------------------------------------------------------------------
    def _item_card(self, seg, it, prefix="     "):
        name, category, base, quality, small, mods, patch = it
        meta = " ".join(x for x in (base, quality, patch) if x)
        seg.append((prefix + "✧ ", "name"))
        seg.append((name, "name"))
        seg.append((f"   [{meta}]\n", "dim"))
        if small:
            for line in small:
                seg.append((f"{prefix}  {line}\n", "eff"))
        for line in mods:
            seg.append((f"{prefix}  {line}\n", "skill"))
        seg.append(("\n", None))

    def _set_card(self, seg, s):
        name = s['name']
        modline = " ".join(x for x in (name, s['patch']) if x)
        seg.append(("  ✧ ", "name"))
        seg.append((name, "name"))
        seg.append((f"   [{s['patch']}]" if s['patch'] else "", "dim"))
        seg.append((f"   {len(s['items'])} pieces\n", "dim"))
        for it in s['items']:
            seg.append((f"     • {it[0]}  ", "runes"))
            seg.append((f"[{it[1]}]\n", "base"))
            for line in it[3]:
                seg.append((f"         {line}\n", "eff"))
        if s['partial']:
            seg.append(("     Partial set bonus:\n", "ok"))
            for count, mods in s['partial']:
                seg.append((f"     ({count} items)\n", "base"))
                for m in mods:
                    seg.append((f"       {m}\n", "eff"))
        if s['full']:
            seg.append(("     Complete set bonus:\n", "ok"))
            for m in s['full']:
                seg.append((f"       {m}\n", "eff"))
        seg.append(("\n", None))

    def _view_uniques(self, seg, q):
        items = d2r_items.UNIQUES
        if q:
            items = [i for i in items if self._item_matches(i, q)]
        if not items:
            seg.append(("  (nothing matches)\n", "dim"))
            return
        last = None
        for it in items:
            if it[1] != last:
                seg.append((f"── {it[1].upper()} ──\n", "sec"))
                last = it[1]
            self._item_card(seg, it)

    def _view_sets(self, seg, q):
        sets = d2r_items.SETS
        if q:
            sets = [s for s in sets if self._set_matches(s, q)]
        if not sets:
            seg.append(("  (nothing matches)\n", "dim"))
            return
        for s in sets:
            self._set_card(seg, s)

    @staticmethod
    def _item_matches(it, q):
        name, cat, base, qual, small, mods, patch = it
        hay = " ".join([name, cat, base, qual, patch] + small + mods)
        return q in hay.lower()

    @staticmethod
    def _set_matches(s, q):
        hay = " ".join([s['name'], s['patch']])
        for it in s['items']:
            hay += " " + " ".join([it[0], it[1]] + it[2] + it[3])
        for _c, mods in s['partial']:
            hay += " " + " ".join(mods)
        hay += " " + " ".join(s['full'])
        return q in hay.lower()

    @staticmethod
    def _rw_matches(rw, q):
        name, runes, socks, types, req, patch, mods = rw
        hay = " ".join([name] + list(runes) + list(types)
                       + [m for mod in mods for m in mod] + [patch or ""])
        return q in hay.lower()

    @staticmethod
    def _rec_matches(rec, q):
        title, cat, ingredients, output = rec
        hay = " ".join([title, cat] + [n for _, n in ingredients]
                       + [n for _, n in output]
                       + list(d2r_data.CRAFT_ROLLS.get(title, [])))
        return q in hay.lower()

    # ------------------------------------------------------------------
    # refresh / search
    # ------------------------------------------------------------------
    def _on_search(self, *_):
        if self._refresh_timer:
            self.root.after_cancel(self._refresh_timer)
        self._refresh_timer = self.root.after(150, self.refresh)

    def refresh(self, *_):
        q = self.search_var.get().strip().lower()
        tab = self.nb.index(self.nb.select())
        if tab == 0:
            seg = []
            self._view_mine(seg, q)
            self._set_text(self.txt_mine, seg)
        elif tab == 1:
            seg = []
            self._view_all(seg, q)
            self._set_text(self.txt_all, seg)
        elif tab == 2:
            seg = []
            self._view_cube(seg, q)
            self._set_text(self.txt_cube, seg)
        elif tab == 3:
            seg = []
            self._view_uniques(seg, q)
            self._set_text(self.txt_uni, seg)
        else:
            seg = []
            self._view_sets(seg, q)
            self._set_text(self.txt_set, seg)

    # ------------------------------------------------------------------
    # scanning
    # ------------------------------------------------------------------
    def do_scan(self, file=None):
        try:
            if file:
                res = core.analyze_image(file, self.cfg)
                src = os.path.basename(file)
            else:
                path = core.capture_screen(self.cfg)
                try:
                    res = core.analyze_image(path, self.cfg)
                finally:
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
                src = "screen"
            self.owned = res["owned"]
            self.last_scan_info = (src, res["size"])
            if res["warnings"]:
                self._set_status("⚠ " + res["warnings"][0], MISS)
            else:
                n = len([c for c in core.match_runewords(res["owned"])
                         if c[6] > 0])
                self._set_status(
                    f"OK — {n} craftable runewords "
                    f"({len(res['owned'])} runes, {src})", OK)
            self.nb.select(0)
            self.refresh()
        except Exception as e:
            self._set_status(f"scan failed: {e}", MISS)
            self.root.bell()

    # ------------------------------------------------------------------
    # hotkey — always on once assigned; click "Assign hotkey" to (re)pick
    # ------------------------------------------------------------------
    def _assign_hotkey(self):
        if self.assigning:
            self._cancel_assign()
            return
        self.assigning = True
        self.hotkey_btn.config(text="Press any key…")
        self.root.focus_set()
        self.root.bind("<KeyPress>", self._on_assign_key)
        self._set_status("Press any key to use as the scan hotkey — ESC to "
                         "cancel (ESC/Enter/Tab/Space/modifier keys are not "
                         "allowed).", GOLD)

    def _cancel_assign(self):
        self.assigning = False
        self.root.unbind("<KeyPress>")
        self._update_hotkey_button()
        self._set_status("hotkey assignment cancelled", DIM)

    def _on_assign_key(self, ev):
        ks = ev.keysym or ""
        if ks == "Escape":
            self._cancel_assign()
            return "break"
        if not ks or ks == "NoSymbol" or ks in BLOCKED_KEYS or ks in MODIFIER_KEYS:
            self._set_status(f"“{pretty_key(ks) or 'this key'}” is not allowed "
                             f"— press a different key (ESC to cancel).", MISS)
            return "break"
        self.assigning = False
        self.root.unbind("<KeyPress>")
        self.cfg["hotkey"] = ks
        core.save_config(self.cfg)
        if self._start_hotkey(ks):
            self._update_hotkey_button()
        return "break"

    def _update_hotkey_button(self):
        ks = self.cfg.get("hotkey") or ""
        if ks:
            self.hotkey_btn.config(
                text=f"Hotkey: {pretty_key(ks)}  ·  click to change")
        else:
            self.hotkey_btn.config(text="Assign hotkey")

    def _start_hotkey(self, keysym):
        """Grab `keysym` globally (replacing any previous hotkey)."""
        self._stop_hotkey()
        if sys.platform.startswith("win"):
            return self._start_hotkey_win(keysym)
        try:
            from Xlib import X, display, XK
        except ImportError:
            self._set_status("python-xlib not installed — cannot grab the "
                             "hotkey", MISS)
            return False
        xk = XK.string_to_keysym(keysym)
        if not xk:
            self._set_status(f"could not map key “{keysym}” — try another key",
                             MISS)
            return False
        d = display.Display()
        try:
            d.set_error_handler(lambda *a: None)
        except Exception:
            pass
        root = d.screen().root
        keycode = d.keysym_to_keycode(xk)
        if not keycode:
            try:
                d.close()
            except Exception:
                pass
            self._set_status(f"could not map “{pretty_key(keysym)}” on this "
                             f"display — try another key", MISS)
            return False
        # grab the plain key plus NumLock/CapsLock state variants, so the
        # hotkey fires regardless of lock toggles but never steals combos
        mods = (0, X.LockMask, X.Mod2Mask, X.LockMask | X.Mod2Mask)
        grabbed = 0
        for mod in mods:
            try:
                root.grab_key(keycode, mod, True,
                              X.GrabModeAsync, X.GrabModeAsync)
                grabbed += 1
            except Exception:
                pass
        if not grabbed:
            try:
                d.close()
            except Exception:
                pass
            self._set_status(f"could not grab {pretty_key(keysym)} — another "
                             f"app owns it?", MISS)
            return False
        d.sync()
        self.hotkey_keysym = keysym
        self.hotkey_on = True
        self._grab_display = d
        self._grab_keycode = keycode
        self._hotkey_thread = threading.Thread(target=self._hotkey_loop,
                                               daemon=True)
        self._hotkey_thread.start()
        self._set_status(f"Hotkey {pretty_key(keysym)} active — open the RUNES "
                         f"tab in D2R and press {pretty_key(keysym)} to scan.",
                         OK)
        return True

    # -- Windows: RegisterHotKey on a dedicated message-loop thread ---------
    def _start_hotkey_win(self, keysym):
        vk = core.win_vk(keysym)
        if vk is None:
            self._set_status(f"key “{pretty_key(keysym)}” is not supported "
                             "on Windows — try another key", MISS)
            return False
        self.hotkey_keysym = keysym
        self.hotkey_on = True
        self._win_hk_result = queue.Queue()
        self._hotkey_thread = threading.Thread(
            target=self._hotkey_loop_win, args=(vk,), daemon=True)
        self._hotkey_thread.start()
        try:
            ok, msg = self._win_hk_result.get(timeout=2)
        except queue.Empty:
            ok, msg = False, "hotkey registration timed out — try another key"
        if not ok:
            self.hotkey_on = False
            self._set_status(msg, MISS)
            return False
        self._set_status(f"Hotkey {pretty_key(keysym)} active — open the RUNES "
                         f"tab in D2R and press {pretty_key(keysym)} to scan.",
                         OK)
        return True

    def _hotkey_loop_win(self, vk):
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        self._win_hk_tid = ctypes.windll.kernel32.GetCurrentThreadId()
        MOD_NOREPEAT, WM_HOTKEY = 0x4000, 0x0312
        hk_id = 0x4442
        if not user32.RegisterHotKey(None, hk_id, MOD_NOREPEAT, vk):
            self._win_hk_result.put(
                (False, f"could not grab “{pretty_key(self.hotkey_keysym)}” "
                        "— another app owns it?"))
            return
        self._win_hk_result.put((True, ""))
        try:
            msg = wintypes.MSG()
            while self.hotkey_on:
                r = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if r <= 0:
                    break
                if msg.message == WM_HOTKEY and msg.wParam == hk_id:
                    self._hotkey_q.put(self.do_scan)
        finally:
            user32.UnregisterHotKey(None, hk_id)

    def _stop_hotkey(self):
        self.hotkey_on = False
        if self._win_hk_tid is not None:
            try:
                import ctypes
                # WM_QUIT wakes the blocking GetMessageW in the hotkey thread
                ctypes.windll.user32.PostThreadMessageW(
                    self._win_hk_tid, 0x0012, 0, 0)
            except Exception:
                pass
            self._win_hk_tid = None
        d = self._grab_display
        self._grab_display = None
        if d is not None:
            try:
                root = d.screen().root
                if self._grab_keycode:
                    for mod in (0, X.LockMask, X.Mod2Mask,
                                X.LockMask | X.Mod2Mask):
                        try:
                            root.ungrab_key(self._grab_keycode, mod)
                        except Exception:
                            pass
            except Exception:
                pass
            try:
                d.close()
            except Exception:
                pass
        self._grab_keycode = None

    def _hotkey_loop(self):
        from Xlib import X
        d = self._grab_display
        while self.hotkey_on and d is not None:
            try:
                ev = d.next_event()
            except Exception:
                if self.hotkey_on:
                    time.sleep(0.05)
                continue
            if ev.type == X.KeyPress and ev.detail == self._grab_keycode:
                self._hotkey_q.put(self.do_scan)


def main():
    ap = argparse.ArgumentParser(description="D2R Companion — runeword finder")
    ap.add_argument("--image", metavar="FILE", help="pre-load a screenshot")
    ap.add_argument("--selftest", metavar="FILE",
                    help="analyze FILE, print a summary and exit — CI smoke "
                         "test, no window needed")
    args = ap.parse_args()
    if args.selftest:
        # headless self-test: exercises numpy/Pillow/tkinter imports and the
        # whole scan engine without needing a display (used by CI)
        cfg = core.load_config()
        res = core.analyze_image(args.selftest, cfg)
        n = len([c for c in core.match_runewords(res["owned"]) if c[6] > 0])
        print(f"D2R Companion selftest OK: {len(res['owned'])} runes, "
              f"{n} craftable runewords")
        return
    root = tk.Tk()
    App(root, preload_image=args.image)
    root.mainloop()


if __name__ == "__main__":
    main()
