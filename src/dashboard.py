#!/usr/bin/python3

def get_content(lazywp) -> list:

    content = []
    content.append(["   __   ___ ______  ___      _____"])
    content.append(["  / /  / _ /_  /\\ \\/ / | /| / / _ \\ "])
    content.append([" / /__/ __ |/ /_ \\  /| |/ |/ / ___/"])
    content.append(["/____/_/ |_/___/ /_/ |__/|__/_/ "])
    content.append([" "])

    content.append(["Welcome to lazywp - a tui wrapper for wpcli"])
    content.append([f"Version: {lazywp.version}"])
    content.append([" "])
    content.append(["Select menu entry and press [enter]"])
    content.append(["Use [tab] to switch between the menu and content"])
    content.append(["Press [?] for help"])
    content.append(["Press [q] to exit lazywp"])
    content.append([" "])

    content.append(["Visit https://github.com/lauratheq/lazywp for more information and contributing"])

    return content

