#!/usr/bin/python3

import curses, sys
from curses.textpad import Textbox
from math import floor

def draw_menu_window(lazywp) -> None:
    '''
    Draws the window for the menu pad

    Returns:
        void
    '''

    # set dimensions
    height = lazywp.rows - 2
    width = 23

    # set color based on context
    color = lazywp.colors['default']
    if lazywp.context == 1:
        color = lazywp.colors['context_active']

    menu = curses.newwin(height, width, 0, 0)
    menu.clear()
    menu.attron(color)
    menu.box()
    menu.addstr(0, 2, " LazyWP ")
 
    lazywp.window.noutrefresh()
    menu.refresh()

def draw_menu_pad(lazywp):
    '''
    Draws the menu pad with the menu entries

    Returns:
        curses.pad obj
    '''
    width = 21
    height = len(lazywp.menu)

    pad = curses.newpad(height, width)
    counter = 0
    for menu_entry in lazywp.menu:

        # set label
        label = menu_entry
        llabel = label.lower()
        fillers = width - 1 - len(label)
        label += ' ' * fillers

        # set color
        color = lazywp.colors['default']
        if counter == lazywp.menu_hover:
            if lazywp.active_command == llabel:
                color = lazywp.colors['menu_active_hover']
            else:
                color = lazywp.colors['menu_hover']
        else:
            if lazywp.active_command == llabel:
                color = lazywp.colors['menu_active']
            else:
                color = lazywp.colors['default']

        # add label to pad
        pad.addstr(counter, 0, label, color)
        counter += 1

    pad.refresh(0, 0, 1, 2, height, width)
    return pad

def draw_content_window(lazywp) -> None:
    '''
    Draws the window for the content pad

    Returns:
        void
    '''

    # set dimensions
    height = lazywp.rows - 2
    width = lazywp.cols - 24

    # set color based on context
    color = lazywp.colors['default']
    if lazywp.context == 2:
        color = lazywp.colors['context_active']

    # set the label based on the current active command
    label = lazywp.commands[lazywp.active_command]['label']

    content = curses.newwin(height, width, 0, 24)
    content.clear()
    content.attron(color)
    content.box()
    content.addstr(0, 2, f" {label} ")
 
    lazywp.window.noutrefresh()
    content.refresh()

def draw_content_pad(lazywp):
    '''
    Adds the content pad to lazywp

    Returns:
        curses.pad obj
    '''
    width = lazywp.cols - 26
    height = len(lazywp.content)
    pad = curses.newpad(height, width)

    counter = 0
    for line in lazywp.content:

        color = lazywp.colors['default']
        string = line[0]
        if len(line) == 2:
            color = lazywp.colors[line[1]]
        pad.addstr(counter, 0, string, color)
        counter += 1

    pad.refresh(lazywp.content_pad_pos, 0, 1, 26, lazywp.rows-5, lazywp.cols-2)

    return pad

