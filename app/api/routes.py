from .resources import HelloWorld


def init_routes(api):
    api.add_resource(HelloWorld, "/helloworld")
