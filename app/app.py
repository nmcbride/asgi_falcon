import falcon.asgi


class HelloWorldResource:
    async def on_get(self, req, resp):
        resp.media = {"hello": "world"}


def create_app():
    app = falcon.asgi.App()
    app.add_route('/', HelloWorldResource())

    return app
