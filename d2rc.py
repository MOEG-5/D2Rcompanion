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

Scanning is hotkey-driven: click "Assign hotkey", press a key combination,
and from then on that combination is grabbed globally (always on, remembered
across runs). With the stash open on the RUNES tab in D2R, press the hotkey to
re-scan and bring the results window to the front.
An "Open Image..." button is also provided for analyzing screenshot files.

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
from tkinter import filedialog, font as tkfont, ttk

import d2r_data
import d2r_items
import d2r_runewords as core

# --------------------------------------------------------------------------
# palette / fonts (Diablo 2 Gothic Dark Fantasy Theme)
# --------------------------------------------------------------------------
BG          = "#0f0f14"   # deep gothic abyss background
BG2         = "#16161f"   # secondary container / panels
PANEL       = "#1e1e29"   # buttons / fields / elevated panels
PANEL2      = "#282837"   # hover / scrollbar thumb / active
BORDER      = "#2b2b3a"   # structural borders
BORDER_GOLD = "#5a451e"   # ornamental gothic gold border
BORDER_ACT  = "#8c6e28"   # bright active gold border

FG          = "#cfcbbe"   # body text (warm parchment tint)
FG_BRIGHT   = "#f2f0ea"   # pure bright text
DIM         = "#7a7988"   # muted meta text
GOLD        = "#d4af37"   # classic Diablo 2 gold
GOLD_BRIGHT = "#f6d878"   # radiant gold / highlighted titles
AMBER       = "#e69a28"   # warm rune amber
RUNEC       = "#f0b254"   # runic amber text
BASEC       = "#9fd0a0"   # item base category (pale sage)
SKILLC      = "#cfb3ee"   # magic & skill stats (soft lilac)
MISS        = "#ff5555"   # missing rune warning crimson
SEC         = "#f4f3ed"   # section header text
EFF         = "#c7c4b7"   # stat descriptions
OK          = "#4ade80"   # craftable green
SET_COLOR   = "#00e676"   # classic Diablo 2 set green
UNI_COLOR   = "#d8c384"   # classic Diablo 2 unique gold
RECIPE_COLOR= "#e8a06a"   # cube recipe orange
VERSION     = "v0.1.7"

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
    """Dark gothic ttk theme — custom clam styling with dark borders and muted scrollbars."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=BG)

    # notebook — gothic dark tabs, completely dark client area without light border lines
    style.configure("TNotebook", background=BG, borderwidth=0,
                    tabmargins=(0, 0, 0, 0), darkcolor=BG, lightcolor=BG,
                    bordercolor=BG)
    style.configure("TNotebook.Tab", background=BG2, foreground=DIM,
                    bordercolor=BORDER, lightcolor=BG2, darkcolor=BG2,
                    padding=(20, 8), borderwidth=0, relief="flat", focuscolor=BG)
    style.map("TNotebook.Tab",
              background=[("selected", PANEL), ("active", "#252533")],
              foreground=[("selected", GOLD_BRIGHT), ("active", FG_BRIGHT)],
              bordercolor=[("selected", BORDER_GOLD), ("active", BORDER)],
              lightcolor=[("selected", BORDER_GOLD), ("active", BORDER)],
              darkcolor=[("selected", BORDER_GOLD), ("active", BORDER)],
              padding=[("selected", (20, 8)), ("active", (20, 8))])

    # buttons — dark gothic slate with amber/gold borders, zero white highlights
    style.configure("TButton", background=PANEL, foreground=FG,
                    bordercolor=BORDER_GOLD, lightcolor=PANEL, darkcolor=PANEL,
                    focuscolor=PANEL, focusthickness=0, padding=(12, 6),
                    relief="flat")
    style.map("TButton",
              background=[("pressed", "#14141c"), ("active", PANEL2)],
              foreground=[("pressed", GOLD), ("active", GOLD_BRIGHT)],
              bordercolor=[("pressed", BORDER_GOLD), ("active", BORDER_ACT)],
              lightcolor=[("pressed", PANEL), ("active", PANEL2)],
              darkcolor=[("pressed", PANEL), ("active", PANEL2)])

    # search entry — dark background, gold border on focus
    style.configure("TEntry", fieldbackground=PANEL, foreground=FG_BRIGHT,
                    insertcolor=GOLD_BRIGHT, bordercolor=BORDER,
                    lightcolor=BORDER, darkcolor=BORDER, padding=(8, 6))
    style.map("TEntry",
              bordercolor=[("focus", BORDER_ACT)],
              lightcolor=[("focus", BORDER_ACT)],
              darkcolor=[("focus", BORDER_ACT)])

    # scrollbars — clean flat dark bar with gold active indicator and no white grip lines
    style.configure("Vertical.TScrollbar", background=PANEL,
                    troughcolor=BG, bordercolor=BG, lightcolor=BG, darkcolor=BG,
                    arrowcolor=BORDER_GOLD, arrowsize=11, gripcount=0,
                    relief="flat", width=12)
    style.map("Vertical.TScrollbar",
              background=[("pressed", BORDER_GOLD), ("active", PANEL2)],
              arrowcolor=[("pressed", GOLD), ("active", GOLD_BRIGHT)],
              lightcolor=[("active", BG), ("pressed", BG)],
              darkcolor=[("active", BG), ("pressed", BG)],
              bordercolor=[("active", BG), ("pressed", BG)])


def pretty_key(keysym):
    """Human-friendly label for a keysym or a persisted hotkey string."""
    if "+" in keysym:
        mods, key = core.parse_hotkey(keysym)
        ordered_mods = [name for name in ("Ctrl", "Alt", "Shift", "Win")
                        if name in mods]
        return "+".join(ordered_mods + [pretty_key(key)])
    if keysym == "space":
        return "Space"
    if len(keysym) == 1:
        return keysym.upper()
    return keysym


class App:
    def __init__(self, root, preload_image=None):
        self.root = root
        root.title("D2R Companion — runeword finder")
        root.geometry("1120x800")
        root.minsize(860, 560)
        root.configure(bg=BG)

        # set window icon if available
        ico_path = os.path.join(_HERE, "d2r.ico")
        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception:
                pass

        self.cfg = core.load_config()
        self.owned = None          # last scan: rune -> count
        self.last_scan_info = None

        # hotkey state
        self.hotkey_keysym = ""
        self.hotkey_on = False
        self.assigning = False
        self._grab_display = None
        self._grab_keycode = None
        self._grab_modmask = 0
        self._win_hk_tid = None          # Windows RegisterHotKey thread id
        self._win_hk_result = None       # Windows registration result queue
        self._hotkey_thread = None
        self._hotkey_q = queue.Queue()   # hotkey thread -> main thread

        self._fonts()
        _setup_style()
        self._build_ui()
        self._refresh_timer = None
        self._poll_timer = None

        # always-on hotkey (persisted in the config); first run = unassigned
        self._update_hotkey_button()
        if self.cfg.get("hotkey"):
            self._start_hotkey(self.cfg["hotkey"])
        else:
            self._set_status("No hotkey assigned yet — click “Assign hotkey” "
                             "to choose your scan key.", DIM)

        # drain hotkey events on the main thread (queue is thread-safe)
        self._poll_timer = self.root.after(150, self._poll_hotkey_events)

        if preload_image:
            self.do_scan(file=preload_image)

    # ------------------------------------------------------------------
    def _fonts(self):
        families = [
            "Segoe UI", "Inter", "Ubuntu", "DejaVu Sans", "Adwaita Sans",
            "Cantarell", "Helvetica", "Arial"
        ]
        avail = set(tkfont.families(self.root))
        chosen = next((f for f in families if f in avail), None)
        if not chosen:
            chosen = tkfont.nametofont("TkDefaultFont").actual("family")

        self.f_title = tkfont.Font(family=chosen, size=12, weight="bold")
        self.f_sec   = tkfont.Font(family=chosen, size=11, weight="bold")
        self.f_name  = tkfont.Font(family=chosen, size=11, weight="bold")
        self.f_bold  = tkfont.Font(family=chosen, size=10, weight="bold")
        self.f_base  = tkfont.Font(family=chosen, size=10)
        self.f_small = tkfont.Font(family=chosen, size=9)
        self.f_tiny  = tkfont.Font(family=chosen, size=8)

    # ------------------------------------------------------------------
    def _build_ui(self):
        # 1. Top Header bar: Title + Search with live count + Action buttons
        header_outer = tk.Frame(self.root, bg=BG2, highlightbackground=BORDER,
                                highlightthickness=1)
        header_outer.pack(fill="x", padx=10, pady=(8, 4))

        header = tk.Frame(header_outer, bg=BG2)
        header.pack(fill="x", padx=12, pady=8)

        # Brand title & version
        brand_frame = tk.Frame(header, bg=BG2)
        brand_frame.pack(side="left")
        tk.Label(brand_frame, text="⚔  D2R COMPANION", font=self.f_title,
                 fg=GOLD_BRIGHT, bg=BG2).pack(side="left")
        tk.Label(brand_frame, text=f" {VERSION} ", font=self.f_tiny,
                 fg=DIM, bg=PANEL, padx=4, pady=1).pack(side="left", padx=(8, 0))

        # Search bar in center
        search_wrap = tk.Frame(header, bg=BG2)
        search_wrap.pack(side="left", fill="x", expand=True, padx=(20, 16))

        search_box = tk.Frame(search_wrap, bg=PANEL, highlightbackground=BORDER,
                              highlightthickness=1)
        search_box.pack(side="left", fill="x", expand=True)

        tk.Label(search_box, text=" 🔍 ", font=self.f_small, fg=DIM,
                 bg=PANEL).pack(side="left", padx=(4, 0))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        self.search_entry = tk.Entry(
            search_box, textvariable=self.search_var, bg=PANEL, fg=FG_BRIGHT,
            insertbackground=GOLD_BRIGHT, relief="flat", font=self.f_base,
            highlightthickness=0, borderwidth=0)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=4, pady=5)

        # Match count badge
        self.search_count_lbl = tk.Label(search_box, text="", font=self.f_small,
                                         fg=DIM, bg=PANEL)
        self.search_count_lbl.pack(side="left", padx=4)

        # Clear search button
        self.search_clear_btn = tk.Label(search_box, text=" ✕ ", font=self.f_small,
                                         fg=DIM, bg=PANEL, cursor="hand2")
        self.search_clear_btn.bind("<Button-1>", lambda e: self._clear_search())
        self.search_clear_btn.bind("<Enter>", lambda e: self.search_clear_btn.config(fg=GOLD_BRIGHT))
        self.search_clear_btn.bind("<Leave>", lambda e: self.search_clear_btn.config(fg=DIM))
        self.search_clear_btn.pack(side="left", padx=(0, 4))
        self.search_clear_btn.pack_forget()

        # Action buttons on right (Open Image and Hotkey)
        actions = tk.Frame(header, bg=BG2)
        actions.pack(side="right")

        self.open_btn = ttk.Button(actions, text="📁 Open Image…",
                                   style="TButton",
                                   command=self._open_image_dialog)
        self.open_btn.pack(side="left", padx=(0, 8))

        self.hotkey_btn = ttk.Button(actions, style="TButton",
                                     command=self._assign_hotkey)
        self.hotkey_btn.pack(side="left")

        # 2. Notebook tabs
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=10, pady=(2, 4))

        self.tab_mine = ttk.Frame(self.nb)
        self.tab_all  = ttk.Frame(self.nb)
        self.tab_cube = ttk.Frame(self.nb)
        self.tab_uni  = ttk.Frame(self.nb)
        self.tab_set  = ttk.Frame(self.nb)

        self.nb.add(self.tab_mine, text="  ⚔ My runes  ")
        self.nb.add(self.tab_all,  text="  📜 All runewords  ")
        self.nb.add(self.tab_cube, text="  ⚗ Cube recipes  ")
        self.nb.add(self.tab_uni,  text="  ✨ Unique items  ")
        self.nb.add(self.tab_set,  text="  🛡 Set items  ")
        self.nb.bind("<<NotebookTabChanged>>", lambda e: self.refresh())

        # 3. Visual Rune Stash Bar inside "My runes" tab
        self._build_stash_bar()

        # 4. Text areas for each tab
        self.txt_mine, self.wrap_mine = self._make_text(self.tab_mine)
        self.txt_all,  self.wrap_all  = self._make_text(self.tab_all)
        self.txt_cube, self.wrap_cube = self._make_text(self.tab_cube)
        self.txt_uni,  self.wrap_uni  = self._make_text(self.tab_uni)
        self.txt_set,  self.wrap_set  = self._make_text(self.tab_set)
        self._tag_configure_all()

        # 5. Footer status bar
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")
        footer = tk.Frame(self.root, bg=BG2)
        footer.pack(fill="x", padx=12, pady=(5, 6))

        self.status = tk.Label(footer, text="", font=self.f_small, fg=DIM,
                               bg=BG2, anchor="w")
        self.status.pack(side="left", fill="x", expand=True)

        meta_stats = (f"D2R v3.x RotW · {len(d2r_data.RUNEWORDS)} Runewords · "
                      f"{len(d2r_data.RECIPES)} Recipes · "
                      f"{len(d2r_items.UNIQUES)} Uniques · "
                      f"{len(d2r_items.SETS)} Sets")
        tk.Label(footer, text=meta_stats, font=self.f_tiny, fg=DIM,
                 bg=BG2).pack(side="right")

        self.n_uni = len(d2r_items.UNIQUES)
        self.n_set = len(d2r_items.SETS)
        n_set_items = sum(len(s['items']) for s in d2r_items.SETS)
        self._set_status(
            f"Ready — open the RUNES tab in D2R and press your scan hotkey (or click “Open Image…”).")

    # ------------------------------------------------------------------
    # Visual Rune Stash Bar
    # ------------------------------------------------------------------
    def _build_stash_bar(self):
        self.stash_frame = tk.Frame(self.tab_mine, bg=BG2,
                                    highlightbackground=BORDER_GOLD,
                                    highlightthickness=1)
        # Top banner of stash frame
        self.stash_top = tk.Frame(self.stash_frame, bg=BG2)
        self.stash_top.pack(fill="x", padx=10, pady=(6, 4))

        tk.Label(self.stash_top, text="◆  DETECTED RUNE STASH",
                 font=self.f_sec, fg=GOLD_BRIGHT, bg=BG2).pack(side="left")

        self.stash_summary_lbl = tk.Label(self.stash_top, text="",
                                          font=self.f_small, fg=FG, bg=BG2)
        self.stash_summary_lbl.pack(side="left", padx=12)

        self.stash_hint_lbl = tk.Label(
            self.stash_top,
            text="Click any rune to filter runewords  ·  Click again to clear",
            font=self.f_tiny, fg=DIM, bg=BG2)
        self.stash_hint_lbl.pack(side="right")

        # Container where rune chips are rendered
        self.stash_chips_box = tk.Frame(self.stash_frame, bg=BG2)
        self.stash_chips_box.pack(fill="x", padx=10, pady=(0, 6))

    def _update_stash_bar(self):
        """Update the visual rune stash bar with chips for owned runes."""
        if not self.owned:
            self.stash_frame.pack_forget()
            return

        # Ensure stash frame is visible at the top of tab_mine
        self.stash_frame.pack(fill="x", side="top", padx=6, pady=(4, 6),
                              before=self.wrap_mine)

        # Clear existing chip widgets
        for child in self.stash_chips_box.winfo_children():
            child.destroy()

        owned = self.owned
        total_runes = sum(owned.values())
        unique_runes = len(owned)

        craft_count = len([rw for rw in d2r_data.RUNEWORDS
                           if all(owned.get(r, 0) >= 1 for r in rw[1])])
        near_count = len([rw for rw in d2r_data.RUNEWORDS
                          if not all(owned.get(r, 0) >= 1 for r in rw[1])
                          and sum(1 for r in rw[1] if owned.get(r, 0) < 1) == 1])

        self.stash_summary_lbl.config(
            text=f"{unique_runes} runes ({total_runes} total)  ·  "
                 f"● {craft_count} craftable  ·  ▲ {near_count} one rune short")

        # Tiers of runes: High (Mal..Zod), Mid (Sol..Um), Low (El..Amn)
        tiers = [
            ("HIGH", [r for r in d2r_data.RUNES[22:] if r in owned],
             "#7d6124", "#f6c855", "#221c15", "#382c18"),
            ("MID",  [r for r in d2r_data.RUNES[11:22] if r in owned],
             "#344a63", "#8ec5fc", "#17212c", "#223142"),
            ("LOW",  [r for r in d2r_data.RUNES[:11] if r in owned],
             "#4a3a2a", "#e0aa75", "#1f1a16", "#2e251e"),
        ]

        active_filter = self.search_var.get().strip().lower()

        for tier_tag, runes_in_tier, border_c, name_c, chip_bg, hover_bg in tiers:
            if not runes_in_tier:
                continue

            # Break into rows of max 10 chips so it wraps nicely
            chunk_size = 10
            for i in range(0, len(runes_in_tier), chunk_size):
                chunk = runes_in_tier[i:i + chunk_size]
                row = tk.Frame(self.stash_chips_box, bg=BG2)
                row.pack(fill="x", pady=2)

                # Tier label for the first chunk
                prefix_text = f"[{tier_tag}]" if i == 0 else "      "
                tag_lbl = tk.Label(row, text=prefix_text, font=self.f_tiny,
                                   fg=name_c, bg="#101016", width=8,
                                   anchor="center", padx=2, pady=1)
                tag_lbl.pack(side="left", padx=(0, 6))

                for r_name in chunk:
                    cnt = owned[r_name]
                    is_active = (active_filter == r_name.lower())

                    cur_border = BORDER_ACT if is_active else border_c
                    cur_bg = hover_bg if is_active else chip_bg

                    chip = tk.Frame(row, bg=cur_bg,
                                    highlightbackground=cur_border,
                                    highlightthickness=1, cursor="hand2")
                    chip.pack(side="left", padx=2)

                    lbl_r = tk.Label(chip, text=r_name, font=self.f_bold,
                                     fg=GOLD_BRIGHT if is_active else name_c,
                                     bg=cur_bg)
                    lbl_r.pack(side="left", padx=(6, 2), pady=1)

                    badge = tk.Label(chip, text=f"×{cnt}", font=self.f_tiny,
                                     fg=FG_BRIGHT, bg="#0c0c10", padx=3, pady=0)
                    badge.pack(side="left", padx=(2, 4), pady=1)

                    # Click and hover events
                    def _make_click(name=r_name):
                        return lambda e: self._on_rune_chip_click(name)

                    def _make_enter(w_chip, w_lbl, h_bg, b_act):
                        return lambda e: (w_chip.config(bg=h_bg, highlightbackground=b_act),
                                          w_lbl.config(bg=h_bg))

                    def _make_leave(w_chip, w_lbl, orig_bg, orig_b):
                        return lambda e: (w_chip.config(bg=orig_bg, highlightbackground=orig_b),
                                          w_lbl.config(bg=orig_bg))

                    click_handler = _make_click(r_name)
                    enter_handler = _make_enter(chip, lbl_r, hover_bg, BORDER_ACT)
                    leave_handler = _make_leave(chip, lbl_r, cur_bg, cur_border)

                    for widget in (chip, lbl_r, badge):
                        widget.bind("<Button-1>", click_handler)
                        widget.bind("<Enter>", enter_handler)
                        widget.bind("<Leave>", leave_handler)

    def _on_rune_chip_click(self, r_name):
        """Clicking a rune chip filters by that rune, or clears if already filtered."""
        current = self.search_var.get().strip()
        if current.lower() == r_name.lower():
            self._clear_search()
        else:
            self.search_var.set(r_name)

    def _clear_search(self):
        self.search_var.set("")
        self.search_entry.focus_set()

    def _open_image_dialog(self):
        try:
            fn = filedialog.askopenfilename(
                title="Select D2R Rune Stash Screenshot",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"),
                    ("All files", "*.*")
                ]
            )
            if fn:
                self.do_scan(file=fn)
        except Exception as e:
            self._set_status(f"Error opening image: {e}", MISS)

    # ------------------------------------------------------------------
    def _make_text(self, parent):
        wrap = tk.Frame(parent, bg=BG)
        wrap.pack(fill="both", expand=True, padx=4, pady=(2, 4))
        txt = tk.Text(wrap, bg=BG, fg=FG, insertbackground=GOLD_BRIGHT,
                      relief="flat", wrap="word", font=self.f_base,
                      padx=16, pady=12, highlightthickness=0, borderwidth=0,
                      cursor="arrow")
        sb = ttk.Scrollbar(wrap, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)
        txt.configure(state="disabled")
        return txt, wrap

    def _tag_configure_all(self):
        for txt in (self.txt_mine, self.txt_all, self.txt_cube,
                    self.txt_uni, self.txt_set):
            txt.tag_configure("name", font=self.f_name, foreground=GOLD_BRIGHT)
            txt.tag_configure("icon", font=self.f_bold, foreground=GOLD)
            txt.tag_configure("runes", font=self.f_bold, foreground=RUNEC)
            txt.tag_configure("rune_sep", font=self.f_small, foreground=DIM)
            txt.tag_configure("base", font=self.f_bold, foreground=BASEC)
            txt.tag_configure("skill", font=self.f_base, foreground=SKILLC)
            txt.tag_configure("miss", font=self.f_bold, foreground=MISS)
            txt.tag_configure("miss_label", font=self.f_bold, foreground=MISS)
            txt.tag_configure("sec", font=self.f_sec, foreground=GOLD)
            txt.tag_configure("dim", font=self.f_small, foreground=DIM)
            txt.tag_configure("ok", font=self.f_bold, foreground=OK)
            txt.tag_configure("eff", font=self.f_base, foreground=EFF)
            txt.tag_configure("label", font=self.f_small, foreground=DIM)
            txt.tag_configure("sub_label", font=self.f_small, foreground=GOLD)
            txt.tag_configure("meta", font=self.f_small, foreground=DIM)
            txt.tag_configure("div", font=self.f_small, foreground=BORDER)
            txt.tag_configure("head_craft", font=self.f_sec, foreground=OK)
            txt.tag_configure("head_craft_div", font=self.f_small, foreground="#2a4a30")
            txt.tag_configure("head_near", font=self.f_sec, foreground="#f59e0b")
            txt.tag_configure("head_near_div", font=self.f_small, foreground="#4a3820")
            txt.tag_configure("welcome_head", font=self.f_title, foreground=GOLD_BRIGHT)
            txt.tag_configure("welcome_sub", font=self.f_name, foreground=GOLD)
            txt.tag_configure("rec_title", font=self.f_name, foreground=RECIPE_COLOR)
            txt.tag_configure("uni_name", font=self.f_name, foreground=UNI_COLOR)
            txt.tag_configure("set_name", font=self.f_name, foreground=SET_COLOR)
            txt.tag_configure("amber", font=self.f_bold, foreground="#f59e0b")
            for cat, col in CAT_COLORS.items():
                txt.tag_configure("cat:" + cat, font=self.f_small, foreground=col)

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
        try:
            if self.root.winfo_exists():
                self._poll_timer = self.root.after(150, self._poll_hotkey_events)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def _set_status(self, text, color=None):
        try:
            if self.status.winfo_exists():
                self.status.config(text=text, fg=color or DIM)
        except Exception:
            pass

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
    # content card builders (Gothic card layouts)
    # ------------------------------------------------------------------
    def _rw_card(self, seg, rw, missing=None):
        name, runes, socks, types, req, patch, mods = rw
        seg.append(("  ✦ ", "icon"))
        seg.append((name.upper(), "name"))
        meta = f"   [ Req Lvl {req if req else '—'}  ·  ⬡ {socks} Socket{'s' if socks != 1 else ''}"
        if patch:
            meta += f"  ·  v{patch}"
        meta += " ]"
        seg.append((meta + "\n", "meta"))

        # Runes with diamond separators
        seg.append(("     RUNES:    ", "label"))
        for i, r in enumerate(runes):
            if i > 0:
                seg.append(("  ◈  ", "rune_sep"))
            if missing and r in missing:
                seg.append((f"[ {r} ]", "miss"))
            else:
                seg.append((r, "runes"))
        seg.append(("\n", None))

        if missing:
            seg.append(("     ⚠ MISSING: ", "miss_label"))
            seg.append((f"{', '.join(missing)} (need 1 more)\n", "miss"))

        seg.append(("     BASES:    ", "label"))
        seg.append((f"{', '.join(types)}\n", "base"))

        if mods:
            seg.append(("     PROPERTIES:\n", "label"))
            if len(mods) == 1:
                for line in mods[0]:
                    seg.append((f"       • {line}\n", "eff"))
            else:
                for i, lines in enumerate(mods):
                    tname = types[i] if i < len(types) else f"variant {i+1}"
                    seg.append((f"       ({tname}):\n", "sub_label"))
                    for line in lines:
                        seg.append((f"         • {line}\n", "eff"))
        seg.append(("  " + "─" * 72 + "\n\n", "div"))

    def _rec_card(self, seg, rec):
        title, cat, ingredients, output = rec
        seg.append(("  ✦ ", "icon"))
        seg.append((title, "rec_title"))
        seg.append((f"   [ {cat} ]\n", "cat:" + cat))

        ing = " + ".join(f"{q} {n}" if q != 1 else n for q, n in ingredients)
        out = " + ".join(f"{q} {n}" if q != 1 else n for q, n in output)
        seg.append(("     FORMULA:  ", "label"))
        seg.append((f"{ing}\n", "eff"))
        seg.append(("     OUTPUT:   ", "label"))
        seg.append((f"➔ {out}\n", "ok"))

        rolls = d2r_data.CRAFT_ROLLS.get(title)
        if rolls:
            seg.append(("     ALWAYS ROLLS:\n", "label"))
            for line in rolls:
                seg.append((f"       • {line}\n", "eff"))
            seg.append(("     NOTES:\n", "label"))
            seg.append(("       • Plus 1-4 random affixes (magic/rare pool — more at higher ilvl)\n", "dim"))
        seg.append(("  " + "─" * 72 + "\n\n", "div"))

    def _item_card(self, seg, it):
        name, category, base, quality, small, mods, patch = it
        meta_parts = [x for x in (base, quality) if x]
        if patch:
            meta_parts.append(f"v{patch}")
        meta = "  ·  ".join(meta_parts)

        seg.append(("  ✦ ", "icon"))
        seg.append((name, "uni_name"))
        if meta:
            seg.append((f"   [ {meta} ]\n", "meta"))
        else:
            seg.append(("\n", None))

        if small:
            seg.append(("     BASE STATS: ", "label"))
            seg.append((f"{'  |  '.join(small)}\n", "eff"))

        if mods:
            seg.append(("     PROPERTIES:\n", "label"))
            for line in mods:
                seg.append((f"       • {line}\n", "skill"))
        seg.append(("  " + "─" * 72 + "\n\n", "div"))

    def _set_card(self, seg, s):
        name = s['name']
        meta = f"v{s['patch']}" if s.get('patch') else ""
        seg.append(("  ✦ ", "icon"))
        seg.append((name.upper(), "set_name"))
        info = f"{len(s['items'])} pieces"
        if meta:
            info += f"  ·  {meta}"
        seg.append((f"   [ {info} ]\n", "meta"))

        seg.append(("     SET PIECES:\n", "label"))
        for it in s['items']:
            seg.append((f"       • {it[0]}", "runes"))
            seg.append((f"   [ {it[1]} ]\n", "base"))
            if len(it) > 2 and it[2]:
                seg.append((f"           {'  |  '.join(it[2])}\n", "dim"))
            if len(it) > 3 and it[3]:
                for line in it[3]:
                    seg.append((f"           {line}\n", "eff"))

        if s['partial']:
            seg.append(("     PARTIAL SET BONUSES:\n", "ok"))
            for count, mods in s['partial']:
                seg.append((f"       ({count} items equipped):\n", "base"))
                for m in mods:
                    seg.append((f"         • {m}\n", "eff"))

        if s['full']:
            seg.append(("     COMPLETE SET BONUS:\n", "ok"))
            for m in s['full']:
                seg.append((f"       • {m}\n", "eff"))
        seg.append(("  " + "─" * 72 + "\n\n", "div"))

    # ------------------------------------------------------------------
    # data views
    # ------------------------------------------------------------------
    def _view_mine(self, seg, q):
        if self.owned is None:
            # Gothic welcome hero banner
            seg.append(("\n", None))
            seg.append(("     ⚔  DIABLO II: RESURRECTED — RUNE STASH COMPANION  ⚔\n\n", "welcome_head"))
            seg.append(("     Quick Start Guide:\n\n", "welcome_sub"))
            seg.append(("     1. In Diablo 2: Resurrected, open your stash on the RUNES tab.\n", "eff"))
            seg.append(("     2. Press your assigned scan hotkey (see top right) while in-game.\n", "eff"))
            seg.append(("     3. The companion scans your rune stash and instantly displays:\n", "eff"))
            seg.append(("        • Craftable Runewords — runewords you can make right now\n", "ok"))
            seg.append(("        • One Rune Short — runewords missing only 1 rune to complete\n", "amber"))
            seg.append(("        • Visual Rune Stash — inventory summary of all detected runes\n\n", "runes"))
            seg.append(("     You can also click [📁 Open Image…] to analyze an existing screenshot,\n", "dim"))
            seg.append(("     or browse the tabs above for All Runewords, Cube Recipes, Uniques, and Sets.\n", "dim"))
            return

        owned = self.owned
        if not owned:
            seg.append(("\n  (No runes detected in stash screenshot — verify stash is on RUNES tab)\n\n", "dim"))
            return

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

        seg.append((f"  ⚔  CRAFTABLE RUNEWORDS ({len(craft)})\n", "head_craft"))
        seg.append(("  " + "═" * 72 + "\n\n", "head_craft_div"))
        if not craft:
            seg.append(("    (No craftable runewords with current runes — collect more runes!)\n\n", "dim"))
        for rw in craft:
            self._rw_card(seg, rw)

        seg.append((f"\n  ⚠  ONE RUNE SHORT ({len(near)})\n", "head_near"))
        seg.append(("  " + "═" * 72 + "\n\n", "head_near_div"))
        if not near:
            seg.append(("    (None)\n\n", "dim"))
        for rw in near:
            missing = [r for r in rw[1] if owned.get(r, 0) < 1]
            self._rw_card(seg, rw, missing=missing)

        seg.append(("  Note: Runewords require their runes inserted in the exact order shown!\n",
                    "dim"))

    def _view_all(self, seg, q):
        rws = sorted(d2r_data.RUNEWORDS, key=lambda r: (r[4] or 0, r[0]))
        if q:
            rws = [rw for rw in rws if self._rw_matches(rw, q)]
        if not rws:
            seg.append(("\n  (No runewords match your search query)\n", "dim"))
            return
        last_lvl = None
        for rw in rws:
            lvl = rw[4] or 0
            if lvl != last_lvl:
                seg.append((f"\n  ═══════════════ ◆ REQUIRED LEVEL {lvl} ◆ ═══════════════\n\n", "sec"))
                last_lvl = lvl
            self._rw_card(seg, rw)

    def _view_cube(self, seg, q):
        recs = d2r_data.RECIPES
        if q:
            recs = [r for r in recs if self._rec_matches(r, q)]
        if not recs:
            seg.append(("\n  (No cube recipes match your search query)\n", "dim"))
            return
        cats = [c for c in CAT_COLORS]
        for cat in cats:
            group = [r for r in recs if r[1] == cat]
            if not group:
                continue
            seg.append((f"\n  ═══════════════ ◆ {cat.upper()} ({len(group)}) ◆ ═══════════════\n\n", "cat:" + cat))
            for rec in group:
                self._rec_card(seg, rec)

    def _view_uniques(self, seg, q):
        items = d2r_items.UNIQUES
        if q:
            items = [i for i in items if self._item_matches(i, q)]
        if not items:
            seg.append(("\n  (No unique items match your search query)\n", "dim"))
            return
        last = None
        for it in items:
            if it[1] != last:
                seg.append((f"\n  ═══════════════ ◆ {it[1].upper()} ◆ ═══════════════\n\n", "sec"))
                last = it[1]
            self._item_card(seg, it)

    def _view_sets(self, seg, q):
        sets = d2r_items.SETS
        if q:
            sets = [s for s in sets if self._set_matches(s, q)]
        if not sets:
            seg.append(("\n  (No set items match your search query)\n", "dim"))
            return
        for s in sets:
            self._set_card(seg, s)

    @staticmethod
    def _item_matches(it, q):
        name, cat, base, qual, small, mods, patch = it
        hay = " ".join([name, cat, base, qual, patch or ""] + small + mods)
        return q in hay.lower()

    @staticmethod
    def _set_matches(s, q):
        hay = " ".join([s['name'], s.get('patch') or ""])
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
            try:
                self.root.after_cancel(self._refresh_timer)
            except Exception:
                pass
        try:
            if self.root.winfo_exists():
                self._refresh_timer = self.root.after(120, self.refresh)
        except Exception:
            pass

    def refresh(self, *_):
        try:
            if not self.root.winfo_exists():
                return
        except Exception:
            return

        q = self.search_var.get().strip().lower()

        # Update clear button visibility
        if q:
            self.search_clear_btn.pack(side="left", padx=(0, 4))
        else:
            self.search_clear_btn.pack_forget()

        # Refresh stash chips active highlight
        self._update_stash_bar()

        tab = self.nb.index(self.nb.select())
        match_count = 0

        if tab == 0:
            seg = []
            self._view_mine(seg, q)
            self._set_text(self.txt_mine, seg)
            if self.owned:
                craft_n = len([rw for rw in d2r_data.RUNEWORDS
                               if self._rw_matches(rw, q)
                               and all(self.owned.get(r, 0) >= 1 for r in rw[1])])
                near_n = len([rw for rw in d2r_data.RUNEWORDS
                              if self._rw_matches(rw, q)
                              and not all(self.owned.get(r, 0) >= 1 for r in rw[1])
                              and sum(1 for r in rw[1] if self.owned.get(r, 0) < 1) == 1])
                match_count = craft_n + near_n
                self.nb.tab(self.tab_mine, text=f"  ⚔ My runes ({craft_n})  ")
            else:
                self.nb.tab(self.tab_mine, text="  ⚔ My runes  ")
        elif tab == 1:
            seg = []
            self._view_all(seg, q)
            self._set_text(self.txt_all, seg)
            match_count = len([rw for rw in d2r_data.RUNEWORDS if self._rw_matches(rw, q)]) if q else len(d2r_data.RUNEWORDS)
        elif tab == 2:
            seg = []
            self._view_cube(seg, q)
            self._set_text(self.txt_cube, seg)
            match_count = len([r for r in d2r_data.RECIPES if self._rec_matches(r, q)]) if q else len(d2r_data.RECIPES)
        elif tab == 3:
            seg = []
            self._view_uniques(seg, q)
            self._set_text(self.txt_uni, seg)
            match_count = len([i for i in d2r_items.UNIQUES if self._item_matches(i, q)]) if q else len(d2r_items.UNIQUES)
        else:
            seg = []
            self._view_sets(seg, q)
            self._set_text(self.txt_set, seg)
            match_count = len([s for s in d2r_items.SETS if self._set_matches(s, q)]) if q else len(d2r_items.SETS)

        # Update search match counter badge
        if q:
            if match_count == 0:
                self.search_count_lbl.config(text="0 matches", fg=MISS)
            else:
                self.search_count_lbl.config(text=f"{match_count} matches", fg=GOLD)
        else:
            self.search_count_lbl.config(text=f"{match_count} total", fg=DIM)

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
                    f"Scan OK — {n} craftable runewords detected "
                    f"({len(res['owned'])} runes, from {src})", OK)
            self.nb.select(0)
            self.refresh()
            if file is None:
                self._bring_to_front()
        except Exception as e:
            self._set_status(f"Scan failed: {e}", MISS)
            self.root.bell()

    def _bring_to_front(self):
        """Raise the results after a global hotkey scan, including when minimized."""
        try:
            self.root.deiconify()
            self.root.update_idletasks()
            # A short topmost interval reliably raises the window on both
            # Windows and X11 without changing the app's normal z-order.
            self.root.attributes("-topmost", True)
            self.root.lift()
            self.root.focus_force()
            self.root.after(400, self._clear_temporary_topmost)
        except (tk.TclError, RuntimeError):
            # Some window managers reject focus/topmost requests.  The scan
            # result is still valid and the ordinary lift is best effort.
            try:
                self.root.lift()
            except tk.TclError:
                pass

    def _clear_temporary_topmost(self):
        try:
            if self.root.winfo_exists():
                self.root.attributes("-topmost", False)
        except (tk.TclError, RuntimeError):
            pass

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
        self._set_status("Press a key or combination (for example Ctrl+J) — "
                         "ESC to cancel. Enter/Tab/Space and modifier-only "
                         "keys are not allowed.", GOLD)

    def _cancel_assign(self):
        self.assigning = False
        self.root.unbind("<KeyPress>")
        self._update_hotkey_button()
        self._set_status("Hotkey assignment cancelled", DIM)

    def _on_assign_key(self, ev):
        ks = ev.keysym or ""
        if ks == "Escape":
            self._cancel_assign()
            return "break"
        if ks in MODIFIER_KEYS:
            held = self._event_modifiers(ev)
            if held:
                self._set_status(f"{'+'.join(held)} held — press the key to pair "
                                 "with it (ESC to cancel).", GOLD)
            return "break"
        if not ks or ks == "NoSymbol" or ks in BLOCKED_KEYS:
            self._set_status(f"“{pretty_key(ks) or 'this key'}” is not allowed "
                             f"— press a different key (ESC to cancel).", MISS)
            return "break"
        mods = self._event_modifiers(ev)
        hotkey = "+".join(mods + [ks])
        previous = self.cfg.get("hotkey") or ""
        self.assigning = False
        self.root.unbind("<KeyPress>")
        if self._start_hotkey(hotkey):
            self.cfg["hotkey"] = hotkey
            core.save_config(self.cfg)
            self._update_hotkey_button()
        else:
            # Keep a previously working binding if the new combination is
            # unsupported or already owned by another application.
            self.cfg["hotkey"] = previous
            self._update_hotkey_button()
            if previous:
                self._start_hotkey(previous)
        return "break"

    @staticmethod
    def _event_modifiers(ev):
        """Return pressed modifiers in the canonical order used in config."""
        state = getattr(ev, "state", 0) or 0
        # Tk uses the X11-compatible modifier state bits on both supported
        # platforms: Shift=1, Control=4, Alt/Mod1=8, Win/Mod4=64.
        return [name for mask, name in (
            (0x0004, "Ctrl"), (0x0008, "Alt"),
            (0x0001, "Shift"), (0x0040, "Win"),
        ) if state & mask]

    def _update_hotkey_button(self):
        ks = self.cfg.get("hotkey") or ""
        if ks:
            self.hotkey_btn.config(
                text=f"⌨ Hotkey: {pretty_key(ks)}")
        else:
            self.hotkey_btn.config(text="⌨ Assign hotkey")

    def _start_hotkey(self, hotkey):
        """Grab `hotkey` globally (replacing any previous hotkey)."""
        self._stop_hotkey()
        if sys.platform.startswith("win"):
            return self._start_hotkey_win(hotkey)
        try:
            from Xlib import X, display
        except ImportError:
            self._set_status("python-xlib not installed — cannot grab the "
                             "hotkey", MISS)
            return False
        d = display.Display()
        try:
            d.set_error_handler(lambda *a: None)
        except Exception:
            pass
        root = d.screen().root
        keycode, base_modmask = core.hotkey_to_xlib(hotkey, d)
        if not keycode:
            try:
                d.close()
            except Exception:
                pass
            self._set_status(f"could not map “{pretty_key(hotkey)}” on this "
                             f"display — try another key", MISS)
            return False
        # Grab the requested combination plus NumLock/CapsLock state
        # variants, without grabbing the unmodified key by accident.
        lock_masks = (0, X.LockMask, X.Mod2Mask,
                      X.LockMask | X.Mod2Mask)
        grabbed = 0
        for lock_mask in lock_masks:
            try:
                root.grab_key(keycode, base_modmask | lock_mask, True,
                              X.GrabModeAsync, X.GrabModeAsync)
                grabbed += 1
            except Exception:
                pass
        if not grabbed:
            try:
                d.close()
            except Exception:
                pass
            self._set_status(f"could not grab {pretty_key(hotkey)} — another "
                             f"app owns it?", MISS)
            return False
        d.sync()
        self.hotkey_keysym = hotkey
        self.hotkey_on = True
        self._grab_display = d
        self._grab_keycode = keycode
        self._grab_modmask = base_modmask
        self._hotkey_thread = threading.Thread(target=self._hotkey_loop,
                                               daemon=True)
        self._hotkey_thread.start()
        self._set_status(f"Hotkey {pretty_key(hotkey)} active — open the RUNES "
                         f"tab in D2R and press {pretty_key(hotkey)} to scan.",
                         OK)
        return True

    # -- Windows: RegisterHotKey on a dedicated message-loop thread ---------
    def _start_hotkey_win(self, hotkey):
        fs_modifiers, vk = core.hotkey_to_win(hotkey)
        if vk is None:
            self._set_status(f"hotkey “{pretty_key(hotkey)}” is not supported "
                             "on Windows — try another key", MISS)
            return False
        self.hotkey_keysym = hotkey
        self.hotkey_on = True
        self._win_hk_result = queue.Queue()
        self._hotkey_thread = threading.Thread(
            target=self._hotkey_loop_win, args=(fs_modifiers, vk), daemon=True)
        self._hotkey_thread.start()
        try:
            ok, msg = self._win_hk_result.get(timeout=2)
        except queue.Empty:
            ok, msg = False, "hotkey registration timed out — try another key"
        if not ok:
            self.hotkey_on = False
            self._set_status(msg, MISS)
            return False
        self._set_status(f"Hotkey {pretty_key(hotkey)} active — open the RUNES "
                         f"tab in D2R and press {pretty_key(hotkey)} to scan.",
                         OK)
        return True

    def _hotkey_loop_win(self, fs_modifiers, vk):
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        self._win_hk_tid = ctypes.windll.kernel32.GetCurrentThreadId()
        WM_HOTKEY = 0x0312
        hk_id = 0x4442
        if not user32.RegisterHotKey(None, hk_id, fs_modifiers, vk):
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
        grab_modmask = self._grab_modmask
        self._grab_modmask = 0
        if d is not None:
            try:
                from Xlib import X
                root = d.screen().root
                if self._grab_keycode:
                    for lock_mask in (0, X.LockMask, X.Mod2Mask,
                                      X.LockMask | X.Mod2Mask):
                        try:
                            root.ungrab_key(self._grab_keycode,
                                            grab_modmask | lock_mask)
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
                clean_state = ev.state & ~(X.LockMask | X.Mod2Mask)
                if clean_state == self._grab_modmask:
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
