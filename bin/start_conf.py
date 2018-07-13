import configparser

from imapproxy.proxy import IMAP_Proxy

if __name__ == '__main__':
    # Parser
    parser = configparser.RawConfigParser()
    fp = open('imapproxy.conf', 'rt')
    parser.read_file(fp)

    certfile = parser.get('general', 'certfile')
    key = parser.get('general', 'key')
    port = parser.getint('general', 'port')
    nclient = parser.getint('general', 'nclient')
    verbose = parser.getboolean('general', 'verbose_enabled')
    ipv6 = parser.getboolean('general', 'ipv6_enabled')

    # Start proxy
    print("Starting proxy")
    IMAP_Proxy(port=port, certfile=certfile, key=key, max_client=nclient, ipv6=ipv6, verbose=verbose)