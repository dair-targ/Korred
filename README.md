# Korred

<img src="misc/DnD_Korred.png" style="float:right;margin:1em;"/>

In Breton folklore, a [Korrigan](https://en.wikipedia.org/wiki/Korrigan)
([kɔˈriːɡɑ̃n]) is a fairy or dwarf-like spirit.
The word korrigan means "small-dwarf" (korr means dwarf,
ig is a diminutive and the suffix an is a hypocoristic).
It is closely related to the Cornish word korrik which means gnome.
The name changes according to the place.
Among the other names, there are korrig, **korred**, korrs,
kores, couril, crion, goric, kornandon,
ozigan, nozigan, torrigan, viltañs, poulpikan, paotred ar sabad...

Also Korred is the pair of WebExtension and MacOS application
that allow to run an arbitrary script in the terminal
via a single click in browser.

## How to use Korred

* Install Korred.app
* Install and configure Firefox browser extension
* Open some page and click Korred extension button.
A Terminal window should open.

## How Korred works

Korred consists of two components -
WebExtension (see [`extension/`](extension/README.md))
and the MacOS application bundle named `Korred.app` which is described below.
In order to use Korred, the application must be running
(you'll notice the `Korred` menu in the top menu bar),
and the WebExtension installed into the Firefox.

When user clicks onto extension button:
* All necessary information is extracted from the active tab
* Korred WebExtension sends the extracted data to `korred@example.org`
through the [Native Messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging)
* Firefox invokes `korred.py`, registered as a `korred@example.org` endpoint
and passes information from the WebExtension to this script
* `korred.py` compiles the information into a temporary shell script,
`~/Library/Application Support/Korred/temp.sh`
and then sends `SIGUSR2` to the Korred Daemon which PID
is stored in `~/Library/Application Support/Korred/agent.pid`.
* Upon receiving `SIGUSR2` Korred Daemon opens aforementioned script
in the new `Terminal.app` window
* User gets a new Terminal window with whatever script is configured.

## How to contribute

### Requirements:
1. MacOS
1. [Homebrew](https://brew.sh/)
1. XCode Command Line tools, to install run:
    - `xcode-select --install`)
1. Modern Firefox (v64+)
1. Python 3.7.1, to install you may:
    - Install [pyenv](https://github.com/pyenv/pyenv):
        `brew install pyenv`
    - Install Python 3.7.1 with the shared library:
         `PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.7.1`

### How to build

(optional) Obtain `apiKey` and `apiSecret` from [`Firefox Developer Hub`](https://addons.mozilla.org/en-US/developers/addons)
and put then into `./extension/local/credentials.json` like `{"apiKey":"...", "apiSecret":"..."}`.
This is necessary to sign the extension.

To get a MacOS application bundle run:

    python setup.py build_webextension py2app

The `Korred.app` would be placed in the `dist/` directory.
This application could be distributed as-is. MacOS installation
could be performed by moving this bundle into `/Applications/`.

Firefox extension for now is located in an unpacked state
under the `extension/` directory.
