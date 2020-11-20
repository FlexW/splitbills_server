from .resources.user import UserResource
from .resources.users import UsersResource
from .resources.group_members import GroupMembersResource
from .resources.group_member import GroupMemberResource
from .resources.groups import GroupsResource
from .resources.bills import BillsResource


def init_routes(api):
    api.add_resource(UserResource, "/users/<int:user_id>")
    api.add_resource(UsersResource, "/users")

    api.add_resource(GroupsResource, "/groups")
    api.add_resource(GroupMembersResource, "/groups/members")
    api.add_resource(GroupMemberResource, "/groups/members/<int:user_id>")

    api.add_resource(BillsResource, "/bills")
