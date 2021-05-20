# Architecture of ChattyBoi

ChattyBoi is a desktop application first and foremost, and its framework capabilities are a feature of the application. ChattyBoi can be installed and launched as-is. All code that uses the ChattyBoi API resides in extensions, which are Python packages loaded at runtime after a profile is selected.

## Terms used

The following terms are used in the documentation and in code comments. It's listed here because it can be ambiguous or confusing otherwise. These should not be capitalized.

**User**: the system user that launches the ChattyBoi application on their computer.  
**Chatter**: a person that interacts with ChattyBoi by means of sending messages to a chat-like API that ChattyBoi listens to. In other words, it's a chat user.  
**Chat**: a `Chat` object, i.e. something that messages can be sent to and received from.  
**Message**: a `Message` object, i.e. a data structure that corresponds to a message received from a chat.  
**ChattyBoi**: any or all elements of the application, including the launcher and the bot.  
**Profile**: a database and a set of configuration specific to an "instance" of the bot; has a name and can be selected with the GUI launcher or using the --profile command line argument.  
**Launcher**: the GUI window launched by the default main method, allowing the user to edit and/or select a profile, which is then used to launch the bot.  
**Bot**: the launched main program, including all of the loaded extensions. Inherently tied to a profile.  
**Load a profile**: start the bot under a given profile.  
**Extension**: a directory that contains a metadata file and is a valid Python package.  
**Installed extension**: an extension that can be accessed by ChattyBoi (e.g. selected from the launcher).  
**Enabled extension**: an extension that is enabled for a specific profile, and will be loaded whenever that profile is loaded.  
**Loaded extension**: the Python module object that exists during bot runtime and corresponds to an extension package.  
**Extension module**: same as "loaded extension".  
**Extension metadata**: data stored in an extension's metadata file.  
**Extension object**: an instance of `bot.Extension` that contains extension metadata and a reference to the extension module.   
**ExtAPI**: the `extapi` module; other than the bot object itself, it's the primary way for loaded extensions to interact with ChattyBoi.

## Classes

Extensions are expected to need only the following classes (and/or their subclasses) out of those used in ChattyBoi's internals:

**Profile** impl. in `profile.py`: a way to access data stored in a profile  
**DatabaseWrapper** impl. in `database.py`: an object that contains the database connection and several helper methods  
**Extension** impl. in `extension.py`: an extension object  
**Chatter** impl. in `classes.py`  
**Chat** impl. in `classes.py`  
**Message** impl. in `classes.py`  
**Command** impl. in `command.py`: the definition of trigger(s) and action(s) for a specific command

All of these can be accessed from the `extapi` module directly.

## Application state

Application state is shared between functions (including extension callbacks and slots) by passing an instance of `bot.Bot` as an argument.

## Extension runtime

All extension code is expected to either run at import or from callbacks. Extensions are imported after a profile was selected, but before the database or any other part of the bot is loaded. At that stage, extensions are expected to do only two things: register callbacks with extAPI's decorators, and/or perform actions that don't depend on the bot, such as reading some data from the filesystem. The latter should only be done if necessary, e.g. dynamically registering callbacks (which can still be done within other callbacks in most situations).

A list of callback decorators is available in the [extAPI documentation](null). Keep in mind that some of them are expected to wrap async functions.

## Internals: starting the bot

ChattyBoi can be launched as GUI or headless. In both situations, the process of loading a profile is the same; an instance of Bot is created. This is implemented in `main.py`, and the Bot class is implemented in `bot.py`. Functionality related to retrieving data from a profile is implemented in `profile.py`. The `Extension` class, along with the mechanism for importing extensions and creating Extension objects, is implemented in `extensions.py`.

After a `Bot` was created, it is initialized. This logic is implemented in the class. First, the profile's metadata is loaded, which contains the list of enabled extensions. Next, the extensions' metadata is loaded, which is used to figure out the load order.

Once extensions are imported, they're expected to define all custom classes and slots, then register synchronous extAPI callbacks as needed. Unless an extension started another thread or process at import, from this point onwards, everything extensions do will originate from callbacks or slots.

