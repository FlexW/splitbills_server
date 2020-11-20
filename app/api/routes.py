from .resources.user import UserResource
from .resources.users import UsersResource
from .resources.group_add_user import GroupAddUserResource
from .resources.groups import GroupsResource
from .resources.bills import BillsResource


def init_routes(api):
    api.add_resource(UserResource, "/users/<int:user_id>")
    api.add_resource(UsersResource, "/users")

    api.add_resource(GroupsResource, "/groups")
    api.add_resource(GroupAddUserResource, "/groups/add_user")

    api.add_resource(BillsResource, "/bills")
