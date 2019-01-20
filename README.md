# tornado-http-firewall

An HTTP proxy that utilizes ACLs to control access to URIs.

**NOTE**: Consider this software alpha and extremely buggy and insecure.  You
probably shouldn't use this.

Requires Python>=3.6

## Usage

    usage: thfirewall [-h] [-a ADDRESS] [-p PORT] [-c CONFIG] [-d]

    An HTTP proxy that utilizes ACLs to control access to URIs

    optional arguments:
      -h, --help            show this help message and exit
      -a ADDRESS, --address ADDRESS
                            Port number to listen on
      -p PORT, --port PORT  Port number to listen on
      -c CONFIG, --config CONFIG
                            The ACL config YAML file
      -d, --debug           Show debug messages

## ACL Config Format

Here's an example ACL file.  This is a whitelist.  All URLs are evaluated
from each path part at a time until one matches.  So if someone requests
`/api/v0/get/QmASFD...`, it will first see if `/api` is allowed, then
`/api/v0`, etc...

`public` is the only named role.  Every other one should be by IP address.

    ---
    roles:
      public:
        - /api/v0/get
        - /api/v0/pin/ls
      127.0.0.1:
        - /api/v0/ping

