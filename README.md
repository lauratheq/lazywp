# lazywp - a TUI for wpcli

lazywp is a terminal user interface for wpcli commands. It is heavily inspired by awesome projects like [lazygit](https://github.com/jesseduffield/lazygit) and [lazydocker](https://github.com/jesseduffield/lazydocker).

## Elevator Pitch

wpcli is a powerful tool to manage your WordPress installation on the command line. It comes with a lot of commands and services which helps with the daily work. But memorising all the commands and its different operators is hard. The goal of lazywp is to have a very simple interface where every needed information and tool is in one place.

## Installation

Currently there is no simplier way than this:
1. Clone the repository to somewhere you want
1. Make `lazywp` executeable via `chmod +x lazywp`
1. Link `lazywp` to you local bin folder like `ln -s lazywp /usr/local/bin/lazywp`
1. Create log file `[sudo] touch /var/log/lazywp.log`
1. Head to your WordPress installation and type `lazywp`

## Active Development

Due to the early state of this project the active development takes place in the `main` branch. If you want to contribute please fork this repository and perform a pull request against the main branch. This process will change as soon as there is a release present.

If you want to implement a wpcli command see `src/commands/plugins.py` as template for your development.

### Contributing

Please note that this project is adapting the [Contributor Code of Conduct](https://learn.wordpress.org/online-workshops/code-of-conduct/) from WordPress.org even though this is not a WordPress project. By participating in this project you agree to abide by its terms.

### Known problems

* The terminal size must be at least 126x30 or the system crashes

### Current Todos

#### MVP

**Basic Features**
* [ ] Display help which aggregates the infos from the commands
* [ ] Version check
* [x] Logging mechanism
* [x] Basic Layout
 * [x] Panels
 * [x] Scrolling
 * [x] Dynamic status bar
* [x] Dynamic loading of commands
* [ ] Methods to make usage of curses easier within the project
 * [x] Tables
 * [ ] Modals 
* [ ] Code comments (i know ...)
* [ ] functionality documentation in README.md
* [ ] Automatic installation process
* [x] wpcli wrapper method for usage within modules

**wpcli Commands**

Determine for each command what exactly to implement

* [ ] admin
* [ ] chache
* [ ] cap
* [ ] cli
* [ ] comment
* [ ] config
* [ ] core
* [ ] cron
* [ ] db
* [ ] dist-archive
* [ ] embed
* [ ] eval
* [ ] eval-file
* [ ] export
* [ ] find
* [ ] help
* [ ] i18n
* [ ] import
* [ ] language
* [ ] maintenance-mode
* [ ] media
* [ ] menu
* [ ] network
* [ ] option
* [ ] package
* [ ] plugin
 * [x] update
 * [x] update all
 * [x] activate
 * [x] deactivate
 * [ ] toggle auto update
 * [ ] install
 * [x] remove
* [ ] post
* [ ] post-type
* [ ] profile
* [ ] rewrite
* [ ] role
* [ ] scaffold
* [ ] search-replace
* [ ] server
* [ ] shell
* [ ] sidebar
* [ ] site
* [ ] super-admin
* [ ] taxonomy
* [ ] term
* [ ] theme
* [ ] transient
* [ ] user
* [ ] widget

#### Planned features (also with questionable ideas)

* Plugin System (like neovim's approach)
* Package Manager for plugins
* Autoupdate
* Installation of WordPress
* Full network support
* Fuzzy-Filter for the menu
* compatibility with wp cli commands
* Contributing processes
* Sponsorship handling
* Website
* Global installation
* implementation of `--allow-root`
* CI/CD stuff
* Automatic tests and code analyzes
