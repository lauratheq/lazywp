#!/usr/bin/python3

def draw(pad, version):

    pad.addstr(0, 2, "   __   ___ ______  ___      _____")
    pad.addstr(1, 2, "  / /  / _ /_  /\\ \\/ / | /| / / _ \\ ")
    pad.addstr(2, 2, " / /__/ __ |/ /_ \\  /| |/ |/ / ___/")
    pad.addstr(3, 2, "/____/_/ |_/___/ /_/ |__/|__/_/ ")

    pad.addstr(5, 2, "Welcome to lazywp - a tui wrapper for wpcli")
    pad.addstr(6, 2, f"Version: {version}")
    pad.addstr(8, 2, "Select menu entry and press [enter]")
    pad.addstr(9, 2, "Use [tab] to switch between the menu and content")
    pad.addstr(10, 2, "Press [?] for help")
    pad.addstr(11, 2, "Press [q] to exit lazywp")
    pad.addstr(13, 2, "Visit https://github.com/lauratheq/lazywp for more information and contributing")
    return 20


