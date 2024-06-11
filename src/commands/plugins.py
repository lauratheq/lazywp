#!/usr/bin/python3

import json

def config():
    return {
        'label': 'Plugins',
        'menu': 'Plugins',
        'actions': [
            ['a', 'toggle_activation', 'Toggle activation of a plugin'],
            ['i', 'install_plugin', 'Install new plugin'],
            ['r', 'deinstall_plugin', 'Deinstalls and removes a plugin'],
            ['u', 'update_plugin', 'Update plugin'],
            ['U', 'update_all_plugins', 'Update all plugins'],
            ['t', 'toggle_autoupdate', 'Toggle Autoupdate'],
            ['v', 'verify_plugin', 'Verify plugin agains wp.org']
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
    Builds the basic content for the plugins view

    Parameters:
        lazywp (obj): the lazywp object

    returns:
        list: the content to be drawn
    '''
    # set defaults
    content = []
    lazywp.wp("plugin list --format=json")
    plugins = lazywp.wp_output
    plugins = json.loads(plugins)

    # check if plugins exists
    if len(plugins) == 0:
        return [['No plugins found.']]

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
    active_plugin = plugins[lazywp.cursor_position]
    lazywp.command_holder['active_plugin'] = active_plugin

    # walk the plugins
    plugin_counter = 0
    for plugin in plugins:
        color = 'entry_default'
        if lazywp.cursor_position == plugin_counter:
            color = 'entry_hover'

        if plugin['update'] == 'available':
            color = 'entry_active'
            if lazywp.cursor_position == plugin_counter:
                color = 'entry_active_hover'

        line = lazywp.tui.draw_table_entry({
            plugin['name']: 0,
            plugin['status']: 8,
            plugin['version']: 10,
            plugin['update']: 17,
            plugin['auto_update']: 3
        }, color, lazywp)
        content.append([line, color])
        plugin_counter += 1

    return content

def toggle_activation(lazywp, data):
    '''
    Toggles the activation of a plugin

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    if data['active_plugin']['status'] == 'inactive':
        lazywp.msgbox([f"Activating plugin {data['active_plugin']['name']}"])
        lazywp.wp(f"plugin activate {data['active_plugin']['name']}", False)
    elif data['active_plugin']['status'] == 'active':
        lazywp.msgbox([f"Deactivating plugin {data['active_plugin']['name']}"])
        lazywp.wp(f"plugin deactivate {data['active_plugin']['name']}", False)

def install_plugin(lazywp, data):
    '''
    Asks a user for a plugin which needs to be installed

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    plugin = lazywp.slinputbox([f"Please enter the slug of the plugin you want to install"])
    lazywp.msgbox([f"Downloading plugin {plugin}"])
    lazywp.wp(f"plugin install {plugin}", False)
    lazywp.reload_content = True
 

def deinstall_plugin(lazywp, data):
    '''
    Deinstalls a plugin

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''

    result = lazywp.askbox([f"Are you sure you want to delete {data['active_plugin']['name']}?"])
    if result == True:
        lazywp.reload_content = True
        lazywp.cursor_position = 0
        lazywp.msgbox([f"Deleting plugin {data['active_plugin']['name']}"])
        lazywp.wp(f"plugin delete {data['active_plugin']['name']}", False)

def update_plugin(lazywp, data):
    '''
    Updates a plugin

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    lazywp.msgbox([f"Updating plugin {data['active_plugin']['name']}"])
    lazywp.wp(f"plugin update {data['active_plugin']['name']}", False)

def update_all_plugins(lazywp, data):
    '''
    Updates all plugins

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    lazywp.msgbox([f"Updating all plugins"])
    lazywp.wp(f"plugin update --all", False)

def toggle_autoupdate(lazywp, data):
    '''
    Toggles the autoupdate of a plugin

    Parameters:
        lazywp (obj): the lazywp object
        data (dict): the transfer data dict

    Returns:
        void
    '''
    lazywp.reload_content = True
    if data['active_plugin']['auto_update'] == 'off':
        lazywp.msgbox([f"Activating autoupdate for plugin {data['active_plugin']['name']}"])
        lazywp.wp(f"plugin auto-updates enable {data['active_plugin']['name']}", False)
    elif data['active_plugin']['auto_update'] == 'on':
        lazywp.msgbox([f"Deactivating autoupdate for plugin {data['active_plugin']['name']}"])
        lazywp.wp(f"plugin auto-updates disable {data['active_plugin']['name']}", False)


def verify_plugin(lazywp, data):
    lazywp.log.debug('verify_plugin')
