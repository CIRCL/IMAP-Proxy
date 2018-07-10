# Python IMAP transparent proxy server

## Features

* The proxy acts transparently and interprets every IMAP command
* Support TLS/SSL for both client and server connections
* Support IPv6
* Works with email applications as [Thunderbird](https://www.mozilla.org/en-US/thunderbird/) or [Outlook](https://outlook.live.com/owa/)
* Asynchronous, non-blocking socket connections
* Possibility to display IMAP payload
* Easy to modulate and to handle IMAP commands
* Extensions: [UIDPLUS](https://rfc-editor.org/rfc/rfc4315.txt), [MOVE](https://rfc-editor.org/rfc/rfc6851.txt), [ID](https://rfc-editor.org/rfc/rfc2971.txt), [UNSELECT](https://rfc-editor.org/rfc/rfc3691.txt), [CHILDREN](https://rfc-editor.org/rfc/rfc3348.txt) and [NAMESPACE](https://rfc-editor.org/rfc/rfc2342.txt).

### Integrated modules

Modules are easy to integrate and easy to remove (just remove their calls in the proxy.py file).

* Sanitize emails and keep a copy in a Quarantine folder using the [PyCIRCLeanMail](https://github.com/CIRCL/PyCIRCLeanMail)
* Forward emails to [MISP](https://github.com/misp)

## Installation and run

![Demonstration with PyCIRCLeanMail](demo.gif)

Clone this repository, install and run the proxy.

```
git clone https://github.com/CIRCL/PyCIRCLeanIMAP.git
cd PyCIRCLeanIMAP
pip3 install -r requirements.txt
python3 proxy/proxy.py -h
```

### Run with Thunderbird

First, open [Thunderbird](https://www.mozilla.org/en-US/thunderbird/), right-click on your email address and select "Settings". In "Server Settings", modify the "Server Name" by the IP address of the proxy. That's it !

### Run the tests

```
python3 tests/test_proxy.py -h
python3 tests/test_proxy.py $username $password $ip_proxy
python3 tests/test_sanitizer.py -h
python3 tests/test_sanitizer.py $username $password $ip_proxy
```