#!/usr/bin/python3

import curses

def draw_table_header(headers, pad, pad_width):

    # get the max length of the headers to calc needed space
    header_width_values = headers.values()
    header_width_sum = sum(header_width_values)
    header_amount = len(header_width_values)
    spacers = header_amount - 1
    header_flex_width = pad_width - header_width_sum - spacers - 2

    # walk the headers
    walker = 0
    header_left_pos = 0
    for header in headers:
        
        # set the width of the flexible header
        header_width = headers[header]
        if header_width == 0:
            header_width = header_flex_width
        
        # add the vertical spacer to the header text
        spaces = header_width - len(header)
        header_text = header + (" " * spaces)
        if walker != 0:
            header_text = f"|{header_text}"

        # add needed spaces to the header
        header_length = len(header_text)
        if walker == 0:
            pad.addstr(0,0,header_text)

            spacers = "-" * header_length
            pad.addstr(1,0,spacers)
        else:
            pad.addstr(0,header_left_pos, header_text)
            spacers = "-" * (header_length - 1)
            pad.addstr(1,header_left_pos,"|")
            pad.addstr(1,header_left_pos+1,spacers)

        # add the length of the header to the position
        header_left_pos += header_length

        walker += 1

def draw_table_entry(entries, entry_position, color, pad, pad_width, l):

    # get the max length of the headers to calc needed space
    entry_width_values = entries.values()
    entry_width_sum = sum(entry_width_values)
    entry_amount = len(entry_width_values)
    spacers = entry_amount - 1
    entry_flex_width = pad_width - entry_width_sum - spacers - 2

    # walk the headers
    walker = 0
    entry_left_pos = 0
    for entry in entries:

        # set the width of the flexible header
        entry_width = entries[entry]
        if entry_width == 0:
            entry_width = entry_flex_width
        
        # add the vertical spacer to the header text
        spaces = entry_width - len(entry)
        entry_text = entry + (" " * spaces)
        if walker != 0:
            entry_text = f"|{entry_text}"

        # add needed spaces to the header
        entry_length = len(entry_text)
        pad.addstr(entry_position,entry_left_pos,entry_text, color)

        # add the length of the entry to the position
        entry_left_pos += entry_length

        walker += 1

