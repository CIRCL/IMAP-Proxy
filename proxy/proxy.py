import sys, socket, ssl, re, base64, threading, argparse, imaplib
from modules import pycircleanmail, misp

# Default maximum number of client supported by the proxy
MAX_CLIENT = 5  
# Default ports
IMAP_PORT, IMAP_SSL_PORT = 143, 993
CRLF = b'\r\n'

# Tagged request from the client
Tagged_Request = re.compile(r'(?P<tag>[A-Z0-9]+)'
    r'(\s(UID))?'
    r'\s(?P<command>[A-Z]*)'
    r'(\s(?P<flags>.*))?', flags=re.IGNORECASE)
# Tagged response from the server
Tagged_Response= re.compile(r'\A(?P<tag>[A-Z0-9]+)'
    r'\s(OK)'
    r'(\s\[(?P<flags>.*)\])?'
    r'\s(?P<command>[A-Z]*)', flags=re.IGNORECASE)

# Capabilities of the proxy
CAPABILITIES = ( 
    'IMAP4',
    'IMAP4rev1',
    'AUTH=PLAIN',
    'UIDPLUS',
    'MOVE',
    'ID',
    'UNSELECT', 
    'CHILDREN', 
    'NAMESPACE'
)

# Authorized domain addresses with their corresponding host
HOSTS = {
    'hotmail': 'imap-mail.outlook.com',
    'outlook': 'imap-mail.outlook.com',
    'yahoo': 'imap.mail.yahoo.com',
    'gmail': 'imap.gmail.com'
}

# Intercepted commands
COMMANDS = (
    'authenticate',
    'capability',
    'login',
    'logout',
    'select',
    'move',
    'fetch'
)

class IMAP_Proxy:
    
    r""" Implementation of the proxy.

    Instantiate with: IMAP_Proxy([port[, host[, certfile[, max_client[, verbose[, ipv6]]]]]])

            port - port number (default: None. Standard IMAP4 / IMAP4 SSL port will be selected);
            host - host's name (default: localhost);
            certfile - PEM formatted certificate chain file (default: None);
                Note: if certfile is provided, the connection will be secured over
                SSL/TLS. Otherwise, it won't be secured.
            max_client - Maximum number of client supported by the proxy (default: global variable MAX_CLIENT);
            verbose - Display the IMAP payload (default: False)
            ipv6 - Should be enabled if the ip of the proxy is IPv6 (default: False)
    
    The proxy listens on the given host and port and creates an object IMAP4_Client (or IMAP4_Client_SSL for
    secured connections) for each new client. These socket connections are asynchronous and non-blocking.
    """

    def __init__(self, port=None, host='', certfile=None, max_client=MAX_CLIENT, verbose=False, ipv6=False):
        self.verbose = verbose
        self.certfile = certfile

        if not port: # Set default port
            port = IMAP_SSL_PORT if certfile else IMAP_PORT

        if not max_client:
            max_client = MAX_CLIENT 

        if ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        self.sock.bind(('', port))
        self.sock.listen(max_client)
        self.listen()


    def listen(self):
        """ Wait and create a new IMAP_Client for each new connection. """

        def new_client(ssock):
            if not self.certfile: # Connection without SSL/TLS
                IMAP_Client(ssock, self.verbose)
            else: # Connection with SSL/TLS
                IMAP_Client_SSL(ssock, self.certfile, self.verbose)

        while True:
            try:
                ssock, addr = self.sock.accept()
                threading.Thread(target = new_client, args = (ssock,)).start()
            except KeyboardInterrupt:
                break
            
        if self.sock:
            self.sock.close()

