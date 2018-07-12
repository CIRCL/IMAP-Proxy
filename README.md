# Python IMAP transparent proxy server

## Features

* Support IPv6 and TLS/SSL for both client and server connections
* Works with email applications as [Thunderbird](https://www.mozilla.org/en-US/thunderbird/) or [Outlook](https://outlook.live.com/owa/)
* Extensions: [UIDPLUS](https://rfc-editor.org/rfc/rfc4315.txt), [MOVE](https://rfc-editor.org/rfc/rfc6851.txt), [ID](https://rfc-editor.org/rfc/rfc2971.txt), [UNSELECT](https://rfc-editor.org/rfc/rfc3691.txt), [CHILDREN](https://rfc-editor.org/rfc/rfc3348.txt) and [NAMESPACE](https://rfc-editor.org/rfc/rfc2342.txt)

### Integrated modules

Modules are easy to integrate and easy to remove (just remove their calls in the proxy.py file).

* Sanitize emails and keep a copy in a Quarantine folder using the [PyCIRCLeanMail](https://github.com/CIRCL/PyCIRCLeanMail)
* Forward emails to [MISP](https://github.com/misp)

## Installation and run

![Demonstration with PyCIRCLeanMail](demo.gif)

Clone this repository, install and run the proxy.

```
git clone https://github.com/CIRCL/IMAP-Proxy.git
cd IMAP-Proxy
python3 setup.py install
pip3 install -r requirements.txt
start.py -h
```

### Run with Thunderbird

First, open [Thunderbird](https://www.mozilla.org/en-US/thunderbird/), right-click on your email address and select *"Settings"*. In *"Server Settings"*, modify the *"Server Name"* by the IP address of the proxy (or localhost). That's it !