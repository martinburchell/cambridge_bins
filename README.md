cambridge_bins
==============

Scrapes the Cambridge City Council website for bin collection dates:

Sends message if bin needs to be put out tomorrow:
```
$ ./check_collection_date.py '324 Mill Road' 'CB1 3NN' blue
$ ./check_collection_date.py '11 Rustat Road' 'CB1 3QR' green
$ ./check_collection_date.py '33 Emery Street' 'CB1 2AX' black
```
to send email:
```
$ ./check_collection_date.py '33 Emery Street' 'CB1 2AX' black 'Bin Reminder' sender@example.com recipient@example.com
```

To find out next collection date:
```
$ ./next_collection_date.py '33 Emery Street' 'CB1 2AX' black
```

Prerequisites:

* lxml
* BeautifulSoup

Installation:

After cloning:

    $ git submodule init
    $ git submodule update

from within the project directory.
