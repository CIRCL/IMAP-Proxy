# Modular Python IMAP proxy

[![Build Status](https://travis-ci.org/CIRCL/IMAP-Proxy.svg?branch=master)](https://travis-ci.org/CIRCL/IMAP-Proxy)

## Features

* Support IPv6 and TLS/SSL for both client and server connections
* Works with email applications as [Thunderbird](https://www.mozilla.org/en-US/thunderbird/) or [Outlook](https://outlook.live.com/owa/)
* Extensions: [UIDPLUS](https://rfc-editor.org/rfc/rfc4315.txt), [MOVE](https://rfc-editor.org/rfc/rfc6851.txt), [ID](https://rfc-editor.org/rfc/rfc2971.txt), [UNSELECT](https://rfc-editor.org/rfc/rfc3691.txt), [CHILDREN](https://rfc-editor.org/rfc/rfc3348.txt) and [NAMESPACE](https://rfc-editor.org/rfc/rfc2342.txt)

### Integrated modules

Modules are easy to integrate and to remove (just remove their calls in the proxy.py file).

* Sanitize emails and keep a copy in a Quarantine folder using the [PyCIRCLeanMail](https://github.com/CIRCL/PyCIRCLeanMail)
* Forward emails to [MISP](https://github.com/misp)

## Installation and run

![Demonstration with PyCIRCLeanMail](demo.gif)

### Installation

```
git clone https://github.com/CIRCL/IMAP-Proxy.git
cd IMAP-Proxy
python3 setup.py install
pip3 install -r requirements.txt
```

### Run the proxy

It can be started by adding arguments to the command line:
```
start_cl.py -h
```

Or it can be started with the configuration file *imapproxy.conf*:
```
start_conf.py
```

### Run with Thunderbird

First, open [Thunderbird](https://www.mozilla.org/en-US/thunderbird/), right-click on your email address and select *"Settings"*. In *"Server Settings"*, modify the *"Server Name"* by the IP address of the proxy (or localhost).

## How to contribute

Any help is welcome via pull requests and Issues or by contacting contributors of this project. Thank you !

## License

```
    Copyright (C) 2018 Xavier Schul
    Copyright (C) 2018 CIRCL - Computer Incident Response Center Luxembourg (c/o smile, security made in Lëtzebuerg, Groupement d'Intérêt Economique)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```