def draw_help_window(lazywp):
    '''
    Draws the help winwow and displays the content

    Parameters:
        lazywp (obj): the lazywp object

    Returns:
        void
    '''
    # set dimensions
    height = lazywp.rows - 6
    width = lazywp.cols - 20

    begin_x = floor(lazywp.cols / 2) - floor(width / 2)
    begin_y = floor(lazywp.rows / 2) - floor(height / 2)

    # set color
    color = lazywp.colors['menu_active_hover']

    # build the window
    help = curses.newwin(height, width, begin_y, begin_x)
    help.clear()
    help.attron(color)
    help.box()
    help.addstr(0, 2, f" Help [esc to close]")
    help.refresh()

    # build content
    content = []
    content.append(["Welcome to lazywp - a tui wrapper for wpcli"])
    content.append([f"Version: {lazywp.version}"])
    content.append([" "])
    content.append(["Select menu entry and press [enter]"])
    content.append(["Use [tab] to switch between the menu and content"])
    content.append(["Press [?] for help"])
    content.append(["Press [q] to exit lazywp"])
    content.append([" "])

    # fetch the commands
    for command_module in lazywp.commands:
        command_data = lazywp.commands[command_module]
        label = command_data['label']

        if len(command_data['actions']) != 0:
            content.append([f"Keybindings for {label}"])
            for binding in command_data['actions']:
                content.append([f"    [{binding[0]}] {binding[2]}"])
            content.append([" "])

    # build pad
    help_pad_pos = 0
    pad_width = width - 2
    pad_height = len(content)
    pad = curses.newpad(pad_height, pad_width)

    counter = 0
    for line in content:

        color = lazywp.colors['default']
        string = line[0]
        if len(line) == 2:
            color = lazywp.colors[line[1]]
        pad.addstr(counter, 0, string, color)
        counter += 1
    hidden_lines = len(content) - height-2
    
    pad.refresh(help_pad_pos, 0, begin_y+2, begin_x+2, height+1, width-2)

    # fetch the keys
    key = 0
    esc = False
    while esc != True:

        help.refresh()
        key = lazywp.window.getch() 

        # detect esc
        if key == 27:
            help.clearok(True)
            help.clear()
            help.refresh()
            pad.clearok(True)
            pad.clear()
            esc = True

        # scrolling position
        if key == curses.KEY_DOWN:
            if help_pad_pos < hidden_lines:
                help_pad_pos += 1
        elif key == curses.KEY_UP:
            if help_pad_pos > 0:
                help_pad_pos -= 1

        pad.refresh(help_pad_pos, 0, begin_y+2, begin_x+2, height+1, width-2)
 
def draw_table_header(headers, lazywp) -> list:
    '''
    Generates a string which simulates table header.
    It also beautifies it with spaces and -.

    Returns:
        list: the content
    '''

    # get the max length of the headers to calc needed space
    header_width_values = headers.values()
    header_width_sum = sum(header_width_values)
    header_amount = len(header_width_values)
    spacers = header_amount - 1
    header_flex_width = lazywp.cols - 26 - header_width_sum - spacers - 2

    # walk the headers
    content = []
    formatted_headers = []
    formatted_spacers = []
    
    # prepare headers
    for header in headers:
        
        # set the width of the flexible header
        header_width = headers[header]
        if header_width == 0:
            header_width = header_flex_width
        
        # add the vertical spacer to the header text
        spaces = header_width - len(header)
        header_text = header + (" " * spaces)

        # add needed spaces to the header
        formatted_headers.append(header_text)
        header_spacer = '-' * len(header_text)
        formatted_spacers.append(header_spacer)

    content.append(['|'.join(formatted_headers)])
    content.append(['|'.join(formatted_spacers)])
    return content

def draw_table_entry(entries, color, lazywp):
    '''
    Generates a string which simulates table entries.

    Parameters:
        entries (list): list of col entries
        color (str): current set color
        lazywp (obj): the lazywp object

    Returns:
        str: the content
    '''

    # get the max length of the headers to calc needed space
    entry_width_values = entries.values()
    entry_width_sum = sum(entry_width_values)
    entry_amount = len(entry_width_values)
    spacers = entry_amount - 1
    entry_flex_width = lazywp.cols - 26 - entry_width_sum - spacers - 2

    # walk the headers
    formatted_entries = []
    for entry in entries:

        # set the width of the flexible header
        entry_width = entries[entry]
        if entry_width == 0:
            entry_width = entry_flex_width
        
        # add the vertical spacer to the header text
        spaces = entry_width - len(entry)
        entry_text = entry + (" " * spaces)

        # add needed spaces to the header
        formatted_entries.append(entry_text)

    return '|'.join(formatted_entries)
 
def msgbox(lazywp, messages=[]):
    '''
    Builds a messagebox

    Parameters:
        lazywp (obj): lazywp
        messages (list): list of messages to be displayed

    Returns:
        void
    '''
 
    # remove the box if it exists
    if isinstance(lazywp.box, curses.window):
        lazywp.box.clearok(True)
        lazywp.box.clear()
        lazywp.box.refresh()

    # calculate needed width and height
    base_height = 2
    height = len(messages) + base_height
    max_width = 0
    for message in messages:
        if len(message) > max_width:
            max_width = len(message)
    width = max_width + 2

    # center box
    begin_x = floor(lazywp.cols / 2) - floor(width / 2)
    begin_y = floor(lazywp.rows / 2) - floor(height / 2) - 2

    # draw the pad
    lazywp.box = curses.newwin(height, width, begin_y, begin_x)
    lazywp.box.clear()
    lazywp.box.attron(lazywp.colors['messagebox'])
    lazywp.box.box()

    # add messages
    position_y = 1
    for message in messages:
        lazywp.box.addstr(position_y,1,message)
        position_y += 1

    lazywp.box.refresh()

