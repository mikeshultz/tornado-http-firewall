import re
import sys
import tornado.ioloop
import tornado.web
import tornado.httpclient
from argparse import ArgumentParser
from typing import Type, List, Tuple
from . import __doc__ as http_firewall_description
from .logging import get_logger, set_debug_logging

log = get_logger(__name__)

HTTP_HEADER_PATTERN = r'^(?P<name>[\w\d\-]+): (?P<value>[\w\d\s]+)\r\n$'
BLOCK_HEADERS = [
    'Transfer-Encoding'
]


def build_backend_url(root_url: str, path: str, arguments: dict) -> str:
    """ Build a backend URL for the proxy request """

    args: List[Tuple[str, str]] = []

    # Strip the param string from the path if it's there.  Unclear why it's
    # not always one way or the other
    if '?' in path and len(arguments) > 0:
        path = path.split('?')[0]

    for k, vs in arguments.items():
        for val in vs:
            if isinstance(val, bytes):
                args.append((k, val.decode('utf-8')))
            else:
                args.append((k, str(val)))

    return '{}{}?{}'.format(
        root_url,
        path,
        '&'.join(['{}={}'.format(k, v) for k, v in args])
    )

    return '{}{}'.format(root_url, path)


class ForwardHandler(tornado.web.RequestHandler):
    METHODS = ['GET', 'POST', 'CONNECT']

    @tornado.web.asynchronous
    async def get(self, *args, **kwargs):
        log.debug("get({}, {})".format(args, kwargs))
        # get path
        path = self.request.uri

        log.debug("request path: {}".format(path))

        # Send new request
        client = tornado.httpclient.AsyncHTTPClient()

        try:
            req_url = build_backend_url(self.proxy_dest_url, path,
                                        self.request.arguments)

            log.debug("Backend request URL: {}".format(req_url))

            request = tornado.httpclient.HTTPRequest(
                req_url,
                method='GET',
                streaming_callback=self.on_chunk,
                header_callback=self.on_headers,
            )

            await client.fetch(request)

        except tornado.httpclient.HTTPClientError as err:

            if err.code == 500:
                log.exception("500 Returned from backend")
            log.debug("backend returned {} for {}".format(err.code, path))
            raise tornado.web.HTTPError(err.code)

        except Exception as err:

            log.exception("Unknown error making proxy request to backend")
            raise err

    def on_chunk(self, chunk):
        """ Write a chunk to the client """
        self.write(chunk)

    def on_headers(self, header):
        """ Handle response headers """
        if header != '\r\n':
            match = re.match(HTTP_HEADER_PATTERN, header)
            if not match:
                log.warning("Header unmatched. Not sending to client.")
                return
            if match.group('name') not in BLOCK_HEADERS:
                log.debug("Setting header {} to {}".format(
                    match.group('name'),
                    match.group('value'),
                ))
                self.set_header(match.group('name'), match.group('value'))
            else:
                log.debug("Blocked header {}".format(match.group('name')))


def forward_handler_factory() -> Type[ForwardHandler]:
    handler = ForwardHandler
    setattr(handler, 'proxy_dest_url', 'http://localhost:5001')
    return handler


def make_app() -> tornado.web.Application:
    return tornado.web.Application([
        (r"/(.*)", forward_handler_factory()),
    ])


def main(args=None):
    """ Main app entry point """

    # TODO: Remove below
    set_debug_logging()

    parser = ArgumentParser(description=http_firewall_description)
    parser.add_argument('-a', '--address', type=str, default='127.0.0.1',
                        help='Port number to listen on')
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help='Port number to listen on')
    args = parser.parse_args(args or sys.argv[1:])

    app = make_app()
    app.listen(args.port, address=args.address)
    tornado.ioloop.IOLoop.current().start()
