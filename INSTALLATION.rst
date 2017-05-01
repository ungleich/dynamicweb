Dynamicweb
----------
Installation for dynamicweb
=======


Requirements
============
* Python 3.5+
* Postgresql 
* Libmemchached (pylibmc)

Install
=======
The quick way:
    ``pip install -r requirements.txt``

Next find the dump.db file on stagging server. Path for the file is under the base application folder.

Install the postgresql server and import the database::
    ``psql -d app < dump.db``
    
**No migration is needed after a clean install, and You are ready to start developing.**

Development
===========
Project is separated in master branch and development branch, and feature branches.
Master branch is currently used on `Digital Glarus <https://digitalglarus.ungleich.ch/en-us/digitalglarus/>`_ and `Ungleich blog <https://digitalglarus.ungleich.ch/en-us/blog/>`_.

If You are starting to  create a new feature fork the github `repo <https://github.com/ungleich/dynamicweb>`_ and branch the development branch. 

After You have complited the task create a pull request and ask someone to review the code from other developers. 

**Cheat sheet for branching and forking**:

*branching*

``git branch feature_name && git checkout feature_name``


*fetching upstream(should be done everytime before development is started)*

``git fetch upstream && git merge upstream/feature_name``


`read more about getting code from upstream here <https://help.github.com/articles/syncing-a-fork/>`_

*merging your branch*
(**IMPORTANT**)

Before You make a pull request from Your forked branch to the ungleich make sure You did merge and resolve any conflicts You may find and that the application is running bug free.
Also You can run

``./manage test``


To merge upstream branch run this git commands.

``git fetch upstream``

``git checkout your_feature_branch``

``git merge remotes/upstream/develop``







