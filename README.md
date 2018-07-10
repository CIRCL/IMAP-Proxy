# Python IMAP transparent proxy server

Fully IMAP4rev1 compliant transparent proxy easy to modulate.

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

Clone this repository, install and run the proxy.

```
git clone https://github.com/xschul/IMAProxy.git
cd IMAProxy
pip3 install -r requirements.txt
python3 proxy/proxy.py -h
```

### Run with Thunderbird

First, open [Thunderbird](https://www.mozilla.org/en-US/thunderbird/), right-click on your email address and select "Settings". In "Server Settings", modify the "Server Name" by the IP address of the proxy. That's it !

It might not work if the IP address of the proxy is **IPv6** and the connection is **SSL/TLS**. If it does not work, please try with Connection security: None.

### Run the tests

```
python3 tests/test_proxy.py -h
python3 tests/test_proxy.py $username $password $ip_proxy
python3 tests/test_sanitizer.py -h
python3 tests/test_sanitizer.py $username $password $ip_proxy
```

## Authors

* **Xavier Schul**
* **CIRCL** - *Computer Incident Response Center Luxembourg* - [CIRCL](https://www.circl.lu/)
