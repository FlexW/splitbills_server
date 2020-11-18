from .resources.user import UserResource
from .resources.users import UsersResource


def init_routes(api):
    api.add_resource(UserResource, "/users/<int:user_id>")
    api.add_resource(UsersResource, "/users")
