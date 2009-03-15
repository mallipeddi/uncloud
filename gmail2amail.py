
import imaplib, re, os

LABELS_TO_IGNORE = ["[Gmail]"]
DEFAULT_LABELS = [
                "INBOX", 
                "[Gmail]/All Mail", 
                "[Gmail]/Drafts", 
                "[Gmail]/Sent Mail", 
                "[Gmail]/Spam",
                "[Gmail]/Starred",
                "[Gmail]/Trash",
                ]
RAW_FOLDER_REGEX = re.compile("\((?P<flags>.*)\) \"(?P<root>.*)\" \"(?P<folder>.*)\"")
MBOXRD_SUB_REGEX = re.compile('^(>*From )', re.MULTILINE)

class Account(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.labels = self._fetch_labels()
    
    def get_new_connection(self):
        conn = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        conn.login(self.email, self.password)
        return conn
    
    def get_labels(self):
        return self.labels
    
    def get_iter_for_label(self, label):
        return FolderIterator(self.get_new_connection(), label)
    
    def _fetch_labels(self):
        conn = self.get_new_connection()
        (resp_type, resp_data) = conn.list()
        labels = []
        for raw_label in resp_data:
            label_name = self._parse_raw_label(raw_label)
            if label_name in LABELS_TO_IGNORE:
                continue
            else:
                labels.append(label_name)
        conn.logout()
        return labels
    
    def _parse_raw_label(self, raw_label_str):
        r = RAW_FOLDER_REGEX
        (flags, root, folder_name) = r.match(raw_label_str).groups()
        return folder_name


class FolderIterator(object):
    def __init__(self, conn, folder_name):
        self.conn = conn
        self.folder_name = folder_name
        self._prepare()

    def __iter__(self):
        return self

    def next(self):
        if self.cursor <= self.total:
            (resp_type, resp_data) = self.conn.fetch(str(self.cursor), 'RFC822')
            m = resp_data[0][1]
            self.cursor += 1
            return m
        else:
            self.close()
            raise StopIteration

    def get_total(self):
        return self.total

    def get_fetched(self):
        return self.cursor - 1

    def _prepare(self):
        (resp_type, resp_data) = self.conn.select(self.folder_name, True) # select the IMAP folder
        self.total = int(resp_data[0])
        self.cursor = 1

    def close(self):
        self.conn.logout()


class MboxrdWriter(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.fout = None
        self._setup_file_package()

    def append(self, mail):
        mail = self._escape_fromlines(mail)
        if self.fout is None:
            self.fout = open(self.filepath, "w")
        self.fout.write("From \n") # from line
        self.fout.write(mail) # escaped mail
        self.fout.write("\n") # blank line
        self.fout.flush()

    def _escape_fromlines(self, m):
        r = MBOXRD_SUB_REGEX
        return r.sub(lambda (m): '>' + m.group(1), m).replace("\r\n", "\n")

    def _setup_file_package(self):
        os.mkdir(self.filepath)
        # open an empty mbox file to write to
        self.fout = open(os.path.join(self.filepath, "mbox"), "w")
        
        # write an empty table_of_contents file
        toc = open(os.path.join(self.filepath, "table_of_contents"), "w")
        toc.close()

    def close(self):
        self.fout.close()
