# ChattyBoi

### This is a work-in-progress and is not ready for use yet.

ChattyBoi is a chat bot framework and application that lets you re-use the same code for any chatting platform. In other words, you can write a command or other trigger that will work on any chat that ChattyBoi can connect to - be it Twitch, Discord, or something like an online game or a social network. Of course, you can also add custom support for any chat-like API.

In addition to this feature, ChattyBoi provides simple APIs for the following:

- User configuration
- Storing chatter records with custom columns
- Privilege levels and other customizable groups for chatters
- Linking chatters across platforms (i.e. the same person can use different APIs to interact with the bot and access the same database entry)
- Chat moderation (for platforms that support it)
- Commands, and a way to create them inside the app
- GUI (headless mode also supported)

Other features:

- Configuration and databases stored in separate profiles, i.e. instances of the bot
- Based on asyncio from the ground up
- GUI: dashboard with customizable shortcuts; manual sending of messages; direct editing of the database

ChattyBoi is open-source and cross-platform (using Python and Qt). See individual files for license info. Unless otherwise noted, (c) 2021 Illia Boiko under the Apache 2.0 license, whose terms can be found in the LICENSE file.

## Extensions

Useful functionality is added to ChattyBoi through the extension system. Extensions are essentially regular Python packages, and thus can do anything that Python can do. You can install an extension by copying the package (i.e. a directory that contains `chattyboi_extension.toml`) into ChattyBoi's `extensions` directory (by default, it's inside the installation path). After that, you'll need to enable the extension for any desired profile(s) inside the launcher or by editing their configuration. Extensions cannot be added, changed, or removed without restarting the profile.

The following extensions are currently available:

The following extensions are planned:

- Twitch integration
- Discord integration
- Advanced moderation
- Minigames with virtual currency
- Web dashboard

## Creating extensions

See the documentation for instructions, or `ARCHITECTURE.md` for a quick overview.

## Contributing

Please read GitHub's Projects page for this repo in case your idea will become irrelevant soon, or is already being worked on.

Code style: please follow PEP 8, except for Qt-related names and signals, which should use camelCase. Please use tabs for indentation and don't go over 80 columns per line (with tabs counting as 4) except for closing delimiters. Do your best to write good docstrings (especially for public APIs) and keep them updated; use the [Sphinx style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).

All contributions are welcome!
