#!/usr/bin/python3

import curses

def draw_menu_pad(context, pad_height, colors, window):
        
    menu_pad = curses.newpad(pad_height,25)
    window.noutrefresh()
    menu_pad.attrset(colors['pad_border_inactive'])
    if context == 1:
        menu_pad.attrset(colors['pad_border_active'])
    menu_pad.box()
    menu_pad.addstr(0, 2, " LazyWP ")
    menu_pad.refresh(0, 0, 0, 0, pad_height, 25)

    return menu_pad

def draw_menu_entries(menu_entries, menu_hover, pad_height, colors, window):

    menu_entries_pad = curses.newpad(100, 22)
    menu_entry_counter = 0
    for menu_entry in menu_entries:
        menu_entry_label = menu_entries[menu_entry]
        fillers = 21 - len(menu_entry_label)
        menu_entry_label += ' ' * fillers
        if menu_entry_counter == menu_hover:
            menu_entries_pad.addstr(menu_entry_counter, 0, menu_entry_label, colors['menu_active'])
        else:
            menu_entries_pad.addstr(menu_entry_counter, 0, menu_entry_label)
        menu_entry_counter += 1
    menu_entries_pad.refresh(0, 0, 1, 2, pad_height-2, 22)
    return menu_entries_pad

def draw_content_pad(height, width, context, menu_active, colors, window):

    # create content pad
    content_pad = curses.newpad(height, width)
    window.noutrefresh()
    content_pad.attrset(colors['pad_border_inactive'])
    if context == 2:
        content_pad.attrset(colors['pad_border_active'])
    content_pad.box()

    # pad title
    content_pad_title = menu_active
    content_pad.addstr(0, 2, f" {content_pad_title} ")
    content_pad.refresh(0, 0, 0, 25, height, width+25)

    return content_pad

def draw_status_bar(entries, rows, cols, colors, window):

    text = " | ".join(entries)
    window.attron(colors['statusbar'])
    window.addstr(rows-2, 0, text)
    window.addstr(rows-2, len(text), " " * (cols - len(text)))
    window.attroff(colors['statusbar'])


