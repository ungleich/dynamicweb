PY?=python3

BASEDIR=$(CURDIR)

SSH_HOST=dynamicweb-staging.ungleich.ch
SSH_PORT=22
SSH_USER=app
SSH_TARGET_DIR=/home/$(SSH_USER)/dynamicweb

help:
	@echo 'Makefile for a dynamicweb website'
	@echo '                                            '
	@echo 'Usage:                                      '
	@echo '  make rsync_upload                         '

collectstatic:
	$(PY?) $(BASEDIR)/manage.py collectstatic

rsync_upload:
	rsync -avz -e "ssh -p $(SSH_PORT)" --exclude .git --exclude .ropeproject --exclude __pycache__ --exclude *.pyc --exclude *~ --exclude *.psd $(BASEDIR) $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)