The bot will figure out when callbacks have to be called. Extensions are expected to connect signals to slots during initialization (not import) or inside of whatever object is concerned with the connection. After everything is initialized and chats are ready to receive messages, extensions should not need to interact with ChattyBoi's internals in any way except for emitting signals, calling methods, or accessing or modifying attributes of the Bot instance.

## Internals: main runtime

At main runtime, i.e. when chats receive messages, all events happen by means of Qt's signal and slot system. To facilitate the use of async, the qasync library is used. Slots that are asynchronous must be decorated or wrapped with `qasync.asyncSlot()`.

Extensions are expected to connect all needed signals and slots at initialization (not import), but connections can be made at any point during runtime if necessary. All signals (that extensions should be concerned with) which are not built into Qt objects are emitted from the bot object or individual chats. Other signals are not meant to be used by extensions.

Extension-provided callbacks have unrestricted functionality. However, it's encouraged to use async technology wherever possible. The bot uses asyncio's global event loop (to be more precise, it creates one using qasync and sets it as the main), so everything regarding that should be standard.

## Database

ChattyBoi uses a SQLite3 database to store chatter records for extensions to use. Every chatter has a unique integer ID, which is used as the primary key for all tables. Every extension has its own table with only the chatter ID as the default column; these tables are created automatically for every enabled extension (unless this is disabled in the metadata file), but they're expected to do their own maintenance. ChattyBoi also has its own table for some basic metadata about the chatters, such as their primary nickname.

The class `DatabaseWrapper`, implemented in `database.py`, is how ChattyBoi interacts with the database. It contains helper methods for clean-up and validation, and stores the actual SQLite3 connection object as an attribute.

## Linking chatters

Due to the fact that ChattyBoi can work on multiple chats at once, some chatters may wish to access their same record from multiple sources. However, a new record is created anytime ChattyBoi encounters a new chatter, even before they attempt to link. ChattyBoi implements a mechanism for combining two chatters into one, and extensions can implement their own way of dealing with this, which will override the default method. Documentation for the `bot.Bot.linkChatters` signal describes this in detail.

## Data structures

The base ChattyBoi application uses the following chat-related data structures, which are implemented in `classes.py`:

- **Chat**, a QObject that emits a signal when it receives a message and contains helper attributes.
- **Chatter**, an object that represents a single chatter in terms of the database. Helper methods implemented in this class should remove the need to manually write SQL for most basic needs. Chat objects are responsible for detecting linked chatters and using the same chatter ID as the other chat(s).
- **Message**, a static object that represents a single message received from a chat. Usually, subclasses of Chat will have corresponding subclasses of Message so that custom types of content (like images) can be stored there. Chat instances are responsible for creating Message instances and emitting related signals.
- **Command**, a description of an action and what triggers it. Usually, it will be connected to a `messageReceived` signal, which will check the message and perform the action if needed. It can also be connected to other things, such as GUI shortcuts.

## GUI

GUI elements are implemented in the `gui` package.

The main GUI is a window with several tabs, including the Dashboard. Extensions can register their own tabs. The Dashboard contains an area for customizable shortcuts, among other things. Extensions can register their own shortcuts. Both tabs and shortcuts can be enabled or disabled by the user, and this configuration is automatically saved by ChattyBoi.

## Headless

Headless mode is a way to non-interactively run ChattyBoi in the terminal. Extensions should not attempt to ask for user input. Any attempt to create widgets will be passed on to Qt itself, which, in turn, will terminate the application. However, if extAPI is used for GUI-related functionality, the related functions become no-op; this way, extensions don't have to worry about writing safeguards, though it should still be kept in mind in case it becomes undesirable behavior.

## Logging, warnings, and user messages

ChattyBoi uses Python's `logging` module, and all internals operate under the `chattyboi` logger. Extensions should prefer to only use extAPI's logging for simple output, as all messages above a certain log level may be treated specially.

## User configuration

User configuration that isn't profile-specific is stored using Qt's `QSettings` class, in user scope. This is implemented in `config.py`. Profile-specific settings are also stored using QSettings, but pointed to a file inside the profile, which is also used by extensions. Profile configuration is implemented in `profiles.py`.
