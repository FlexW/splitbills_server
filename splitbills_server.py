import os

from app import create_app

app = create_app("default")


@app.cli.command()
def deploy():
    """Run deplyoment tasks."""
    pass


@app.cli.command()
def deploy_debug():
    """Run deplyoment tasks for development."""
    _insert_debug_data()


def _insert_debug_data():
    from app.models.user import User, insert_user
    from app.models.group import Group, insert_group
    from app.models.group_member import GroupMember

    user_schmidt = User(first_name="Max",
                        last_name="Schmidt",
                        email="schmidt@mail.de",
                        password="securepassword",
                        registered=True,
                        confirmed=True)
    insert_user(user_schmidt)
    user_fischer = User(first_name="Daniel",
                        last_name="Fischer",
                        email="fischer@mail.de",
                        password="securepassword",
                        registered=True,
                        confirmed=True)
    insert_user(user_fischer)
    user_weber = User(first_name="Maria",
                      last_name="Weber",
                      email="weber@mail.de",
                      password="securepassword",
                      registered=True,
                      confirmed=True)
    insert_user(user_weber)
    user_neumann = User(first_name="Anna",
                        last_name="Neumann",
                        email="neumann@mail.de",
                        password="securepassword",
                        registered=True,
                        confirmed=True)
    insert_user(user_neumann)
    user_hofmann = User(first_name="Tom",
                        last_name="Hofmann",
                        email="hofmann@mail.de",
                        password="securepassword",
                        registered=True,
                        confirmed=True)
    insert_user(user_hofmann)

    group_holiday = Group(name="Urlaub")
    group_holiday.group_members.append(GroupMember(
        user=user_schmidt, group=group_holiday))
    group_holiday.group_members.append(GroupMember(
        user=user_fischer, group=group_holiday))
    group_holiday.group_members.append(GroupMember(
        user=user_neumann, group=group_holiday))
    group_holiday.group_members.append(GroupMember(
        user=user_hofmann, group=group_holiday))
    insert_group(group_holiday)

    group_flat = Group(name="Wohnung")
    group_flat.group_members.append(GroupMember(
        user=user_schmidt, group=group_flat))
    group_flat.group_members.append(GroupMember(
        user=user_fischer, group=group_flat))
    group_flat.group_members.append(GroupMember(
        user=user_weber, group=group_flat))
    insert_group(group_flat)
