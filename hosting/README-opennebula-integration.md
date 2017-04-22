Here are the steps to follow for running opennebula-integration correctly.

1. Install [python-oca](https://github.com/python-oca/python-oca)
This is the library that allows sending XMLRPC commands to OpenNebula. Unfortunately, the latest version of oca available in Python package index is not compatible with python 3.5. Hence, one would need to download the latest version from the above github link and install it from there.
Assuming virtualenv is located at ~/python/env

```
~/python/env/bin/python setup.py build
sudo ~/python/env/bin/python setup.py install
```

2. Setup opennebula parameters in settings/local.py or settings/prod.py depending on deployment environment. The following are the parameters. Add them to the end of the file. Make sure to change them to fit your deployment.

```
# The user name of the OpenNebula infrastructure
OPENNEBULA_USERNAME = 'oneadmin'

# The password of the OpenNebula infrastructure
# The default credentials of the Sandbox OpenNebula VM is 
# oneadmin:opennebula
OPENNEBULA_PASSWORD = 'opennebula'

# The protocol is generally http or https
OPENNEBULA_PROTOCOL = 'http'

# The ip address or the domain name of the opennebula infrastructure
OPENNEBULA_DOMAIN = '192.168.182.173'

# The port to connect in order to send an xmlrpc request. The default 
# port is 2633
OPENNEBULA_PORT = '2633'

# The endpoint to which the XML RPC request needs to be sent to. The 
# default value is /RPC2
OPENNEBULA_ENDPOINT = '/RPC2'
```

