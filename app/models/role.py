from app import db


class Permission:
    DEFAULT = 0
    ADMIN = 2


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", back_populates='role')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = Permission.DEFAULT

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


def insert_default_roles():
    roles = {
        "User": [Permission.DEFAULT],
        "Admin": [
            Permission.DEFAULT, Permission.ADMIN
        ]
    }
    default_role = "User"
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
        role.reset_permissions()
        for perm in roles[r]:
            role.add_permission(perm)
            role.default = (role.name == default_role)
        db.session.add(role)
    db.session.commit()
