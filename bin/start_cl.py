import argparse

from imapproxy.proxy import IMAP_Proxy

if __name__ == '__main__':
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--certfile', help='Enable SSL/TLS connection with the given certfile (default: None). ' +
                                                    'Should be the path to a certificate.')
    parser.add_argument('-k', '--key', help='String key used to verify the integrity of emails append by the proxy (default: secret-proxy)')
    parser.add_argument('-p', '--port', type=int, help='Listen on the given port (default: 143 without certfile or 993)')
    parser.add_argument('-n', '--nclient', type=int, help='Maximum number of client supported by the proxy (default: 5)')
    parser.add_argument('-v', '--verbose', help='Echo IMAP payload', action='store_true')
    parser.add_argument('-6', '--ipv6', help='Enable IPv6 connection', action='store_true')
    args = parser.parse_args()

    # Start proxy
    print("Starting proxy")
    IMAP_Proxy(port=args.port, certfile=args.certfile, key=args.key, max_client=args.nclient, ipv6=args.ipv6, verbose=args.verbose)