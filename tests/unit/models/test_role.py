import pytest

from app.models.role import Role, Permission, insert_default_roles


def test_add_permission():
    role = Role()
    role.add_permission(Permission.ADMIN)
    assert role.has_permission(Permission.ADMIN)


def test_remove_permission():
    role = Role()
    role.add_permission(Permission.ADMIN)
    role.remove_permission(Permission.ADMIN)
    assert not role.has_permission(Permission.ADMIN)


def test_reset_permission():
    role = Role()
    role.add_permission(Permission.ADMIN)
    role.reset_permissions()
    assert not role.has_permission(Permission.ADMIN)


def test_insert_default_roles():
    insert_default_roles()

    user_role = Role.query.filter_by(name="User").first()
    assert user_role.has_permission(Permission.DEFAULT)
    assert not user_role.has_permission(Permission.ADMIN)

    user_role = Role.query.filter_by(name="Admin").first()
    assert user_role.has_permission(Permission.DEFAULT)
    assert user_role.has_permission(Permission.ADMIN)
