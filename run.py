#!/usr/bin/env python3
import argparse
import os

from gevent.monkey import patch_all
from gevent.pywsgi import WSGIServer
try:
    from psycogreen.gevent import patch_psycopg
except ImportError:
    def patch_psycopg(*_, **__): pass

__all__ = 'main',


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-H', '--host', default='0.0.0.0')
parser.add_argument('-p', '--port',
                    type=int,
                    default=int(os.environ.get('PORT', 2222)),
                    help='port number to listen')
parser.add_argument('-d', '--debug', action='store_true', default=False)
parser.add_argument('-c', '--config',
                    type=str,
                    default=str(os.environ.get('WORD_WAY_ENV', 'prod')))


def main():
    args = parser.parse_args()

    if not args.debug:
        patch_all()
        patch_psycopg()

    from word_way.app import create_app

    wsgi_app = create_app(args.config)
    if args.debug:
        wsgi_app.run(host=args.host, port=args.port, debug=True)
    else:
        http_server = WSGIServer((args.host, args.port), wsgi_app)
        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            raise SystemExit


if __name__ == '__main__':
    main()