class IMAP_Client:

    r""" Implementation of a client.

    Instantiate with: IMAP_Client([ssock[, verbose]])

            socket - Connection (with or without SSL/TLS) with the client
            verbose - Display the IMAP payload (default: False)
    
    Listens on the socket commands from the client.
    """

    def __init__(self, socket, verbose = False):
        self.verbose = verbose
        self.conn_client = socket
        self.conn_server = None

        try:
            self.send_to_client('* OK Service Ready.') # Server greeting
            self.listen_client()
        except ssl.SSLError:
            pass
        except (BrokenPipeError, ConnectionResetError):
            print('Connections closed')
        except ValueError as e:
            print('[ERROR]', e)

        self.close()

    #       Listen client/server and connect server

    def listen_client(self):
        """ Listen commands from the client """

        while self.listen_client:
            for request in self.recv_from_client().split('\r\n'): # In case of multiple requests

                match = Tagged_Request.match(request)

                if not match:
                    # Not a correct request
                    self.send_to_client(self.error('Incorrect request'))
                    raise ValueError('Error while listening the client: '
                        + request + ' contains no tag and/or no command')

                self.client_tag = match.group('tag')
                self.client_command = match.group('command').lower()
                self.client_flags = match.group('flags')
                self.request = request

                if self.client_command in COMMANDS:
                    # Command supported by the proxy
                    getattr(self, self.client_command)()
                else:
                    # Command unsupported -> directly transmit the command 
                    # to the server and response to the client
                    self.transmit()

    def transmit(self):
        """ Replace client tag by the server tag """
        server_tag = self.conn_server._new_tag().decode()
        self.send_to_server(self.request.replace(self.client_tag, server_tag, 1))
        self.listen_server(server_tag)
                
    def listen_server(self, server_tag):
        """ Continuously listen the server until a command completion response 
        with the corresponding server_tag is received"""

        while True:
            response = self.recv_from_server()
            response_match = Tagged_Response.match(response)

            ##   Command completion response
            if response_match: 
                server_response_tag = response_match.group('tag')
                if server_tag == server_response_tag:
                    # Verify the command completion corresponds to the client command
                    self.send_to_client(response.replace(server_response_tag, self.client_tag, 1))
                    return 
            
            ##   Untagged or continuation response or data messages
            self.send_to_client(response)

            
            if response.startswith('+') and self.client_command.upper() != 'FETCH':
                ##   Continuation response
                client_sequence = self.recv_from_client()
                while client_sequence != '': # Client sequence ends with empty request
                    self.send_to_server(client_sequence)
                    client_sequence = self.recv_from_client()
                self.send_to_server(client_sequence)

    def connect_server(self, username, password):
        """ Connect to the real server of the client for its credentials """

        username = self.remove_quotation_marks(username)
        password = self.remove_quotation_marks(password)

        domains = username.split('@')[1].split('.')[:-1] # Remove before '@' and remove '.com' / '.be' / ...
        domain = ' '.join(str(d) for d in domains) 

        try:
            hostname = HOSTS[domain]
        except KeyError:
            self.send_to_client(self.error('Unknown hostname'))
            raise ValueError('Error while connecting to the server: '
                    + 'Invalid domain name '+ domain)

        print("Trying to connect ", username)
        self.conn_server = imaplib.IMAP4_SSL(hostname)

        try:
            self.conn_server.login(username, password)
        except imaplib.IMAP4.error:
            self.send_to_client(self.failure())
            raise ValueError('Error while connecting to the server: '
                    + 'Invalid credentials: ' + username + " / " + password)

        self.send_to_client(self.success())

    #       Supported IMAP commands

    def capability(self):
        """ Send capabilites of the proxy """
        self.send_to_client('* CAPABILITY ' + ' '.join(cap for cap in CAPABILITIES) + ' +')
        self.send_to_client(self.success())

    def authenticate(self):
        """ Authenticate the client and call the given auth mechanism """
        auth_type = self.client_flags.split(' ')[0].lower()
        getattr(self, self.client_command+"_"+auth_type)() 

    def authenticate_plain(self):
        """ Get the username and password using plain mechanism and 
        connect to the server """
        self.send_to_client('+')
        request = self.recv_from_client()
        (empty, busername, bpassword) = base64.b64decode(request).split(b'\x00')
        username = busername.decode()
        password = bpassword.decode()
        self.connect_server(username, password)

    def login(self):
        """ Login and connect to the server """
        (username, password) = self.client_flags.split(' ')
        self.connect_server(username, password)

    def logout(self):
        """ Logout and stop listening the client """
        self.listen_client = False
        self.transmit()

    def select(self):
        """ Select a mailbox """
        self.set_current_folder(self.client_flags)
        self.transmit()

    def move(self):
        """ Move an email to another mailbox """
        misp.process(self)
        self.transmit()

    def fetch(self):
        """ Fetch an email """
        pycircleanmail.process(self)
        self.transmit()

    #       Command completion

    def success(self):
        """ Success command completing response """
        return self.client_tag + ' OK ' + self.client_command + ' completed.'

    def failure(self):
        """ Failure command completing response """
        return self.client_tag + ' NO ' + self.client_command + ' failed.'

    def error(self, msg):
        """ Error command completing response """
        return self.client_tag + ' BAD ' + msg

    #       Sending and receiving methods

    def send_to_client(self, str_data):
        """ Send String data (without CRLF) to the client """

        b_data = str_data.encode('utf-8', 'replace') + CRLF
        self.conn_client.send(b_data)

        if self.verbose: 
            print("[<--]: ", b_data)

    def recv_from_client(self):
        """ Return the last String request from the client without CRLF """

        b_request = self.conn_client.recv(1024)
        str_request = b_request.decode('utf-8', 'replace')[:-2] # decode and remove CRLF

        if self.verbose: 
            print("[-->]: ", b_request)

        return str_request

    def send_to_server(self, str_data):
        """ Send String data (without CRLF) to the server """

        b_data = str_data.encode('utf-8', 'replace') + CRLF
        self.conn_server.send(b_data)

        if self.verbose: 
            print("  [-->]: ", b_data)

    def recv_from_server(self):
        """ Return the last String response from the server without CRLF """

        b_response = self.conn_server._get_line()
        str_response = b_response.decode('utf-8', 'replace')    

        if self.verbose: 
            print("  [<--]: ", b_response)

        return str_response

    #       Utils

    def set_current_folder(self, folder):
        """ Set the current folder of the client """
        self.current_folder = self.remove_quotation_marks(folder)

    def remove_quotation_marks(self, text):
        """ Remove quotation marks of a String """
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        return text

    def close(self):
        """ Close connection with the client """
        if self.conn_client:
            self.conn_client.close()
    

