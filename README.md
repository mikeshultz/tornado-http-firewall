# tornado-http-firewall

An HTTP proxy that utilizes ACLs to control access to URIs.

**NOTE**: Consider this software alpha and extremely buggy and insecure.  You
probably shouldn't use this.

Requires Python>=3.6

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

