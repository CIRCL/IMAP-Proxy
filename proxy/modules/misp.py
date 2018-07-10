import re, imaplib, smtplib, email
from email.message import EmailMessage
from email import message_from_bytes
from .utils import parse_ids

# MISP client mailbox (should be created)
MISP_FOLDER = '\"MISP\"'
MISP_SERVER = 'freeblind.net'
BODY = """m2m:attach_original_mail:1"""
FILENAME = 'email.eml'

SUBJECT = 'IMAP proxy email'
SRC_ADDR = 'imapproxy'
DST_ADDR = 'mail2misp@freeblind.net'

Move_MISP = re.compile(r'\A(?P<tag>[A-Z0-9]+)'
    r'(\s(UID))?'
    r'\s(MOVE)'
    r'\s(?P<ids>[0-9:,]+)'
    r'\s' + re.escape(MISP_FOLDER), flags=re.IGNORECASE)

# Message data used to get the entire mail
MSG_DATA = 'BODY.PEEK[]'

def process(client):
    """ Apply the MISP module when an email is moved to the MISP mailbox

        client - IMAP_Client object

    """

    request = client.request
    match = Move_MISP.match(request)
    conn_server = client.conn_server
    folder = client.current_folder

    uidc = True if (('UID' in request) or ('uid' in request)) else False

    match = Move_MISP.match(request) 
    if not match: return 
    ids = match.group('ids')

    
    if ids.isdigit():
        # Only one email
        forward_to_misp(ids, conn_server, folder, uidc)
    else:
        # Multiple emails
        for id in parse_ids(ids):
            forward_to_misp(str(id), conn_server, folder, uidc)

def forward_to_misp(id, conn_server, folder, uidc):
    """ Forward an email to MISP.

        id - String containing the id of the email to forward;
        conn_server - imaplib connection to the server;
        folder - Current folder of the client;
        uidc - True if command contains UID flag

    """

    # Fetch the entire email
    conn_server.select(folder)
    result, response = conn_server.uid('fetch', id, MSG_DATA) if uidc else conn_server.fetch(id, MSG_DATA)

    if result == 'OK' and response != [b'The specified message set is invalid.'] and response != [None]:
        print(response[0][1])
        bmail = message_from_bytes(response[0][1])
    else:
        return

    # Initialize an email containing the moved email in attachment
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From'] = SRC_ADDR
    msg['To'] = DST_ADDR

    msg.set_content(BODY)
    msg.add_attachment(bmail, filename=FILENAME)

    s = smtplib.SMTP(MISP_SERVER)
    s.send_message(msg)
    s.quit()

    print('Sent !')