ungleich
========

dynamicweb
----------
Installation for dynamicweb
=======


Requirements
============
* Python 3.5+

Install
=======
The quick way::
    pip install -r requirements.txt

Next find the dump.db file on stagging server. Path for the file is under the base application folder.

Install the postgresql server and import the database::
    psql -d app < dump.db


Development
===========
Project is separated in master branch and development branch.
Master branch is currently used on [Digital Glarus](https://digitalglarus.ungleich.ch/en-us/digitalglarus/) and [Ungleich blog](https://digitalglarus.ungleich.ch/en-us/blog/).


