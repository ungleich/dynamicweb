dynamicweb deploy steps
=======================

The Makefile has a couple of tasks that can be useful when deploying the project, if using please
configure the values for the ssh host, user, port and target directory.

1. Upload the project.

   It's recommended to *make* use of the task 'rsync_upload' (See Makefile for more info.)
   If there's access to the git repo, just pull from master/develop.

2. Install system dependencies.

   If using debian, you could *make* use of the task 'install_debian_packages'.
   One cloud use the task 'install_debian_packages', which first do an update and then
   it installs the packages listed in the file ./requirements.debian.txt.

3. Make a new virtualenv with python3.

   In the requirements.debian.txt, 'virtualenvwrapper' is listed, maybe you could do:

   $ source /usr/share/virtualenvwrapper/virtualenvwrapper_lazy.sh
   $ mkvirtualenv dynamicweb --python=/usr/bin/python3

4. Install the requirements.txt for the dynamicweb project.

   Problem is you need an ssh key that exists in a github account, because I use two or three github repos
   for some packages, which they egg in pypi doesn't work well with python3, it's annoying...

   $ pip -r requirements.txt

5. Database/Memcached settings.

   Create postgres user: https://wiki.debian.org/PostgreSql.
   Create postgres database.
   Set postgres settings on dynamicweb/dynamicweb/settings.py
   Memcached should be already installed, we just need to check if the service is running.

6. Make migrations and sync the database

   Run:

   $ python manage.py makemigratoins
   $ python manage.py syncdb

7. Setup a circus configuration.

   [http://circus.readthedocs.org/en/0.11.1/]
   You could use the circus.ungleich.ini file in configs/ :

       $ circusd --daemon configs/circus.ungleich.ini

   That will start a new process for the webapp.
   To stop, restart, reload or see the status use circusctl.

       $ circusctl
       ...
       (circusctl) reload webapp

8. Configure nginx proxy.

   There's an example for the nginx proxy in configs/nginx.proxy.conf.
   For the stating server one can just copy configs/nginx.proxy.conf -> /etc/nginx/conf.d/ungleich.proxy.conf.
   Remember to comment/delete/change the configuration /etc/nginx/sites-enabled/default.

Other stuff (unsorted):

    python manage.py  makemigrations


    - restart
        - should have sudo!
        /etc/init.d/uwsgi restart
        
    - staticfiles: 
        python manage.py collectstatic
