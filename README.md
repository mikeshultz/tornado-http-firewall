# tornado-http-firewall
[![Build Status](https://travis-ci.org/mikeshultz/solidbyte.svg?branch=master)](https://travis-ci.org/mikeshultz/solidbyte) [![Coverage Status](https://coveralls.io/repos/github/mikeshultz/tornado-http-firewall/badge.svg?branch=master)](https://coveralls.io/github/mikeshultz/tornado-http-firewall?branch=master)

An HTTP proxy that utilizes ACLs to control access to URIs.

**NOTE**: Consider this software alpha and extremely buggy and insecure.  You
probably shouldn't use this unless you're desparate for something like me. Pull
requests are welcome and encouraged.

Requires Python>=3.6

## Usage

    usage: thfirewall [-h] [-a ADDRESS] [-p PORT] [-t TARGET] [-c CONFIG] [-d]

    An HTTP proxy that utilizes ACLs to control access to URIs

    optional arguments:
      -h, --help            show this help message and exit
      -a ADDRESS, --address ADDRESS
                            Port number to listen on
      -p PORT, --port PORT  Port number to listen on
      -t TARGET, --target TARGET
                            The target top level URL to forward requests
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