class IMAP_Client_SSL(IMAP_Client):
    r""" IMAP_Client class over SSL/TLS connection

    Instantiate with: IMAP_Client_SSL([ssock[, certfile[, verbose]]])
    
        ssock - Socket with the client;
        certfile - PEM formatted certificate chain file;
        verbose - Display the IMAP payload (default: False)

    for more documentation see the docstring of the parent class IMAP_Client.
    """

    def __init__(self, ssock, certfile, verbose = False):
        try:
            self.conn_client = ssl.wrap_socket(ssock, certfile=certfile, server_side=True)
        except ssl.SSLError as e:
            raise

        IMAP_Client.__init__(self, self.conn_client, verbose)

if __name__ == '__main__':
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--certfile', help='Enable SSL/TLS connection over port 993 (by default) with the certfile given. '
        + 'Without this argument, the connection will not use SSL/TLS over port 143 (by default)')
    parser.add_argument('-p', '--port', type=int, help='Listen on the given port')
    parser.add_argument('-n', '--nclient', type=int, help='Maximum number of client supported by the proxy')
    parser.add_argument('-v', '--verbose', help='Echo IMAP payload', action='store_true')
    parser.add_argument('-6', '--ipv6', help='Enable IPv6 connection (the proxy should have an IPv6 address)', action='store_true')
    args = parser.parse_args()

    # Start proxy
    IMAP_Proxy(port=args.port, certfile=args.certfile, max_client=args.nclient, verbose=args.verbose, ipv6=args.ipv6)