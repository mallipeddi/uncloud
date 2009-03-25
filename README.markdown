Uncloud
=======

Uncloud is a Mac OS X utility that lets you download & archive emails from your GMail account. Archive files are generated in the "Apple Mail" MBox format. They can be easily imported into Apple Mail.

* Written in PyObjC 2.0 (works only in Leopard)
* Uses IMAP to fetch emails from GMail. You need to enable IMAP in GMail before you can use the app.
* Uses a patched version of `imaplib` since the one which ships with Python 2.5.1 (in Leopard) has a [known bug](http://bugs.python.org/issue1389051).
