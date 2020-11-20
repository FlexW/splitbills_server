from .resources.user import UserResource
from .resources.users import UsersResource
from .resources.group import GroupResource
from .resources.groups import GroupsResource
from .resources.bills import BillsResource


def init_routes(api):
    api.add_resource(UserResource, "/users/<int:user_id>")
    api.add_resource(UsersResource, "/users")

    api.add_resource(GroupResource, "/groups/<int:group_id>")
    api.add_resource(GroupsResource, "/groups")

    api.add_resource(BillsResource, "/bills")
