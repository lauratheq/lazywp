#!/usr/bin/python3

import json

def config():
    return {
        'label': 'Themes',
        'menu': 'Themes',
        'actions': [
            ['a', 'toggle_activation', 'Toggle activation of a theme'],
            ['i', 'install_theme', 'Install new theme'],
            ['r', 'deinstall_theme', 'Deinstalls and removes a theme'],
            ['u', 'update_theme', 'Update theme'],
            ['U', 'update_all_themes', 'Update all themes'],
            ['t', 'toggle_autoupdate', 'Toggle Autoupdate'],
            ['v', 'verify_theme', 'Verify theme agains wp.org']
        ],
        'statusbar': [
            'a: de/active',
            'i: install',
            'r: remove',
            'u: update (U: all)',
        ]
    }

def get_content(lazywp) -> list:
    '''
    Builds the basic content for the themes view

    Parameters:
        lazywp (obj): the lazywp object

    returns:
        list: the content to be drawn
    '''
    # set defaults
    content = []
    lazywp.wp("theme list --format=json")
    themes = lazywp.wp_output
    themes = json.loads(themes)

    # check if themes exists
    if len(themes) == 0:
        return [['No themes found.']]

    # build the table header
    lazywp.has_header = True
    headers = lazywp.tui.draw_table_header({
        'Name': 0,
        'Status': 8,
        'Version': 10,
        'Update Available': 17,
        'AU': 3
    }, lazywp)
    content += headers

    # set local holder
    active_theme = themes[lazywp.cursor_position]
    lazywp.command_holder['active_theme'] = active_theme

    # walk the themes
    theme_counter = 0
    for theme in themes:
        color = 'entry_default'
        if lazywp.cursor_position == theme_counter:
            color = 'entry_hover'

        if theme['update'] == 'available':
            color = 'entry_active'
            if lazywp.cursor_position == theme_counter:
                color = 'entry_active_hover'

        line = lazywp.tui.draw_table_entry({
            theme['name']: 0,
            theme['status']: 8,
            theme['version']: 10,
            theme['update']: 17,
            theme['auto_update']: 3
        }, color, lazywp)
        content.append([line, color])
        theme_counter += 1

    return content

def toggle_activation(lazywp, data):
    '''
    Toggles the activation of a theme

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    if data['active_theme']['status'] == 'inactive':
        lazywp.msgbox([f"Activating theme {data['active_theme']['name']}"])
        lazywp.wp(f"theme activate {data['active_theme']['name']}", False)
    elif data['active_theme']['status'] == 'active':
        lazywp.msgbox([f"Deactivating theme {data['active_theme']['name']}"])
        lazywp.wp(f"theme deactivate {data['active_theme']['name']}", False)

def install_theme(lazywp, data):
    '''
    Asks a user for a theme which needs to be installed

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    theme = lazywp.slinputbox([f"Please enter the slug of the theme you want to install"])
    lazywp.msgbox([f"Downloading theme {theme}"])
    lazywp.wp(f"theme install {theme}", False)
    lazywp.reload_content = True
 

def deinstall_theme(lazywp, data):
    '''
    Deinstalls a theme

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''

    result = lazywp.askbox([f"Are you sure you want to delete {data['active_theme']['name']}?"])
    if result == True:
        lazywp.reload_content = True
        lazywp.cursor_position = 0
        lazywp.msgbox([f"Deleting theme {data['active_theme']['name']}"])
        lazywp.wp(f"theme delete {data['active_theme']['name']}", False)

def update_theme(lazywp, data):
    '''
    Updates a theme

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    lazywp.msgbox([f"Updating theme {data['active_theme']['name']}"])
    lazywp.wp(f"theme update {data['active_theme']['name']}", False)

def update_all_themes(lazywp, data):
    '''
    Updates all themes

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    lazywp.msgbox([f"Updating all themes"])
    lazywp.wp(f"theme update --all", False)

def toggle_autoupdate(lazywp, data):
    '''
    Toggles the autoupdate of a theme

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    if data['active_theme']['auto_update'] == 'off':
        lazywp.msgbox([f"Activating autoupdate for theme {data['active_theme']['name']}"])
        lazywp.wp(f"theme auto-updates enable {data['active_theme']['name']}", False)
    elif data['active_theme']['auto_update'] == 'on':
        lazywp.msgbox([f"Deactivating autoupdate for theme {data['active_theme']['name']}"])
        lazywp.wp(f"theme auto-updates disable {data['active_theme']['name']}", False)


def verify_theme(lazywp, data):
    lazywp.log.debug('verify_theme')
