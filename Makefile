PY?=python3

BASEDIR=$(CURDIR)

SSH_HOST=dynamicweb.ungleich.ch
SSH_PORT=22
SSH_USER=app
SSH_TARGET_DIR=/home/$(SSH_USER)/app

help:
	@echo 'Makefile for a dynamicweb website'
	@echo '                                            '
	@echo 'Usage:                                      '
	@echo '  make rsync_upload                         '
	@echo '  make install_debian_packages              '

collectstatic:
	$(PY?) $(BASEDIR)/manage.py collectstatic

rsync_upload:
	rsync -P -rvzc -e "ssh -p $(SSH_PORT)" --exclude dynamicweb/local/local_settings.py --exclude .git --exclude .ropeproject --exclude __pycache__ --exclude *.pyc --exclude *~ --exclude *.psd $(BASEDIR)/* $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

install_debian_packages:
	apt-get update && cat $(BASEDIR)/requirements.debian.txt | xargs apt-get install -y --no-install-recommends
