from jinja2 import Environment, FileSystemLoader
from stream import TwitterStream
from tornado import websocket
from settings import *
from uuid import uuid4
import tornado.ioloop
import tornado.web
import sys
import os


template_env = Environment(loader=FileSystemLoader(TEMPLATES_ROOT), auto_reload=DEBUG)
twitter_stream = TwitterStream(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)


def render(template, context):
    # a default context to have some standard vars in there.
    _context = {
        'STATIC_URL': STATIC_URL,
        'SOCKET_URL': SOCKET_URL
    }
    template = template_env.get_template(template)
    _context.update(context)
    return template.render(_context)


class WebSocket(websocket.WebSocketHandler):
    def open(self):
        self.opened = True
        self.uuid = uuid4().hex
        twitter_stream.add_client(self)

    def on_message(self, message):
        pass # right now we don't do anything for the client.

    def on_close(self):
        twitter_stream.remove_client(self)
        self.opened = False


class MainHandler(tornado.web.RequestHandler):
    def get(self, template='analysis.html'):
        self.write(render(template, {}))

routes = [
    (r"/", MainHandler),
    ("^%s$" % (SOCKET_URL,), WebSocket),
]

opts = {
    'static_path': STATIC_ROOT,
    'enable_pretty_logging': True,
}

application = tornado.web.Application(routes, **opts)

if __name__ == "__main__":
    try:
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit()
