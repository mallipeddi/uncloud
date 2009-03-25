"""
gmail2amail.py
Copyright (c) 2009 Harish Mallipeddi

Utilities to fetch emails from a GMail folder via IMAP and archive into a MBox file
"""

import myimaplib as imaplib
import re, os

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
    "Represents a GMail account. Stores the account email/password and available labels for backup"
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self._labels = self._fetch_labels()
    
    def get_new_connection(self):
        conn = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        conn.login(self.email, self.password)
        return conn
    
    def _get_labels(self):
        return self._labels
    labels = property(_get_labels)
    
    def get_label(self, label_name):
        return Label(self, label_name)
    
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


class Label(object):
    "Represents a label/folder in a GMail account. Also serves as an iterator to iterate over the emails in the label."
    def __init__(self, account, label_name):
        self.account = account
        self.label_name = label_name

    def __iter__(self):
        self.conn = self.account.get_new_connection()
        (resp_type, resp_data) = self.conn.select(self.label_name, True) # select the IMAP folder
        self._total = int(resp_data[0])
        self._fetched = 1
        return self

    def next(self):
        if self._fetched <= self._total:
            (resp_type, resp_data) = self.conn.fetch(str(self._fetched), 'RFC822')
            m = resp_data[0][1]
            self._fetched += 1
            return m
        else:
            raise StopIteration

    def _get_total(self):
        return self._total
    total = property(_get_total)

    def _get_fetched(self):
        return self._fetched - 1
    fetched = property(_get_fetched)

    def close(self):
        self.conn.logout()


class MboxrdWriter(object):
    "Writes emails to a mbox file (format compatible with Apple Mail)"
    def __init__(self, filepath):
        self.filepath = filepath
        self.fout = None

    def append(self, mail):
        mail = self._escape_fromlines(mail)
        if self.fout is None:
            self._setup_file_package()
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
