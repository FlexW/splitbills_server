from .resources.user import UserResource
from .resources.users import UsersResource
from .resources.group_members import GroupMembersResource
from .resources.group_member import GroupMemberResource
from .resources.groups import GroupsResource
from .resources.group import GroupResource
from .resources.group_bills import GroupBillsResource
from .resources.bills import BillsResource
from .resources.bill import BillResource
from .resources.tokens import TokensResource
from .resources.token import TokenResource
from .resources.tokens_refresh import TokensRefreshResource
from .resources.welcome import WelcomeResource
from .resources.friends import FriendsResource


def init_routes(api):
    api.add_resource(WelcomeResource, "/")

    api.add_resource(TokensResource, "/tokens")
    api.add_resource(TokenResource, "/tokens/<int:token_id>")
    api.add_resource(TokensRefreshResource, "/tokens/refresh")

    api.add_resource(UserResource, "/users/<int:user_id>")
    api.add_resource(UsersResource, "/users")

    api.add_resource(GroupResource, "/groups/<int:group_id>")
    api.add_resource(GroupsResource, "/groups")
    api.add_resource(GroupMembersResource, "/groups/<int:group_id>/members")
    api.add_resource(GroupMemberResource,
                     "/groups/<int:group_id>/members/<int:user_id>")
    api.add_resource(GroupBillsResource,
                     "/groups/<int:group_id>/bills")

    api.add_resource(BillResource, "/bills/<int:bill_id>")
    api.add_resource(BillsResource, "/bills")

    api.add_resource(FriendsResource, "/friends")
