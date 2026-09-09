"""Regression checks for hotkey parsing and platform mappings."""

from types import SimpleNamespace

from d2rc import App, pretty_key
from d2r_runewords import hotkey_to_win, parse_hotkey


def test_parse_hotkey():
    assert parse_hotkey("Ctrl+J") == ({"Ctrl"}, "J")
    assert parse_hotkey("Ctrl+Shift+F8") == ({"Ctrl", "Shift"}, "F8")
    assert parse_hotkey(" Alt + j ") == ({"Alt"}, "j")


def test_windows_modifier_mapping():
    assert hotkey_to_win("Ctrl+J") == (0x4000 | 0x0002, ord("J"))
    assert hotkey_to_win("Ctrl+Shift+F8") == (
        0x4000 | 0x0002 | 0x0004, 0x77
    )


def test_tk_modifier_capture():
    event = SimpleNamespace(state=0x0004 | 0x0001, keysym="j")
    assert App._event_modifiers(event) == ["Ctrl", "Shift"]
    assert pretty_key("Ctrl+j") == "Ctrl+J"


if __name__ == "__main__":
    test_parse_hotkey()
    test_windows_modifier_mapping()
    test_tk_modifier_capture()
    print("hotkey mapping OK")
