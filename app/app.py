import falcon.asgi


class HelloWorldResource:
    async def on_get(self, req: falcon.asgi.Request, resp: falcon.asgi.Response):
        resp.media = {"hello": "world"}


def create_app():
    app = falcon.asgi.App()
    app.add_route('/', HelloWorldResource())

    return app