def askbox(lazywp, messages=[]):
    '''
    Builds a messagebox which lets the user confirm their input

    Parameters:
        lazywp (obj): lazywp
        messages (list): list of messages to be displayed

    Returns:
        void
    '''
    # remove the box if it exists
    if isinstance(lazywp.box, curses.window):
        lazywp.box.clearok(True)
        lazywp.box.clear()
        lazywp.box.refresh()

    # calculate needed width and height
    base_height = 2
    height = len(messages) + base_height
    max_width = 0
    for message in messages:
        if len(message) > max_width:
            max_width = len(message)
    if max_width < 17:
        max_width = 17
    width = max_width + 2

    # center box
    begin_x = floor(lazywp.cols / 2) - floor(width / 2)
    begin_y = floor(lazywp.rows / 2) - floor(height / 2) - 2

    # draw the pad
    lazywp.box = curses.newwin(height, width, begin_y, begin_x)
    lazywp.box.clear()
    lazywp.box.attron(lazywp.colors['askbox'])
    lazywp.box.box()

    # add messages
    position_y = 1
    for message in messages:
        lazywp.box.addstr(position_y,1,message)
        position_y += 1

    key = 0
    enter = False
    focus = 1
    while enter != True:
        # display yes no
        if focus == 1:
            lazywp.box.addstr(position_y, 2, '[ Yes ]', lazywp.colors['askbox_hover'])
        else:
            lazywp.box.addstr(position_y, 2, '[ Yes ]', lazywp.colors['askbox'])

        if focus == 2:
            lazywp.box.addstr(position_y, 10, '[ No ]', lazywp.colors['askbox_hover'])
        else:
            lazywp.box.addstr(position_y, 10, '[ No ]', lazywp.colors['askbox'])

        lazywp.box.refresh()
        key = lazywp.window.getch() 

        # detect input for qbox
        if key == curses.KEY_LEFT:
            focus = 1
        elif key == curses.KEY_RIGHT:
            focus = 2
        elif key == 10:
            enter = True

    if focus == 2:
        return False
    return True

def slinputbox(lazywp, messages=[]):
    '''
    Builds a messagebox which lets the user input a single line

    Parameters:
        lazywp (obj): lazywp
        messages (list): list of messages to be displayed

    Returns:
        string the user input
    '''

    # remove the box if it exists
    if isinstance(lazywp.box, curses.window):
        lazywp.box.clearok(True)
        lazywp.box.clear()
        lazywp.box.refresh()

    # calculate needed width and height
    base_height = 3
    height = len(messages) + base_height
    max_width = 0
    for message in messages:
        if len(message) > max_width:
            max_width = len(message)
    if max_width < 17:
        max_width = 17
    width = max_width + 2

    # center box
    begin_x = floor(lazywp.cols / 2) - floor(width / 2)
    begin_y = floor(lazywp.rows / 2) - floor(height / 2) - 2

    # draw the pad
    lazywp.box = curses.newwin(height, width, begin_y, begin_x)
    lazywp.box.clear()
    lazywp.box.attron(lazywp.colors['inputbox'])
    lazywp.box.box()

    # add messages
    position_y = 1
    for message in messages:
        lazywp.box.addstr(position_y,1,message)
        position_y += 1

    input_base = lazywp.box.subwin(1, width-2, begin_y+position_y, begin_x+1)
    input_base.clear()
    input_base.refresh()
    lazywp.box.refresh()

    textbox = curses.textpad.Textbox(input_base)
    textbox.edit(enter_is_terminate)
    message = textbox.gather()
    return message

def enter_is_terminate(x):
    '''
    Callback function for the curses textbox to identify
    the 'enter' press and returning the content

    Parameters:
        x (int): the key pressed

    Returns:
        int
    '''
    # enter detected
    if x == 10:
        x = 7
    return x
