#!/usr/bin/python3

def config():
    return {
        'label': 'Plugins',
        'actions': [
            ['a', 'activate_plugin', 'Activate plugin'],
            ['d', 'deactivate_plugin', 'Deactivate plugin'],
            ['i', 'install_plugin', 'Install new plugin'],
            ['r', 'deinstall_plugin', 'Deinstalls and removes a plugin'],
            ['u', 'update_plugin', 'Update plugin'],
            ['U', 'update_all_plugins', 'Update all plugins'],
            ['t', 'toggle_autoupdate', 'Toggle Autoupdate'],
            ['v', 'verify_plugin', 'Verify plugin agains wp.org']
        ],
        'statusbar': [
            'a: activate',
            'd: deactivate',
            'i: install',
            'r: remove',
            'u: update'
        ]
    }

def data(lazywp):
    pass

def run(lazywp):
    
    # we always display a list of plugins so we first query them
    # by calling wp cli
    # get the plugins
    lazywp.wp("plugin list --format=json")
    plugins = lazywp.wp_output
    plugins = json.loads(plugins)

    if lazywp.key in (85, 97, 100, 114, 117):
        plugin = plugins[lazywp.cursor_position]
        reload = False

        # activate
        if lazywp.key == 97 and plugin['status'] == 'inactive':
            lazywp.msgbox([f"Activating plugin {plugin['name']}"])
            lazywp.wp(f"plugin activate {plugin['name']}", False)
            reload = True

        # deactivate
        if lazywp.key == 100 and plugin['status'] == 'active':
            lazywp.msgbox([f"Deactivating plugin {plugin['name']}"])
            lazywp.wp(f"plugin deactivate {plugin['name']}", False)
            reload = True

        # remove
        if lazywp.key == 114:
            result = lazywp.askbox([f"Are you sure you want to delete {plugin['name']}?"])
            if result == True:
                lazywp.msgbox([f"Deleting plugin {plugin['name']}"])
                lazywp.wp(f"plugin delete {plugin['name']}", False)
                reload = True

        # update
        if lazywp.key == 117 and plugin['update'] == 'available':
            lazywp.msgbox([f"Updating plugin {plugin['name']}"])
            lazywp.wp(f"plugin update {plugin['name']}", False)
            reload = True

        # update all
        if lazywp.key == 85:
            lazywp.msgbox(['Updating all plugins'])
            lazywp.wp(f"plugin update --all", False)
            reload = True

        # reload the plugin list because the items changed
        if reload == True:
            lazywp.msgbox(['Loading plugin list'])
            lazywp.wp("plugin list --format=json", False)

    # always clear the content first
    lazywp.content_pad_inside.clear()

    # build the table
    lazywp.tui.draw_table_header({
        'Name': 0,
        'Status': 8,
        'Version': 10,
        'Update Available': 17,
        'AU': 3
    }, lazywp.content_pad_inside, lazywp.content_pad_width)
    used_lines = 2

    # format
    plugins = lazywp.wp_output
    plugins = json.loads(plugins)

    plugin_counter = 0
    position = 2
    for plugin in plugins:
        
        color = lazywp.colors['plugin_entry_default']
        if lazywp.cursor_position == plugin_counter:
            color = lazywp.colors['plugin_entry_hover']

        if plugin['update'] == 'available':
            color = lazywp.colors['plugin_entry_update_available']
            if lazywp.cursor_position == plugin_counter:
                color = lazywp.colors['plugin_entry_update_available_inverse']

        lazywp.tui.draw_table_entry({
            plugin['name']: 0,
            plugin['status']: 8,
            plugin['version']: 10,
            plugin['update']: 17,
            plugin['auto_update']: 3
        }, position, color, lazywp.content_pad_inside, lazywp.content_pad_width, lazywp)

        position += 1
        used_lines += 1
        plugin_counter += 1

    # set the needed lines in order to make this pad scrollable
    lazywp.content_entries = plugin_counter
    lazywp.content_pad_inside_lines = used_lines

    return lazywp
